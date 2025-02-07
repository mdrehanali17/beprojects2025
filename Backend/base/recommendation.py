from django.db.models import Q, Count, Avg, Sum
from .models import SportDetails, UserSportInteraction, Booking
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import CountVectorizer

# Function for Content-Based Filtering
def content_based_filtering(user_id):
    try:
        sports = SportDetails.objects.values('id', 'category', 'price', 'location')
        sportdetails = pd.DataFrame(list(sports))
        if sportdetails.empty:
            print("No sports details found.")
            return pd.DataFrame()  

        user_interactions = UserSportInteraction.objects.filter(user_id=user_id).values(
            'sport_id', 'view_count', 'booking_count'
        )
        usersportinteraction = pd.DataFrame(list(user_interactions))

        if usersportinteraction.empty:
            print("No user interactions found.")
            return pd.DataFrame()

        print("User interactions data:", usersportinteraction)

        # Adjust weights for view_count and booking_count
        view_weight = 0.3
        booking_weight = 0.7

        usersportinteraction['interaction_score'] = usersportinteraction['view_count'] * view_weight + usersportinteraction['booking_count'] * booking_weight
        interaction_scores = usersportinteraction[['sport_id', 'interaction_score']].drop_duplicates().set_index('sport_id')

        interaction_scores = interaction_scores[~interaction_scores.index.duplicated(keep='first')]
        sportdetails['interaction_score'] = sportdetails['id'].map(interaction_scores['interaction_score']).fillna(0)

        vectorizer = CountVectorizer()
        sport_matrix = vectorizer.fit_transform(sportdetails['category'])
        similarity_matrix = cosine_similarity(sport_matrix)
        
        similarity_scores = similarity_matrix.dot(sportdetails['interaction_score'])
        scaler = MinMaxScaler()
        sportdetails['interaction_score'] = scaler.fit_transform(sportdetails[['interaction_score']])
        similarity_scores = scaler.fit_transform(similarity_scores.reshape(-1, 1)).flatten()

        sportdetails['similarity_score'] = similarity_scores
        content_recommendations = sportdetails.sort_values('similarity_score', ascending=False)

        content_scores = content_recommendations.set_index('id')['similarity_score']
        content_scores.name = 'content_score'
        return content_scores

    except Exception as e:
        print(f"Error in content_based_filtering: {e}")
        return pd.DataFrame()

# Function for Collaborative Filtering
def collaborative_filtering(user_id):
    try:
        interactions = UserSportInteraction.objects.values('user_id', 'sport_id', 'view_count', 'booking_count')
        if not interactions:
            print("No interactions found.")
            return pd.DataFrame()
        
        interaction_data = pd.DataFrame(list(interactions))
        user_item_matrix = interaction_data.pivot_table(
            index='user_id',
            columns='sport_id',
            values='booking_count',
            aggfunc='sum',
            fill_value=0
        )

        if user_item_matrix.shape[1] <= 1:
            print("User item matrix has less than or equal to 1 column.")
            return pd.DataFrame()

        print("User item matrix:\n", user_item_matrix)
        
        user_similarity = cosine_similarity(user_item_matrix)
        user_index = user_item_matrix.index.get_loc(user_id)
        user_similarity_scores = user_similarity[user_index]

        similar_users = user_item_matrix.index[user_similarity_scores.argsort()[::-1][1:]]
        collaborative_recommendations = user_item_matrix.loc[similar_users].mean(axis=0).sort_values(ascending=False)
        
        # Scaling the collaborative scores
        scaler = MinMaxScaler()
        collaborative_scores = scaler.fit_transform(collaborative_recommendations.values.reshape(-1, 1)).flatten()

        collaborative_scores = pd.Series(collaborative_scores, index=collaborative_recommendations.index, name='collaborative_score')

        print("Collaborative scores:", collaborative_scores)
        return collaborative_scores

    except Exception as e:
        print(f"Error in collaborative_filtering: {e}")
        return pd.DataFrame()

# Function for Hybrid Recommendation
def hybrid_recommendation(user_id, alpha=0.3):  # Adjust alpha for better balancing
    try:
        content_scores = content_based_filtering(user_id)
        collaborative_scores = collaborative_filtering(user_id)

        if content_scores.empty and collaborative_scores.empty:
            return fallback_recommendations()
        
        if content_scores.empty:
            content_scores = pd.Series(0, index=collaborative_scores.index, name='content_score')
        
        if collaborative_scores.empty:
            collaborative_scores = pd.Series(0, index=content_scores.index, name='collaborative_score')

        # Combine the scores with alpha weighting
        combined_scores = pd.concat([content_scores, collaborative_scores], axis=1).fillna(0)
        combined_scores['hybrid_score'] = (
            alpha * combined_scores['collaborative_score'] + (1 - alpha) * combined_scores['content_score']
        )

        recommendations = combined_scores.sort_values(by='hybrid_score', ascending=False)
        top_recommendations = recommendations.head(3)

        print("Combined scores:\n", combined_scores)
        print("Top recommendations:\n", top_recommendations)

        recommended_ids = top_recommendations.index.values
        sports_details = SportDetails.objects.filter(id__in=recommended_ids)

        sports_dict = {sport.id: sport for sport in sports_details}

        result = []
        for sport_id in recommended_ids:
            sport = sports_dict.get(sport_id)
            if sport:
                sport_images = sport.sport_images.all()
                images = [{"image": image.image.url} for image in sport_images]

                result.append({
                    "id": sport.id,
                    "name": sport.name,
                    "description": sport.description,
                    "price": sport.price,
                    "sport_images": images,
                    "sport_custom_id": sport.sport_custom_id,
                    "category": sport.category,
                    "location": sport.location
                })

        return result

    except Exception as e:
        print(f"Error in hybrid_recommendation: {e}")
        return []

# Function for fallback recommendations
def fallback_recommendations():
    sports = SportDetails.objects.annotate(
        total_bookings=Count('booking')
    ).order_by('-total_bookings', '-created_at')[:3]

    result = []
    for sport in sports:
        sport_images = sport.sport_images.all()
        images = [{"image": image.image.url} for image in sport_images]

        result.append({
            "id": sport.id,
            "name": sport.name,
            "description": sport.description,
            "price": sport.price,
            "sport_images": images,
            "sport_custom_id": sport.sport_custom_id,
            "category": sport.category,
            "location": sport.location
        })

    return result

# Function to get recommendations
def get_recommendations(user_id):
    try:
        user_exists = UserSportInteraction.objects.filter(user__id=user_id).exists()

        if not user_exists:
            return fallback_recommendations()

        return hybrid_recommendation(user_id)

    except Exception as e:
        print(f"Error in get_recommendations: {e}")
        return []
