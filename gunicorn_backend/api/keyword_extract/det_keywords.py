from keybert import KeyBERT
from flask import jsonify

def get_keywords(input_text, text_type):
    
    # Initialize KeyBERT model
    kw_model = KeyBERT()
    
    # Determine the number of keywords to extract based on the text type
    top_n_keywords = 2 if text_type == "lyrics_keywords" else 5
    
    # Extract keywords using KeyBERT
    extracted_keywords = kw_model.extract_keywords(
        input_text, 
        keyphrase_ngram_range=(1, 2), 
        stop_words='english', 
        use_mmr=True, 
        diversity=0.3,
        top_n=top_n_keywords
    )
       
    return jsonify(extracted_keywords)

# Test Case
# mytext = "we run up the mountain yesterday the night sky was full of stars I've never seen so many stars in the sky before it was such a heavenly view forever remeber it in the bottom of my heart"
# print(get_keywords(mytext, text_type="speech_keywords"))

# song_lyrics = '''
# I watch 'em all pass by
# The moon and the stars
# Let me hold you in my arms forevermore
# These cold nights, the park is ours
# Standing by the side
# Let you go, oh to the sea, just for me
# Don't ever let me, my love
# Keep holding on
# Let the modest go
# As my mic goes to and fro
# Waking up for one more show
# We see him in the night
# Tell him I'm not afraid of him
# I'm not afraid of him
# 'Cause I won't know
# '''
# print(get_keywords(song_lyrics, text_type="lyrics_keywords"))