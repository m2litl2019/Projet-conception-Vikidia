from texteval import load

DEBUG = False

def reperage_pronoms(target, debug=DEBUG):
    data = load(target)
    nb_pro_total = 0
    index_phrase = 0
    freq_pro = {}
    for sentence in data:
        nb_pro_by_sentence = 0
        for word in sentence:     
            if word.pos.startswith('PRO') or word.pos.startswith("CL"):
                nb_pro_by_sentence += 1
                freq_pro[word.pos] = freq_pro.get(word.pos,0) + 1
        if nb_pro_by_sentence > 0:
            if debug:
                print('Phrase', index_phrase, ': ', nb_pro_by_sentence, ' PRO')
            nb_pro_total += nb_pro_by_sentence
        index_phrase += 1
    print('reperage_pronoms on', target)
    print(f'Total pronoms : {nb_pro_total:10d}')
    print(f'Total phrases : {index_phrase:10d}')
    print('Moyenne pro / ph :  ', f"{(nb_pro_total / index_phrase):.3f}")
    for key in freq_pro:
        print(key," : ",f"{freq_pro[key]/nb_pro_total:.3f}")

if __name__ == '__main__':
    reperage_pronoms('ema.tal')
