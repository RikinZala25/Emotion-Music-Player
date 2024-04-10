import numpy as np

def get_va_distance_similarity(text_va, lyrics_arousal, lyrics_valence):
    
    distance = np.sqrt((text_va['arousal'] - lyrics_arousal)**2 + (text_va['valence'] - lyrics_valence)**2)

    # Define parameters for the sigmoid function
    alpha = 10  # Adjust the slope of the sigmoid function
    beta = 0.5  # Adjust the midpoint of the sigmoid function

    # Calculate the similarity percentage using a sigmoid function
    similarity_percentage = 100 / (1 + np.exp(alpha * (distance - beta)))

    return distance, similarity_percentage