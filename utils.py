def reconstruct_abstract(inverted_index):
    if not inverted_index: return "No Abstract."
    word_list = []
    for word, positions in inverted_index.items():
        for pos in positions: word_list.append((pos, word))
    word_list.sort()
    return " ".join([w for _, w in word_list])