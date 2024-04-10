from flask import jsonify
import pickle
import librosa
import numpy as np
import tensorflow as tf

# load models
loaded_model = None
scaler = None
encoder = None

def load_ser_model():
    global loaded_model, scaler, encoder
    
    # Load the JSON model architecture
    json_file = open('models/audio_ser_model/CNN_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    # load weights
    loaded_model = tf.keras.models.model_from_json(loaded_model_json)
    loaded_model.load_weights("models/audio_ser_model/best_model_weights.h5")

    # Load tokenizer
    with open('models/audio_ser_model/scaler.pickle', 'rb') as f:
        scaler = pickle.load(f)

    # Load encoder
    with open('models/audio_ser_model/encoder.pickle', 'rb') as f:
        encoder = pickle.load(f)
        
def zcr(data,frame_length,hop_length):
        zcr=librosa.feature.zero_crossing_rate(data,frame_length=frame_length,hop_length=hop_length)
        return np.squeeze(zcr)

def rmse(data,frame_length=2048,hop_length=512):
    rmse=librosa.feature.rms(y=data,frame_length=frame_length,hop_length=hop_length)
    return np.squeeze(rmse)

def mfcc(data, sr, frame_length=2048, hop_length=512, flatten=True):
    mfcc_result = librosa.feature.mfcc(y=data, sr=sr, n_fft=frame_length, hop_length=hop_length)
    return np.squeeze(mfcc_result.T) if not flatten else np.ravel(mfcc_result.T)

def extract_features(data,sr=22050,frame_length=2048,hop_length=512):
    result=np.array([])

    result=np.hstack((
    result,
    zcr(data,frame_length,hop_length),
    rmse(data,frame_length,hop_length),
    mfcc(data,sr,frame_length,hop_length)
    ))

    return result

def get_predict_feat(path, expected_shape=(1, 2376)):
    d, s_rate = librosa.load(path, duration=2.5, offset=0.6)
    res = extract_features(d)

    # Ensure res is reshaped or padded to match the expected shape
    if res.shape != expected_shape:
        flat_size = np.prod(expected_shape)
        if res.size < flat_size:
            # Pad if the size is smaller than expected
            pad_width = (0, flat_size - res.size)
            res = np.pad(res, pad_width=pad_width, mode='constant')
        else:
            # Resize if the size is larger than expected
            res = np.resize(res, expected_shape)

    i_result = scaler.transform(res.reshape(1, -1))
    final_result = np.expand_dims(i_result, axis=2)

    return final_result

def recognize_audio_emotion(input_path):
    # Load the audio model
    load_ser_model()

    if loaded_model is None or scaler is None or encoder is None:
        return {'error': 'Model not loaded yet. Try again later.'}, 500
    
    res = get_predict_feat(input_path)
    predictions = loaded_model.predict(res)

    # Get the label names or define them if available
    label_names = list(encoder.categories_[0])

    # List to store confidence scores
    confidence_scores = []

    # Display predicted emotion and confidence for each label
    for label_index, label_name in enumerate(label_names):
        confidence_score = predictions[0][label_index]
        confidence_score = 0 if confidence_score < 0.001 else confidence_score

        confidence_scores.append({'label': label_name, 'confidence': confidence_score})
   
    # Convert float32 values to native Python floats
    confidence_scores = [{'label': item['label'], 'value': float(item['confidence'])} for item in confidence_scores]
    
    # Return results
    return jsonify({'confidence_scores': confidence_scores})