from texteval import load, Part

def reperage_passive(target, debug=False):
    if isinstance(target, Part):
        data = target
    else:
        data = load(target)
    liste_passives = []
    for sentence in data:
        for word in sentence:
            if word.dep == 'aux_pass': # Suffisant si on pense qu'il y a qu'une seule forme passive par phrase
                liste_passives.append(sentence)
    nb_phrases = len(data)
    nb_passives = len(liste_passives)
    if debug:
        print('reperage_passive on ' + target)
        print('Nb phrases  :', f"{nb_phrases:6d}")
        print('Nb passives :', f"{nb_passives:6d}")
        print(f'Ratio      : {(nb_passives / nb_phrases):.3f} %')
    return {
        'GEN_SENTENCE_LEN' : nb_phrases,
        'PASSIVE_NB_PASSIVES' : nb_passives,
        'SYN_NB_PASSIVE' : nb_passives / nb_phrases,
        'GEN_WORD_LENGTH' : data.word_len
        }

if __name__ == '__main__':
    reperage_passive('ema.tal')
