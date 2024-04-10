import os
from dotenv import load_dotenv
import requests
from flask import jsonify

# musixmatch api base url
base_url = "https://api.musixmatch.com/ws/1.1/"

# api methods
a1 = lyrics_matcher = "matcher.lyrics.get"
a2 = lyrics_track_matcher = "track.lyrics.get"
a3 = track_matcher = "matcher.track.get"
a4 = subtitle_matcher = "matcher.subtitle.get"
a5 = track_search = "track.search"
a6 = artist_search = "artists.search"
a7 = album_tracks = "album.tracks.get"
a8 = track_charts = "chart.tracks.get"
a9 = artist_charts = "chart.artists.get"
a10 = related_artists = "artist.related.get"
a11 = artist_album_getter = "artist.albums.get"
a12 = track_getter = "track.get"
a13 = artist_getter = "artist.get"
a14 = album_getter = "album.get"
a15 = subtitle_getter = "track.subtitle.get"
a16 = snippet_getter = "track.snippet.get"
api_methods = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16]

# format url
format_url = "?format=json&callback=callback"

# parameters
p1 = artist_search_parameter = "&q_artist="
p2 = track_search_parameter = "&q_track="
p3 = track_id_parameter = "&track_id="
p4 = artist_id_parameter = "&artist_id="
p5 = album_id_parameter = "&album_id="
p6 = has_lyrics_parameter = "&f_has_lyrics="
p7 = has_subtitle_parameter = "&f_has_subtitle="
p8 = page_parameter = "&page="
p9 = page_size_parameter = "&page_size="
p10 = word_in_lyrics_parameter = "&q_lyrics="
p11 = music_genre_parameter = "&f_music_genre_id="
p12 = music_language_parameter = "&f_lyrics_language="
p13 = artist_rating_parameter = "&s_artist_rating="
p14 = track_rating_parameter= "&s_track_rating="
p15 = quorum_factor_parameter = "&quorum_factor="
p16 = artists_id_filter_parameter = "&f_artist_id="
p17 = country_parameter = "&country="
p18 = release_date_parameter = "&s_release_date="
p19 = album_name_parameter = "&g_album_name="
paramaters = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19]

# arrays with paramaters for each method
x1 = lyrics_matcher_parameters = [p1,p2]
x2 = lyrics_track_matcher_parameters = [p3]
x3 = track_matcher_parameters = [p1,p2,p6,p7]
x4 = subtitle_matcher_parameters = [p1,p2]
x5 = track_search_paramaters = [p1,p2,p10,p4,p11,p12,p12,p14,p15,p8,p9]
x6 = artist_search_parameters = [p1,p16,p8,p9]
x7 = album_tracks_parameters = [p5,p6,p8,p9]
x8 = track_charts_paramaters = [p8,p9,p17,p6]
x9 = artist_charts_parameters = [p8,p9,p17]
x10 = related_artists_parameters = [p4,p8,p9]
x11 = artists_album_getter_paramaters = [p4,p18,p19,p8,p9]
x12 = track_getter_parameters = [p3]
x13 = artist_getter_parameters = [p4]
x14 = album_getter_parameters = [p5]
x15 = subtitle_getter_parameters = [p3]
x16 = snippet_getter_parameters = [p3]
paramater_lists = [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16]

def get_lyrics_api2(artist_name, song_name):
    load_dotenv()
    api_key = os.environ['MUSICMATCH_API_KEY']
    
    url = base_url + lyrics_matcher + format_url + artist_search_parameter + artist_name.replace(' ', '%20') + track_search_parameter + song_name.replace(' ', '%20') + '&apikey=' + api_key

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Check if the response contains the expected structure
        if 'message' in data and 'body' in data['message'] and 'lyrics' in data['message']['body']:
            lyrics = data['message']['body']['lyrics']
            
            # Check if 'lyrics' is not empty
            if lyrics:
                # Access the 'lyrics_body' attribute
                lyrics_body = lyrics['lyrics_body']
                if lyrics_body:
                    # Split the lyrics by newline character
                    lyrics_lines = lyrics_body.split('\n')
                    
                    # Exclude the last 4 lines
                    cleaned_lyrics_lines = lyrics_lines[:-4]
                    
                    # Join the remaining lines back together
                    cleaned_lyrics = '\n'.join(cleaned_lyrics_lines)
                
                    return jsonify(cleaned_lyrics)
        
        # Return None if the structure is not as expected or if lyrics are empty
        return None
        
    else:
        return None
    
# Test Case
# lyrics = get_lyrics_api2(artist_name="Dub Inc", song_name="Rude Boy")
# print(lyrics)