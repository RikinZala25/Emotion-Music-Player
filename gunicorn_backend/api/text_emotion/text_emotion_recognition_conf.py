import pickle
import tensorflow as tf
from flask import jsonify

# load models
loaded_model = None
tokenizer = None
encoder = None

def load_emc_model():
    global loaded_model, tokenizer, encoder
    
    # load the saved H5 model
    loaded_model = tf.keras.models.load_model("models/txt_em_conf_model/nlp_model.h5", compile=False)

    # Load tokenizer
    with open('models/txt_em_conf_model/tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)

    # Load encoder
    with open('models/txt_em_conf_model/encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)

def recognize_text_emotion_confidence(input_text): 
    # load the model
    load_emc_model()
    
    if loaded_model is None or tokenizer is None or encoder is None:
        return jsonify({'error': 'Model not loaded yet. Try again later.'}), 500

    # Use the correct reference to loaded_model
    sequences = tokenizer.texts_to_sequences([input_text])
    x_new = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=50)
    
    # Use loaded_model instead of model
    predictions = loaded_model.predict([x_new, x_new])

    emotion_conf_results = []

    for label, conf in zip(encoder.classes_, predictions[0]):
        conf = float(conf)
        emotion_conf_results.append({'label': label, 'value': conf})
        
    return jsonify(emotion_conf_results)

# Test Case
# mytext = "we run up the mountain yesterday the night sky was full of stars I've never seen so many stars in the sky before it was such a heavenly view forever remeber it in the bottom of my heart"
# ans1 = recognize_text_emotion_confidence(mytext)
# print(ans1)