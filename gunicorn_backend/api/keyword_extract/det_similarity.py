import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from flask import jsonify

def get_similarities(speech_keywords, lyrics_keywords):
    
    # Load pre-trained model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Get embeddings for all speech keywords
    speech_embeddings = np.array([model.encode(speech_kw[0]) for speech_kw in speech_keywords])

    # Get embeddings for all lyrics keywords
    lyrics_embeddings = np.array([model.encode(lyrics_kw[0]) for lyrics_kw in lyrics_keywords])

    # Calculate cosine similarity between all pairs of embeddings
    similarity_matrix = cosine_similarity(speech_embeddings, lyrics_embeddings)
    
    # Flatten the similarity matrix to calculate overall similarity
    flat_similarity = similarity_matrix.flatten()

    # Calculate the overall similarity percentage
    overall_similarity_percentage = np.mean(flat_similarity) * 100
    
    # Get Similarity Dictionary
    similarity_scores = []
    for i, speech_kw in enumerate(speech_keywords):
        for j, lyrics_kw in enumerate(lyrics_keywords):
            similarity_scores.append((speech_kw[0], lyrics_kw[0], similarity_matrix[i, j]))

    data_dict = {}

    # Loop through the similarity scores and organize them by id
    for id1, id2, similarity in similarity_scores:
        if id1 not in data_dict:
            data_dict[id1] = []

        data_dict[id1].append({'x': id2, 'y': float(similarity)})

    # Convert the dictionary to a list of objects
    formatted_data = [{'id': key, 'data': value} for key, value in data_dict.items()]

    return jsonify({
        "percentage": float(overall_similarity_percentage),
        "result_list_def": formatted_data
    })
   
# Test Case 
# speech_keywords1 = [('night sky', 0.544),
# ('mountain yesterday', 0.478),
# ('heavenly view', 0.471),
# ('many stars', 0.449),
# ('heart', 0.218)
# ]

# lyrics_keywords1 = [('cold nights', 0.282), ('love', 0.221)]

# print(get_similarities(speech_keywords1, lyrics_keywords1))