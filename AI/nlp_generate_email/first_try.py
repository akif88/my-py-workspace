
def read():
    all_sentence = ''
    with open("dataset.txt") as text:
        all_sentence = text.read()
    return all_sentence


def compute_prob():
    sentence = read()
  
    
    words = sentence.lower().split('\n')
    print(len(words))
    words=words[0].split()
    print(words)

    sentence = sentence.lower().replace('\n', ' ')

    # words = sentence.split()
    

    # for bigram and trigram append <s> </s>
    # bigram = sentence.count("i am")/sentence.count(' i ')
    bigram = sentence.count(' '+words[0]+' '+words[1]+' ') / sentence.count(' '+words[0]+' ') 
    
    a = sentence.count(' '+words[0]+' '+words[1]+' ')
    print(words[0]+' '+words[1])
    
    prob_table_bigram = dict()
    prob_table_bigram[words[0]] = {words[1]: bigram}
    print(prob_table_bigram)
    



    print(bigram)


    trigram = sentence.count(' '+words[0]+' '+words[1]+' '+words[2]+' ') / sentence.count(' '+words[0]+' '+words[1]+' ')
    print(sentence.count(' '+words[0]+' '+words[1]+' '+words[2]+' '))
    print(words[0]+' '+words[1]+' '+words[2]+' ')
    
    prob_table_trigram = dict()
    prob_table_trigram[words[0]] = {words[1]: {words[2]:trigram}}
    print(prob_table_trigram)
    
    print(trigram)
    

    """print(len(sentence))

    print(sentence.count("and"))


    unigram = sentence.count(sentence[0])/len(sentence)


    print(unigram)

    """    






if __name__ == "__main__":

    compute_prob()




