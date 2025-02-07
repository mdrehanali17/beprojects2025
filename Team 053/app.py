import streamlit as st
import pickle
import emoji

# Load model
model = pickle.load(open('sentiment_analysis.pkl', 'rb'))

# Create title
st.title('Sentiment Analysis Model')

review = st.text_area('Enter your review:')

submit = st.button('Predict')

if submit:
    prediction = model.predict([review])

    # Define emojis for smileys
    if prediction[0] == 1:
        emoji_smiley = emoji.emojize(":smiley:")
        st.success(f'{emoji_smiley} Positive Review!!')
    else:
        emoji_sad = emoji.emojize(":disappointed:")
        st.error(f'{emoji_sad} Negative Review..')
