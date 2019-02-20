from texteval import process_file

if __name__ == '__main__':
    data = process_file('ema.tal')

    nb_pro_total = 0
    index_phrase = 0
    for sentence in data:
        nb_pro_by_sentence = 0
        for word in sentence:     
            if word.pos.startswith('PRO'):
                nb_pro_by_sentence += 1
        if nb_pro_by_sentence > 0:
            print('Phrase', index_phrase, ': ', nb_pro_by_sentence, ' PRO')
            nb_pro_total += nb_pro_by_sentence
        index_phrase += 1

    print(f'Total pronoms {nb_pro_total:10d}')
    print(f'Total phrases {index_phrase:10d}')
    print('Moyenne pronoms / phrases', f"{(nb_pro_total / index_phrase):.3f}")
