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

def get_keyword_rec_songs(keyword, predicted_emotion):
    
    # Authorize Spotify
    sp = authorize_spotify()
    
    generatedAPIResponse = sp.search(keyword, limit=10, offset=0, type='track', market='US')
    
    # Get the Structured Output
    track_info_list = get_structured_output(sp, generatedAPIResponse, itemsHierarcy=True)
    
    # Get the top 2 filtered Outputs
    top_2_tracks = getFilteredOutputs(track_info_list, predicted_emotion, 2)
    
    return jsonify(top_2_tracks)

# Test Case
# predicted_emotion = "Happiness"
# input_keyword = "Cold Nights"
# rec_songs = get_keyword_rec_songs(input_keyword, predicted_emotion)
# print(rec_songs)