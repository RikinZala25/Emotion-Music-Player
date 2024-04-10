import numpy as np

def getFilteredOutputs(track_info_list, predicted_emotion, numOfOutput):
    
    # Filter tracks by predicted emotion
    filtered_tracks = [track for track in track_info_list if track['emotion'] == predicted_emotion]

    # If the length of filtered_tracks is less than 5, include tracks with other emotions
    if len(filtered_tracks) < 5:
        other_tracks = [track for track in track_info_list if track['emotion'] != predicted_emotion]
        filtered_tracks += other_tracks[:5 - len(filtered_tracks)]

    # Sort tracks by their angle_deg
    filtered_tracks.sort(key=lambda track: track['angle_deg'])

    # Calculate the mean of angles in filtered tracks using NumPy
    mean_angle = np.mean([track['angle_deg'] for track in filtered_tracks])

    # Sort tracks by their angle difference from the mean angle using NumPy
    sorted_indices = np.argsort(np.abs([track['angle_deg'] - mean_angle for track in filtered_tracks]))

    # Get the top n tracks with angles closest to the mean angle
    top_n_tracks = [filtered_tracks[i] for i in sorted_indices[:numOfOutput]]
    
    return top_n_tracks