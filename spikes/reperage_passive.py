from texteval import process_file

if __name__ == '__main__':
    data = process_file('ema.tal')
    liste_passives = []
    for sentence in data:
        for word in sentence:
            if word.dep == 'aux_pass': # Suffisant si on pense qu'il y a qu'une seule forme passive par phrase
                liste_passives.append(sentence)
    nb_phrases = len(data)
    nb_passives = len(liste_passives)

    print('Nb phrases :', nb_phrases)
    print('Nb passives :', nb_passives)
    print(f'Ratio : {(nb_passives / nb_phrases):.3f} %')
