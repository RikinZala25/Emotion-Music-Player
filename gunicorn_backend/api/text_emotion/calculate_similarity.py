def calculate_similarity_conf(text_em_conf, lyrics_em_conf):
    total_difference = 0.0

    num_labels = len(text_em_conf)

    for i in range(num_labels):
        label1 = text_em_conf[i]['label']
        confidence1 = text_em_conf[i]['value']

        label2 = lyrics_em_conf[i]['label']
        confidence2 = lyrics_em_conf[i]['value']

        if label1 == label2:
            total_difference += abs(confidence1 - confidence2)

    similarity = (1 - total_difference / num_labels) * 100
    return similarity