# In your script (e.g., emotion_recommendation_songs.py)
import sys
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory of the 'api' package to the Python path
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

# Emotion Calculator API
from emotion_calculator.det_quadrant_angle import calculate_angle, determine_quadrant, determine_emotion

# Lyrics API
from lyrics_api.lyrics_ovh import get_lyrics_api1
from lyrics_api.musicmatch_lyrics import get_lyrics_api2

def get_structured_output(sp, api_response, itemsHierarcy):
    
    # Number of limits specified
    limit = 30

    # List to store track information
    track_info_list = []
    
    if itemsHierarcy:
        gen_api_response = api_response["tracks"]["items"]
    else:
        gen_api_response = api_response["tracks"]
        
    # Function to get lyrics dynamically from APIs
    def get_lyrics(artists_names, song_name):
        for artist_name in artists_names:
            lyrics_api1 = get_lyrics_api1(artist_name=artist_name, song_name=song_name)
            if lyrics_api1 is not None:
                return lyrics_api1.json
        
        # If no lyrics are found with API 1, try API 2
        for artist_name in artists_names:
            lyrics_api2 = get_lyrics_api2(artist_name=artist_name, song_name=song_name)
            if lyrics_api2 is not None:
                return lyrics_api2.json
        
        return None

    for i in range(min(limit, len(gen_api_response))):
        track_info = {}
        track = gen_api_response[i]

        # Extracting track ID and name
        track_info['id'] = track['id']
        track_info['name'] = track['name']

        # Extracting artists' names
        track_info['artists'] = [artist['name'] for artist in track['artists']]

        # Extracting images details
        track_info['images'] = track['album']['images']

        # Extracting preview URL if available
        track_info['preview_url'] = track['preview_url']
        
        # Extract the track features
        track_features = sp.audio_features(track['id'])
        track_info['arousal'] = 2 * track_features[0]['energy'] - 1
        # track_info['danceability'] = track_features[0]['danceability']
        # track_info['acousticness'] = track_features[0]['acousticness']
        track_info['valence'] = 2 * track_features[0]['valence'] - 1

        # Extract track URL
        track_info['track_url'] = track['external_urls']['spotify']

        # Check if all fields are filled and preview_url is not "[No preview url found]"
        if all(track_info.values()) and track_info['preview_url'] != "No preview url found":
            # Calculate angle
            track_info['angle_deg'] = calculate_angle(arousal=track_info['arousal'], valence=track_info['valence'])

            # Determine quadrant
            track_info['quadrant'] = determine_quadrant(angle_deg=track_info['angle_deg'])

            # Determine emotion
            track_info['emotion'] = determine_emotion(quadrant_name=track_info['quadrant'])
            
            track_info['lyrics'] = get_lyrics(track_info['artists'], track_info['name'])
            
            if track_info['lyrics'] != None:
                # Append track information to the list
                track_info_list.append(track_info)
    
    return track_info_list