import os
from dotenv import load_dotenv
from flask import jsonify

import replicate as replicate_module

def generate_music(predicted_emotion):
    
    load_dotenv()
    replicate = replicate_module.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

    va_value = "High valence, high arousal"
    
    if predicted_emotion == "Happiness":
        va_value = "High valence, high arousal"
    elif predicted_emotion == "Anger":
        va_value = "Low valence, high arousal"
    elif predicted_emotion == "Sadness":
        va_value = "Low valence, low arousal"
    elif predicted_emotion == "Calmness":
        va_value = "High valence, low arousal"

    output = replicate.run(
        "annahung31/emopia:ad93577dbfe239c7604a49495ac579176157bb2a6f5fa1e0906433fd7acff792",
        input={
            "emotion": va_value
        }
    )
    
    # Store the values in a dictionary
    result_dict = {
        'generated_song': output,
        'va_value': va_value
    }

    return jsonify(result_dict)