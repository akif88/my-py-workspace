import sys

# read training data
def read_data(dataset):
    with open(dataset) as f:
        text = f.read()
    return text

# <s> and </s> in order to determine the beginning and end of each sentence.
# each word is separated in the list
def list_sentence_word(data):
    text = data.replace('\n\n', '\n')
    text = '<s> ' + data
    list_word = text.replace('\n', ' </s> \n<s> ').split()
    return list_word

# initial probability compute
def initial_prob_HMM(list_word):
    list_init_word = list()
    #for initial prob HMM
    for i in range(len(list_word)-1):
        if list_word[i] == '<s>':
            list_init_word.append(list_word[i+1].lower())
    
    initial_prob = dict()
    set_init_word = set(list_init_word)
    total_word = len(list_init_word)
    for i in set_init_word:
        pr_word = list_init_word.count(i)
        init_pr_word = pr_word / total_word
        initial_prob[i] = init_pr_word

    return initial_prob

# transition probability compute with bigram
def transition_prob_HMM(list_word):
    list_trans_word = list()
    for i in range(len(list_word)):
        if list_word[i] == '<ERR' or list_word[i]=='.':
            continue
        elif list_word[i].find('targ=') != -1:
            list_trans_word.append(list_word[i].replace('targ=', '').replace('>', ''))
        elif list_word[i] ==  '</ERR>':
            list_trans_word.pop()
        else:
            if list_word[i].endswith('.'):
                list_word[i]=list_word[i].replace('.', '')
            list_trans_word.append(list_word[i].lower())
    
    transition_prob= dict()
    word_pair = [list_trans_word[i]+' '+list_trans_word[i+1] for i in range(len(list_trans_word)-1)]
    set_word_pair = set(word_pair)

    for words in set_word_pair:
        cond_word = words.split()
        if cond_word[0] == '</s>':
            continue
        if len(cond_word) <=1:
            continue
        total_word_pair = word_pair.count(words)
        total_cond_word = list_trans_word.count(cond_word[0])
        prob_bigram = total_word_pair / total_cond_word

        if cond_word[0] in transition_prob:
            transition_prob[cond_word[0]].update({cond_word[1]: prob_bigram})
        else:
            transition_prob.update({cond_word[0]: {cond_word[1]: prob_bigram}})

    return transition_prob
   
# emission probability compute
def emission_prob_HMM(text, emission_backtrace, delt, ins, subs):
    emission_prob = dict() 
    #p(x|w) compute
    for i in emission_backtrace.keys():
        w, x = i.split('->')
        total_prob=1
        for j in emission_backtrace[i]:
            if j[2] == 'delt':
                total_prob *= delt[j[1]]/text.count(j[0]) 
            elif j[2] == 'ins':
                total_prob *= ins[j[1]]/text.count(j[0]) 
            elif j[2] == 'subs':
                total_prob *= subs[j[0]+'-'+j[1]]/text.count(j[0]) 
        
        if w in emission_prob:
            emission_prob[w].update({x: total_prob})
        else:
            emission_prob.update({w: {x: total_prob}})

    return emission_prob

# determine correct word and misspelled word and put it dict structure  
def pre_emission_prob_HMM(list_word):
    emission_list = list()
    emission_dict = dict()
    for i in range(len(list_word)):
        if list_word[i] == '<ERR':
            continue
        elif list_word[i].find('targ=') != -1:
            emission_list.append(list_word[i].replace('targ=', '').replace('>', ''))
        elif list_word[i] ==  '</ERR>':
            misspell=''
            if list_word[i-2].find('>') == -1:
                misspell = list_word[i-2]+' '+list_word[i-1]
            else:
                misspell = list_word[i-1]
            correct = emission_list.pop()
            emission_dict.setdefault(correct, set()).add(misspell)

    #minimum edit distance and backtrace each correct and misspelled word
    delt = dict()
    ins = dict()
    subs = dict()
    emission_backtrace = dict()
    for i,value in emission_dict.items():
        x = i
        for j in value:
            y = j
            dist = min_edit_dist(x,y)
            backtrace(dist, x, y, emission_backtrace, delt, ins, subs)
    
    return emission_backtrace, delt, ins, subs



# minimum edit distance
def min_edit_dist(x, y):
    dist = [[0]*(len(y)+1) for i in range(len(x)+1)]
    for i in range(1,len(x)+1):
        for j in range(1,len(y)+1):
            dist[i][0]=i
            dist[0][j] = j
            subs=0
            if x[i-1] != y[j-1]:
                subs=1

            dist[i][j] = min(dist[i-1][j-1]+subs, dist[i-1][j]+1, dist[i][j-1]+1)
    
    return dist

# backtrace minimum edit distance 
def backtrace(dist, x, y, emission_backtrace, delt, ins, subs):
    i = len(x)
    j = len(y)
    # go to the diagonal of matrix 
    value = dist[i][j]
    while value != 0:
        # left delete, down insertion, diagonal substutition
        try:
            delete = dist[i-1][j]
            insertion = dist[i][j-1]
            substitution = dist[i-1][j-1]
        except:
            break
        
        # go minimum value in matrix
        min_value = min(delete, insertion, substitution)
        
        # determine which operation
        if substitution == min_value:
            i -= 1
            j -= 1
            # if value and subs not equal, then substution performed
            if value != substitution:
                try:
                    letter_x = x[i]
                    letter_y = y[j]
                except:
                    break
                subs_letter = letter_x+'-'+letter_y
                # subs letters count determine how many time
                if subs_letter not in subs:
                    subs[subs_letter]=1
                else:
                    subs[subs_letter]+=1
                # correct and misspelled word put dict and with which letter
                if x+'->'+y not in emission_backtrace:
                    emission_backtrace.setdefault(x+'->'+y, [[letter_x, letter_y, 'subs']])
                else:
                    emission_backtrace.setdefault(x+'->'+y).append([letter_x, letter_y, 'subs'])
        elif delete == min_value:
            i -= 1
            if value != delete:
                letter = x[i]
                if letter not in delt:
                    delt[letter]=1
                else:
                    delt[letter]+=1
                
                if x+'->'+y not in emission_backtrace: 
                    emission_backtrace.setdefault(x+'->'+y, [[x[i:i+2], letter, 'delt']])
                else:
                    emission_backtrace.setdefault(x+'->'+y).append([x[i:i+2], letter, 'delt'])
        elif insertion == min_value:
            j -= 1
            if value != insertion:
                if len(y)-1 < i: letter = ' ' 
                else: letter = y[i]
                if letter not in ins:
                    ins[letter]=1
                else:
                    ins[letter]+=1

                if x+'->'+y not in emission_backtrace:
                    emission_backtrace.setdefault(x+'->'+y, [[x[i-1],letter, 'ins']])
                else:
                    emission_backtrace.setdefault(x+'->'+y).append([x[i-1], letter, 'ins'])
                    
        try:
            value = dist[i][j]
        except:
            break
            


# determine probability initial,transition and emission probability
# with Hidden Markov Model
def hidden_markov_model(initial_pr, trans_pr, emission_pr):
    initial_prob = initial_pr
    transition_prob = trans_pr
    emission_prob = emission_pr

    #print('initial prob: {}\n'.format(initial_prob))
    #print('transtion prob: {}\n'.format(transition_prob))
    #print('emission prob: {}'.format(emission_prob))



if __name__ == "__main__":
    dataset = sys.argv[1]
    text = read_data(dataset)
    
    output_txt = sys.argv[2]
    result = open(output_txt, 'w')

    list_word = list_sentence_word(text)
    
    #initial probability compute
    init_pr = initial_prob_HMM(list_word)

    #transition probability compute
    trans_pr = transition_prob_HMM(list_word)

    #emission probability compute
    emission_backtrace, delt, ins, subs = pre_emission_prob_HMM(list_word)
    emission_pr = emission_prob_HMM(text, emission_backtrace, delt, ins, subs)

    #Hidden Markov Model
    hidden_markov_model(init_pr, trans_pr, emission_pr)

    result.close()

