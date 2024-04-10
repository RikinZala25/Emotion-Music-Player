import numpy as np
from flask import jsonify

def calculate_angle(arousal, valence):
            
    # Calculate the angle in radians
    angle_rad = np.arctan2(arousal, valence)
    
    # Convert radians to degrees
    angle_deg = np.degrees(angle_rad)
    
    # Ensure angle is positive
    if angle_deg < 0:
        angle_deg += 360
        
    return angle_deg

def determine_quadrant(angle_deg):
    if 0 <= angle_deg < 90:
        return "QUAD1"
    elif 90 <= angle_deg < 180:
        return "QUAD2"
    elif 180 <= angle_deg < 270:
        return "QUAD3"
    else:
        return "QUAD4"

def determine_emotion(quadrant_name):
    if quadrant_name == "QUAD1":
        return "Happiness"
    elif quadrant_name == "QUAD2":
        return "Anger"
    elif quadrant_name == "QUAD3":
        return "Sadness"
    else:
        return "Calmness"
    
def reverse_calculate_angle(angle_deg):
    angle_deg %= 360

    angle_rad = np.radians(angle_deg)
    
    arousal = np.sin(angle_rad)
    valence = np.cos(angle_rad)

    return arousal, valence
    
def get_quadrant_angle(arousal, valence):

    # Determine angle
    angle_deg = calculate_angle(arousal, valence)

    # Determine quadrant
    quadrant = determine_quadrant(angle_deg)

    # Determine emotion
    emotion = determine_emotion(quadrant)

    # Store the values in a dictionary
    result_dict = {
        'angle_deg': angle_deg,
        'quadrant': quadrant,
        'emotion': emotion
    }

    return jsonify(result_dict)
    
# Test Case  
# print(get_quadrant_angle(0.4043076923076923 , 0.7255384615384616))
# print(get_quadrant_angle(0.4043076923076923 , 0.7255384615384616))