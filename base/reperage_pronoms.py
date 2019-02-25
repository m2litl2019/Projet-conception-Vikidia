from texteval import load

DEBUG = False

def reperage_pronoms(target, debug=DEBUG):
    data = load(target)
    nb_pro_total = 0
    index_phrase = 0
    for sentence in data:
        nb_pro_by_sentence = 0
        for word in sentence:     
            if word.pos.startswith('PRO'):
                nb_pro_by_sentence += 1
        if nb_pro_by_sentence > 0:
            if debug:
                print('Phrase', index_phrase, ': ', nb_pro_by_sentence, ' PRO')
            nb_pro_total += nb_pro_by_sentence
        index_phrase += 1
    print('reperage_pronoms on', target)
    print(f'Total pronoms : {nb_pro_total:10d}')
    print(f'Total phrases : {index_phrase:10d}')
    print('Moyenne pro / ph :  ', f"{(nb_pro_total / index_phrase):.3f}")

if __name__ == '__main__':
    reperage_pronoms('ema.tal')
