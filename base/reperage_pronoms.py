from texteval import load, Part

def reperage_pronoms(target, debug=False):
    if isinstance(target, Part):
        data = target
    else:
        data = load(target)
    nb_pro_total = 0
    nb_noms = 0
    index_phrase = 0
    freq_pro = {}
    for sentence in data:
        nb_pro_by_sentence = 0
        for word in sentence:     
            if word.pos.startswith('PRO') or word.pos.startswith("CL"):
                nb_pro_by_sentence += 1
                freq_pro[word.pos] = freq_pro.get(word.pos,0) + 1
            elif word.pos in ['NC', 'NPP']:
                nb_noms += 1
        if nb_pro_by_sentence > 0:
            if debug:
                print('Phrase', index_phrase, ': ', nb_pro_by_sentence, ' PRO')
            nb_pro_total += nb_pro_by_sentence
        index_phrase += 1
    if debug:
        print('reperage_pronoms on', target)
        print(f'Total pronoms : {nb_pro_total:10d}')
        print(f'Total phrases : {index_phrase:10d}')
        print('Moyenne pro / ph :  ', f"{(nb_pro_total / index_phrase):.3f}")
        print('Moyenne pro / nom:  ', f"{(nb_pro_total / nb_noms):.3f}")
    res = {
        'NB_PRONOMS' : nb_pro_total,
        'GEN_SENTENCE_LEN' : index_phrase,
        'PRONOM_AVG_PAR_PHRASE' : nb_pro_total / index_phrase,
        'DIS_PRO' : nb_pro_total / nb_noms,
        'GEN_WORD_LENGTH' : data.word_len,
        'NB_NOMS' : nb_noms
        }
    for key in freq_pro:
        if debug:
            print(key," : ",f"{freq_pro[key]/nb_pro_total:.3f}")
        res['PRONOM_FREQ_' + key] = freq_pro[key] / nb_pro_total
    return res

if __name__ == '__main__':
    reperage_pronoms('ema.tal')
