from django.db.models import Q, Count, Avg
from .models import SportDetails, UserSportInteraction, Booking
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

import pandas as pd


def build_content_based_score():
    """
    Calculate content-based scores using cosine similarity.
    Features: category, price, location, description.
    """
    # Fetch sports data
    sports = SportDetails.objects.values('id', 'category', 'price', 'location', 'description')

    # Convert to DataFrame
    sport_data = pd.DataFrame(list(sports))

    if sport_data.empty:
        return pd.DataFrame()  
    
    # Process categorical fields (category and location) using one-hot encoding
    sport_data = pd.get_dummies(sport_data, columns=['category', 'location'])

    # Convert textual descriptions into numeric features using a simple word count
    sport_data['description_length'] = sport_data['description'].apply(lambda x: len(str(x).split()))

    # Normalize price and description length to scale them between 0 and 1
    sport_data['price'] = sport_data['price'] / sport_data['price'].max()
    sport_data['description_length'] = sport_data['description_length'] / sport_data['description_length'].max()

    # Prepare feature matrix
    feature_matrix = sport_data.drop(columns=['id', 'description'])
    # Compute cosine similarity
    similarity_matrix = cosine_similarity(feature_matrix)

    # Add similarity scores to DataFrame
    sport_data['content_score'] = similarity_matrix.mean(axis=1)

    return sport_data[['id', 'content_score']]


def build_collaborative_score(user_id):
    """
    Calculate collaborative filtering scores using matrix factorization (SVD).
    Features: view_count and booking_count.
    """
    # Fetch user interactions (view and booking counts)
    interactions = UserSportInteraction.objects.values('user_id', 'sport_id', 'view_count', 'booking_count')

    if not interactions:
        return pd.DataFrame()  # Return empty DataFrame if no interactions

    # Convert to DataFrame
    interaction_data = pd.DataFrame(list(interactions))
    # Create a user-item matrix (2D)
    user_item_matrix = interaction_data.pivot_table(
        index='user_id',
        columns='sport_id',
        values=['view_count', 'booking_count'],
        aggfunc='sum',
        fill_value=0
    )

    # Check if the matrix has at least two features
    if user_item_matrix.shape[1] <= 1:
        return pd.DataFrame()  # Return empty DataFrame if there is only one sport feature

    # Combine 'view_count' and 'booking_count' into a single column (interaction score)
    user_item_matrix['interaction_score'] = user_item_matrix[['view_count', 'booking_count']].sum(axis=1)

    # Ensure the interaction_score is 2D by selecting the right columns
    interaction_score_matrix = user_item_matrix[['interaction_score']].values

    # Check if the interaction score matrix has more than one column (feature)
    if interaction_score_matrix.shape[1] <= 1:
        return pd.DataFrame()  # Return empty DataFrame if there's not enough data for SVD

    # Perform SVD(Singular Value Decomposition) for collaborative filtering
    svd = TruncatedSVD(n_components=2)
    user_factors = svd.fit_transform(interaction_score_matrix)  # Fit on the 2D matrix
    item_factors = svd.components_.T
    predicted_matrix = np.dot(user_factors, item_factors)

    # Map predicted scores back to facility IDs
    predicted_scores = pd.DataFrame(
        predicted_matrix, index=user_item_matrix.index, columns=user_item_matrix.columns.droplevel()
    )

    # Check if the user_id is in the predicted scores
    if user_id in predicted_scores.index:
        user_scores = predicted_scores.loc[user_id].reset_index()
        user_scores.columns = ['id', 'collaborative_score']
        return user_scores

    return pd.DataFrame() 


def fallback_recommendations():
    """
    Handle cold-start scenarios by recommending the most popular and recently added sports.
    """
    # Fetch most popular and recently added facilities
    sports = SportDetails.objects.annotate(
        total_bookings=Count('booking')
    ).order_by('-total_bookings', '-created_at')[:5]

    result = []
    for sport in sports:
        # Get sport images for the sport using the related_name 'sport_images'
        sport_images = sport.sport_images.all()  # Corrected line
        images = [{"image": image.image.url} for image in sport_images]

        # Prepare the response structure with full details
        result.append({
            "id": sport.id,
            "name": sport.name,
            "description": sport.description,  # Add description
            "price": sport.price,  # Add price
            "sport_images": images,  # Add images
            "sport_custom_id": sport.sport_custom_id,  # Add sport_custom_id
            "category": sport.category,  # Add category
            "location": sport.location  # Add location
        })

    # Return the structured response as per the required format
    return result


def hybrid_recommendation(user_id, alpha=0.5):
    """
    Combine content-based and collaborative filtering scores to generate hybrid recommendations.
    """
    # Get content-based and collaborative scores
    content_scores = build_content_based_score()
    collaborative_scores = build_collaborative_score(user_id)

    # Merge scores on the sport ID
    if not content_scores.empty and not collaborative_scores.empty:
        combined_scores = pd.merge(content_scores, collaborative_scores, on='id', how='outer').fillna(0)

        # Compute the hybrid score
        combined_scores['hybrid_score'] = (
            alpha * combined_scores['collaborative_score'] + (1 - alpha) * combined_scores['content_score']
        )

        # Sort by hybrid score and get top 3 recommendations
        recommendations = combined_scores.sort_values(by='hybrid_score', ascending=False)
        top_recommendations = recommendations.head(3)

        # Fetch the details for the top 3 recommendations
        sports_details = SportDetails.objects.filter(id__in=top_recommendations['id'].values)
        result = []
        for sport in sports_details:
            # Get sport images for the sport
            sport_images = sport.sport_images.all()
            images = [{"image": image.image.url} for image in sport_images]

            # Prepare the response structure with full details
            result.append({
                "id": sport.id,
                "name": sport.name,
                "description": sport.description,  # Add description
                "price": sport.price,  # Add price
                "sport_images": images,  # Add images
                "sport_custom_id": sport.sport_custom_id,  # Add sport_custom_id
                "category": sport.category,  # Add category
                "location": sport.location  # Add location
            })

        # Return the full details of the recommended sports
        return result
    

    # If either score is missing, fallback to popular/recent recommendations
    return fallback_recommendations()


def get_recommendations(user_id):
    """
    Main function to fetch recommendations for a given user.
    """
    # Check if the user exists in interactions
    user_exists = UserSportInteraction.objects.filter(user__id=user_id).exists()

    if not user_exists:
        # If no interactions, return fallback recommendations
        return fallback_recommendations()

    # Generate hybrid recommendations
    return hybrid_recommendation(user_id)