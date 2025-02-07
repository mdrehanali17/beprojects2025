from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import QuizBattle, Question,User
import asyncio

class BattleConsumer(AsyncWebsocketConsumer):
    # Store players in the quiz room
    players = {}
    answers = {}

    async def connect(self):
        self.quiz_id = self.scope['url_route']['kwargs']['quiz_id']
        self.battle_id = self.scope['url_route']['kwargs']['battle_id']
        self.quiz_group_name = f'quiz_battle_{self.battle_id}'
        user = self.scope["user"]
        
        # Initialize the answers dictionary
        if not hasattr(self, 'answers'):
            self.answers = {}

        # Initialize the dictionary for the current quiz if it doesn't exist
        if self.quiz_group_name not in self.answers:
            self.answers[self.quiz_group_name] = {
                'player_1': None,
                'player_2': None
            }

        # Ensure users are authenticated
        if user.is_authenticated:
            # Get or create a quiz battle instance
            battle = await self.get_or_create_battle(user)

            # Check if the user is already in a battle
            if battle:
                if user.username not in self.players.get(self.quiz_group_name, []):
                    if len(self.players.get(self.quiz_group_name, [])) < 2:
                        # Add player to the room
                        self.players.setdefault(self.quiz_group_name, []).append(user.username)
                        await self.channel_layer.group_add(self.quiz_group_name, self.channel_name)
                        await self.accept()

                        # Check if the room has only one player, then show "Waiting for opponent..."
                        if len(self.players[self.quiz_group_name]) == 1:
                            battle.player_1 = user 
                            battle.status = 'waiting'
                            await self.update_battle(battle)

                            await self.channel_layer.group_send(
                                self.quiz_group_name,
                                {
                                    'type': 'user_join',
                                    'username': user.username,
                                    'message': f'{user.username} has joined. Waiting for opponent...'
                                }
                            )
                        elif len(self.players[self.quiz_group_name]) == 2:
                            # Set player 2 and update the status to active
                            battle.player_2 = user
                            battle.status = 'active'
                            await self.update_battle(battle)

                            await asyncio.sleep(3)

                            # Notify both players the game is starting
                            await self.channel_layer.group_send(
                                self.quiz_group_name,
                                {
                                    'type': 'battle_ready',
                                    'message': 'Both players have joined. The battle is starting!'
                                }
                            )
                    else:
                        await self.close()  
                else:
                    await self.close()  
            else:
                await self.close()  
        else:
            await self.close() 

    async def receive(self, text_data):
        data = json.loads(text_data)
        print('Data:', data)
        battle, player_1, player_2 = await self.get_battle_data()

        if data.get('type') == 'battle_over':
            battle.status = 'completed'
            await self.update_battle(battle)
            await self.determine_winner(battle)
        elif data.get('type') == 'time_up':
            question_index = data['question_index']
            await self.process_answers(battle, question_index, time_up=True)
        else:
            user = self.scope["user"]
            answer = data['answer']
            question_index = data['question_index']
            print(f"Received answer: {answer} for question index: {question_index}")

            # Track player answers by question index
            if user == player_1:
                self.answers[self.quiz_group_name]['player_1'] = {'answer': answer, 'question_index': question_index}
            elif user == player_2:
                self.answers[self.quiz_group_name]['player_2'] = {'answer': answer, 'question_index': question_index}

            # Check if both players have answered the same question
            if (self.answers[self.quiz_group_name]['player_1'] is not None and
                self.answers[self.quiz_group_name]['player_2'] is not None):
                await self.process_answers(battle, question_index)

    async def process_answers(self, battle, question_index, time_up=False):
        print("Processing answers")
        questions = await self.get_questions()
        question = questions[question_index]
        correct_answer = question.correct_option

        # Score calculation logic
        player_1_answered = self.answers[self.quiz_group_name]['player_1'] is not None
        player_2_answered = self.answers[self.quiz_group_name]['player_2'] is not None

        if player_1_answered and self.answers[self.quiz_group_name]['player_1']['answer'] == correct_answer:
            battle.player_1_score += 10

        if player_2_answered and self.answers[self.quiz_group_name]['player_2']['answer'] == correct_answer:
            battle.player_2_score += 10

        # Save battle state
        await self.update_battle(battle)

        # Clear answers for this question after processing
        self.answers[self.quiz_group_name] = {'player_1': None, 'player_2': None}

        # Determine whether to move to the next question or end the game
        if question_index + 1 < len(questions):
            await self.channel_layer.group_send(
                self.quiz_group_name,
                {
                    'type': 'both_answer',
                    'message': 'Move',
                    'question_index': question_index,
                })
        else:
            battle.status = 'completed'
            await self.update_battle(battle)
            await self.determine_winner(battle)


    async def next_question_or_end(self, battle):
        # Check if there are more questions
        next_question_index = battle.current_question_index + 1
        questions = await self.get_questions()

        if next_question_index < len(questions):
            # Move to the next question
            battle.current_question_index = next_question_index
            battle.current_question = questions[next_question_index]
            await self.update_battle(battle)

            # Send the next question to both players
            await self.channel_layer.group_send(
                self.quiz_group_name,
                {
                    'type': 'next_question',
                    'question': battle.current_question.text,
                    'options': [
                        battle.current_question.option1,
                        battle.current_question.option2,
                        battle.current_question.option3,
                        battle.current_question.option4,
                    ]
                }
            )

        else:
            
            # End the battle if no more questions
            battle.status = 'completed'
            await self.update_battle(battle)
            if self.timer_task[self.quiz_group_name]:
                self.timer_task[self.quiz_group_name].cancel()
            # Determine the winner
            await self.determine_winner(battle)
    

    async def determine_winner(self, battle):
        try:
            player_1_username, player_2_username = self.players.get(self.quiz_group_name, [])
            if battle.player_1_score > battle.player_2_score:
                winner_username = player_1_username
                winner_score = battle.player_1_score
            elif battle.player_2_score > battle.player_1_score:
                winner_username = player_2_username
                winner_score = battle.player_2_score
            else:
                winner_username = 'Tie'
                winner_score = battle.player_2_score

            await self.channel_layer.group_send(
                self.quiz_group_name,
                {
                    'type': 'battle_over',
                    'message': 'The battle is over!',
                    'winner_username': winner_username,
                    'winner_score': winner_score,
                    'player_1_score': battle.player_1_score,
                    'player_2_score': battle.player_2_score,
                }
            )
        except Exception as e:
            print(f"Error determining winner: {e}")

    async def next_question(self, event):
        # Send the next question to both players
        await self.send(text_data=json.dumps({
            'message': 'Next question!',
            'question': event['question'],
            'options': event['options']
        }))
    
    async def both_answer(self, event):
        # Send the next question to both players
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'index': event['question_index'],
        }))
    async def disconnect(self, close_code):
        user = self.scope["user"]

        if user.username in self.players.get(self.quiz_group_name, []):
            self.players[self.quiz_group_name].remove(user.username)
            # battle = await self.get_or_create_battle(user)
            battle = await self.get_battle()
            # Remove the battle if there are not enough players
            if len(self.players[self.quiz_group_name]) < 2 and battle.status != 'completed':
                await self.delete_battle()
                await self.channel_layer.group_send(
                    self.quiz_group_name,
                    {
                        'type': 'battle_ended',
                        'message': 'One player has left. The battle has been ended.',
                        'action': 'go_back',
                        'username': user.username,
                    }
                )
        await self.channel_layer.group_discard(self.quiz_group_name, self.channel_name)

    async def user_join(self, event):
        # Send join message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'players': self.players[self.quiz_group_name]
        }))

    async def battle_ready(self, event):
        # Notify both users that the battle is starting
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'players': self.players[self.quiz_group_name]
        }))
        
        for i in range(5,0,-1):
            await self.send(text_data=json.dumps({
                'type':'timer',
                'message':f'Battle starts in {i} seconds'
            }))
            await asyncio.sleep(1)

        questions = await self.get_questions()
        if questions:
            battle = await self.get_battle()
            battle.current_question = questions[0]
            battle.current_question_index = 0
            await self.update_battle(battle)

            # Send all questions at once
            questions_list = [
                {
                    'text': question.text,
                    'options': [question.option1, question.option2, question.option3, question.option4],
                }
                for question in questions
            ]

            await self.send(text_data=json.dumps({
                'message': 'The battle started!',
                'questions': questions_list  # Send the full list of questions to the client
            }))
        else:
            # Handle case where no questions are available
            await self.send(text_data=json.dumps({
                'message': 'No questions available for this quiz.',
                'action': 'end'
            }))
            
    async def battle_over(self, event):
        # Send battle end message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'winner_username': event['winner_username'],
            'winner_score': event['winner_score'],
            'player_1_score': event['player_1_score'],
            'player_2_score': event['player_2_score'],
        }))

    async def battle_ended(self, event):
        # Notify users that the battle has ended
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'action': event.get('action', ''),
            'username': event['username']
        }))
        

    async def user_left(self, event):
        # Notify users that someone has left
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    @database_sync_to_async
    def get_or_create_battle(self, user):
        # Check if the user is already in a battle
        existing_battle = QuizBattle.objects.filter(
            player_1=user, status='waiting'
        ).first() or QuizBattle.objects.filter(
            player_2=user, status='waiting'
        ).first()
        
        if existing_battle:
            return existing_battle

        # Create a new battle instance
        battle = QuizBattle.objects.filter(quiz_id=self.quiz_id, status='waiting').first()
        if not battle:
            battle = QuizBattle.objects.create(
                quiz_id=self.quiz_id,
                player_1=user,
                status='waiting'
            )
        return battle
    
    @database_sync_to_async
    def update_battle(self, battle):
        battle.save()

    @database_sync_to_async
    def delete_battle(self):
        QuizBattle.objects.filter(battle_id=self.battle_id).delete()
    
    @database_sync_to_async
    def get_questions(self):
        return list(Question.objects.filter(quiz_id=self.quiz_id))
    
    @database_sync_to_async
    def get_battle(self):
        return QuizBattle.objects.get(battle_id=self.battle_id)

    @database_sync_to_async
    def get_battle_data(self):
        battle =  QuizBattle.objects.get(battle_id=self.battle_id)
        return battle, battle.player_1, battle.player_2
    
    @database_sync_to_async
    def get_question(self):
        return Question.objects.filter(quiz_id=self.quiz_id).first()
