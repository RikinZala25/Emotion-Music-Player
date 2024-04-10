import sys
import os
from flask import jsonify

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory of the 'api' package to the Python path
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

# Spotipy Auth
from spotipy_api.spotipy_auth import authorize_spotify

# Structure API Output
from spotipy_api.structure_api_output import get_structured_output

# Get Filtered Outputs
from spotipy_api.filter_structure_output import getFilteredOutputs

def get_emotion_rec_songs(predicted_emotion):
    
    # Authorize Spotify
    sp = authorize_spotify()
    
    # Define a dictionary to map emotions to genre seeds and target energy/valence
    emotion_genre_map = {
        "Happiness": {
            "genres": ['dance', 'disco', 'happy', 'pop', 'reggae'],
            "energy": (0.5, 1.0, 0.8),
            "valence": (0.5, 1.0, 0.8)
        },
        "Sadness": {
            "genres": ['blues', 'emotional', 'indie-folk', 'soul', 'sad'],
            "energy": (0.1, 0.5, 0.3),
            "valence": (0.1, 0.5, 0.3)
        },
        "Anger": {
            "genres": ['hardcore', 'heavy-metal', 'punk', 'rock', 'grindcore'],
            "energy": (0.5, 1.0, 0.8),
            "valence": (0.1, 0.5, 0.3)
        },
        "Calmness": {
            "genres": ['acoustic', 'ambient', 'classical', 'piano', 'relaxation'],
            "energy": (0.1, 0.5, 0.3),
            "valence": (0.5, 1.0, 0.8)
        }
    }
    
    # Get the genre seeds and target energy/valence for the predicted emotion
    emotion_info = emotion_genre_map.get(predicted_emotion)
    
    if emotion_info:
        genres = emotion_info["genres"]
        energy = emotion_info["energy"]
        valence = emotion_info["valence"]
        
        generatedAPIResponse = sp.recommendations(
            seed_genres=genres,
            limit=20,
            country="US",
            locale="en_US",
            min_energy=energy[0],
            max_energy=energy[1],
            target_energy=energy[2],
            min_valence=valence[0],
            max_valence=valence[1],
            target_valence=valence[2]
        )
        
    else:
        # Handle invalid emotion
        generatedAPIResponse = {"error": "Invalid emotion"}
    
    # Get the Structured Output
    track_info_list = get_structured_output(sp, generatedAPIResponse, itemsHierarcy=False)

    # Get the top 5 filtered Outputs
    top_10_tracks = getFilteredOutputs(track_info_list, predicted_emotion, 10)
    
    return jsonify(top_10_tracks)

# Test Case
# predicted_emotion = "Happiness"
# rec_songs = get_emotion_rec_songs(predicted_emotion)
# print(rec_songs)