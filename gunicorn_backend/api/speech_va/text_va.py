import os
import sys
import numpy as np
import pandas as pd
from flask import jsonify

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory of the 'api' package to the Python path
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

# Emotion Calculator API
from emotion_calculator.det_quadrant_angle import calculate_angle, determine_quadrant, determine_emotion, reverse_calculate_angle

# load vad_scores
vad_scores = None

def load_vad_csv():
    global vad_scores
    
    vad_scores = pd.read_csv("models/vad-nrc-csv/NRC-VAD-Lexicon_Bipolar.csv", index_col='Word')
    
def recognize_text_valence_arousal_avg(input_text, predicted_emotion):
    
    # load the csv
    load_vad_csv()
    
    if vad_scores is None:
        return jsonify({'error': 'vad_scores csv not loaded yet. Try again later.'}), 500
    
    word_count, position = 0, 0
    cumulative_vad = np.zeros([2,])

    for word in input_text.split(' '):
        polarity = 1 

        negation_terms = ['no', 'not', 'n\'t']
        if word in vad_scores.index and any(term in input_text.split(' ')[position-6:position] for term in negation_terms):
            polarity = -1

        if word in vad_scores.index:
            cumulative_vad[:2] += vad_scores.loc[word][:2] * polarity
            word_count += 1

        position += 1 

    average_vad = cumulative_vad / word_count if word_count > 0 else np.zeros([3,])

    labels = ['valence', 'arousal']
    result_dict = {label: avg for label, avg in zip(labels, average_vad)}
    
    # Determine angle
    angle_deg = calculate_angle(arousal=result_dict['arousal'], valence=result_dict['valence'])

    # Determine quadrant
    quadrant = determine_quadrant(angle_deg=angle_deg)

    # Determine emotion
    va_emotion = determine_emotion(quadrant_name=quadrant)
    
    # Cross-check VA with emotions
    if va_emotion != predicted_emotion:
        
        emotion_to_angle = {
            'Happiness': 15,
            'Sadness': 210,
            'Calmness': 305,
            'Anger': 105
        }

        angle = emotion_to_angle.get(predicted_emotion)
        
        if angle is not None:
            result_dict['arousal'], result_dict['valence'] = reverse_calculate_angle(angle)
        
        else:
            return "Handle default case"
    
    return jsonify(result_dict)

# Test Case
# mytext = "we run up the mountain yesterday the night sky was full of stars I've never seen so many stars in the sky before it was such a heavenly view forever remeber it in the bottom of my heart"
# pred_emo = "Happiness"
# ans1 = recognize_text_valence_arousal_avg(mytext, pred_emo)
# print(ans1)