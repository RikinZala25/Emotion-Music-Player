import requests
from flask import jsonify

def get_lyrics_api1(artist_name, song_name):
    url = 'https://api.lyrics.ovh/v1/'+artist_name.replace(' ', '%20')+'/'+song_name.replace(' ', '%20')

    response = requests.get(url)

    if response.status_code == 200:
        lyrics = response.json().get('lyrics')  # Use .get() to avoid KeyError
        if lyrics:
            # Split the lyrics by newline character and remove the first line
            lyrics_lines = lyrics.split('\n')[1:]
            # Join the remaining lines back together
            cleaned_lyrics = '\n'.join(lyrics_lines)
            return jsonify(cleaned_lyrics)
        else:
            return None  # Return None when lyrics are not available
    else:
        return None
    
# Test Case
# lyrics = get_lyrics_api1(artist_name="NF", song_name="The Search")
# print(lyrics)