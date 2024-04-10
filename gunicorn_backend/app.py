import sys
import os
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from flask_cors import CORS

# Add the 'project' directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Audio Emotion
from api.acoustic_ser.audio_emotion_recognition import recognize_audio_emotion

# Emotion Calculator
from api.emotion_calculator.det_quadrant_angle import get_quadrant_angle

# Keyword Extract Analysis
from api.keyword_extract.det_keywords import get_keywords
from api.keyword_extract.det_similarity import get_similarities

# Lyrics API
from api.lyrics_api.lyrics_ovh import get_lyrics_api1
from api.lyrics_api.musicmatch_lyrics import get_lyrics_api2

# Music Generation
from api.music_generation.emopia_cls import generate_music

# Speech Valence Arousal
from api.speech_va.text_va import recognize_text_valence_arousal_avg
from api.speech_va.va_similarity import get_va_distance_similarity

# Spotipy API
from api.spotipy_api.emotion_recommendation_songs import get_emotion_rec_songs
from api.spotipy_api.keyword_recommendation_songs import get_keyword_rec_songs

# Text Emotion
from api.text_emotion.speech_to_text import transcribe_text
from api.text_emotion.text_emotion_recognition_conf import recognize_text_emotion_confidence
from api.text_emotion.calculate_similarity import calculate_similarity_conf

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
CORS(app)

# CORS Headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/generate_audio_music", methods=['POST'])
def generate_audio_music():
    
    emotion = request.args.get('emotion')
    
    return jsonify(generate_music(emotion).json)

@app.route("/recommend_music", methods=['POST'])
def recommend_music():

    # Check if a file was uploaded in the request
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['audio_file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Check if the file has an allowed extension
    if not allowed_file(file.filename):
        return jsonify({'error': 'File extension not allowed'})

    # Save the uploaded file to the upload folder
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Recognize audio emotion
    get_audio_emotion = recognize_audio_emotion(filepath).json
    
    # Transcribe text
    get_text = transcribe_text(filepath)
    
    # Initialize text emotion outputs
    get_text_emotion_conf = None

    # If text transcription is successful, proceed with text emotion recognition
    if get_text:
        get_text_emotion_conf = recognize_text_emotion_confidence(get_text).json
        
    # Calculate means for confidence scores
    confidence_means = {}

    # Combine confidence scores from both audio and text emotion data
    all_confidence_scores = get_audio_emotion['confidence_scores'] + get_text_emotion_conf

    # Calculate means
    for entry in all_confidence_scores:
        label = entry['label']
        confidence = entry['value']
        if label in confidence_means:
            confidence_means[label].append(confidence)
        else:
            confidence_means[label] = [confidence]

    for label, confidences in confidence_means.items():
        confidence_means[label] = sum(confidences) / len(confidences)

    predicted_emotion, highest_confidence = max(confidence_means.items(), key=lambda x: x[1])
    
    input_text_va = recognize_text_valence_arousal_avg(get_text, predicted_emotion).json
    
    emotion_quadrant_angle = get_quadrant_angle(input_text_va['arousal'], input_text_va['valence']).json
    
    generate_keywords_from_input = get_keywords(get_text, text_type="speech_keywords").json
    
    # Extract keywords to search
    keywords_to_search = [item[0] for item in generate_keywords_from_input]

    # Initialize a list to store all songs
    final_song_list = []

    # Iterate over keywords and retrieve songs
    for keyword in keywords_to_search:
        songs = get_keyword_rec_songs(keyword, predicted_emotion).json
        final_song_list.extend(songs)
        
    final_song_list.extend(get_emotion_rec_songs(predicted_emotion).json)
    
    # Add these fields to each song object in final_song_list
    for song in final_song_list:
        song['lyrics_emotion_confidence'] = None
        song['lyrics_keywords'] = None
        song['keyword_similarity_score'] = None
        song['text_similary'] = None
        song['distance'] = None
        song['acoustic_similarity'] = None
        song['semantics_similarity'] = None
        song['overall_similarity'] = None
        
        if song['lyrics'] is not None:
            lyrics_text = song['lyrics'].replace('\n', '')
            song['lyrics_emotion_confidence'] = recognize_text_emotion_confidence(lyrics_text).json
            song['lyrics_keywords'] = get_keywords(lyrics_text, text_type="lyrics_keywords").json
            song['keyword_similarity_score'] = get_similarities(generate_keywords_from_input, song['lyrics_keywords']).json
            song['text_similary'] = calculate_similarity_conf(get_text_emotion_conf, song['lyrics_emotion_confidence'])
            song['distance'], song['acoustic_similarity'] = get_va_distance_similarity(input_text_va, song['arousal'], song['valence'])
            song['semantics_similarity'] = song['keyword_similarity_score']['percentage']
            song['overall_similarity'] = (song['text_similary'] + song['acoustic_similarity'] + song['semantics_similarity'] ) / 3
    
    # Sort final_song_list by overall_similarity in descending order
    final_song_list_sorted = sorted(final_song_list, key=lambda x: x['overall_similarity'], reverse=True)
      
    # Construct the response dictionary
    response = {
        "audio_emotion": get_audio_emotion,
        "detected_text": get_text,
        "text_emotion_confidence": get_text_emotion_conf,
        "final_prediction": {'label': predicted_emotion, 'value': highest_confidence},
        "text_va": input_text_va,
        "emotion_quadrant_angle": emotion_quadrant_angle,
        "input_text_keywords": generate_keywords_from_input,
        "suggested_songs": final_song_list_sorted,
    }
    
    # Delete the file after processing
    os.remove(filepath)

    # Return the response dictionary
    return jsonify(response)

if __name__ == "__main__":
    app.run()