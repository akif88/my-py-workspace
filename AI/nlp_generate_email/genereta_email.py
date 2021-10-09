import sys
import math
import random

# read email/text data
def read_data(dataset):
    with open(dataset) as text: 
        email_data = text.read()
    return email_data


# the beginning and end of each clue is determined with <s> and </s>
# then they are separated into words of each sentence.
def list_all_sentence(data, n_gram):
    email_data ='<s> ' + data
    if n_gram == 2:
        email_data ='<s> ' + data
        list_sentence = email_data.replace('\n', ' </s> \n<s> ').split()
    elif n_gram == 3:
        email_data ='<s> <s> ' + data
        list_sentence = email_data.replace('\n', ' </s> </s> \n<s> <s> ').split()
    return list_sentence


# each unique number of words is specified for add-one
def words_count(data):
    set_words = set(data)
    count = len(set_words)
    return count

# the frequency and probabilities of each word are calculated and 
# the probability of the word being in the sentence is written in the table 
def unsmoothed_unigram(list_words):
    total_words_number = len(list_words)
    set_words = set(list_words)

    table_unsmoothed_unigram = dict()
    for word in set_words:
        if '<s>' == word:
            continue
        total_word = list_words.count(word)

        prob_unigram = total_word / total_words_number

        table_unsmoothed_unigram[word] = prob_unigram

    return table_unsmoothed_unigram


# add-one unigram
def smoothed_unigram(list_words, words_count):
    total_words_number = len(list_words) + words_count
    set_words = set(list_words)
    
    table_smoothed_unigram = dict()
    for word in set_words:
        if '<s>' == word:
            continue
        total_word = list_words.count(word) + 1
        
        prob_unigram = total_word / total_words_number
        table_smoothed_unigram[word] = prob_unigram

    return table_smoothed_unigram


# In the sentence, there is a possibility of two calves 
# coming side by side and recorded in the table.
def unsmoothed_bigram(list_words):
    words_pair = [list_words[i]+' '+list_words[i+1] for i in range(len(list_words)-1)]
    set_words_pair = set(words_pair)
    
    table_unsmoothed_bigram = dict()
    for words in set_words_pair:
        cond_word = words.split()
        if cond_word[0] == '</s>':
            continue
        
        total_words_pair = words_pair.count(words)

        total_cond_word = list_words.count(cond_word[0])

        prob_bigram = total_words_pair / total_cond_word

        if cond_word[0] in table_unsmoothed_bigram:
            table_unsmoothed_bigram[cond_word[0]].update({cond_word[1]: prob_bigram})
        else:
            table_unsmoothed_bigram.update({cond_word[0]: {cond_word[1]: prob_bigram}})

    return table_unsmoothed_bigram
    

    
# we add the word pairs to the table and apply the add-one method
def smoothed_bigram(list_words, count):
    words_pair = [list_words[i]+' '+list_words[i+1] for i in range(len(list_words)-1)]
    set_words_pair = set(words_pair)
    
    table_smoothed_bigram = dict()
    for words in set_words_pair:
        cond_word = words.split()
        if cond_word[0] == '</s>':
            continue

        total_words_pair = words_pair.count(words) + 1

        total_cond_word = list_words.count(cond_word[0]) + count

        prob_bigram = total_words_pair / total_cond_word

        if cond_word[0] in table_smoothed_bigram:
            table_smoothed_bigram[cond_word[0]].update({cond_word[1]: prob_bigram})
        else:
            table_smoothed_bigram.update({cond_word[0]: {cond_word[1]: prob_bigram}})

    
    set_words = set(list_words)
    
    # In this loop, we add other pairs that are not in the training set, 
    # and we do the probability calculation with add-one method.
    for word in set_words:
        if word == '</s>':
            continue

        total_cond_word=list_words.count(word) + count
        total_word_number = 1
        prob_smooth_bigram = total_word_number / total_cond_word
        
        for words in set_words:
            
            if word not in table_smoothed_bigram:
                table_smoothed_bigram.update({word:{words: prob_smooth_bigram}})
                
            if words not in table_smoothed_bigram:
                table_smoothed_bigram.update({words:{word: prob_smooth_bigram}})
                
            if words in table_smoothed_bigram[word]:
                continue
            
            table_smoothed_bigram[word].update({words:prob_smooth_bigram})
    
    return table_smoothed_bigram
    
# The probabilities of the three words coming together are calculated.
def unsmoothed_trigram(list_words):
    words_three = [list_words[i]+' '+list_words[i+1]+' '+list_words[i+2] 
            for i in range(len(list_words)-2)]
    set_words_three = set(words_three)
    
    words_pair = [list_words[i]+' '+list_words[i+1] for i in range(len(list_words)-1)]

    table_unsmoothed_trigram = dict()
    for words in set_words_three:
        dist_word = words.split()
        if dist_word[0] == '</s>' or dist_word[1] == '</s>':
            continue
        
        total_three_words = words_three.count(words)
        
        total_words_pair = words_pair.count(dist_word[0]+' '+dist_word[1])
        
        prob_trigram = total_three_words / total_words_pair
        
        if dist_word[0]+' '+dist_word[1] in table_unsmoothed_trigram:
            table_unsmoothed_trigram[dist_word[0]+' '+dist_word[1]].update({dist_word[2]: prob_trigram})
        else:
            table_unsmoothed_trigram.update({dist_word[0]+' '+dist_word[1]: {dist_word[2]: prob_trigram}})
    
    return table_unsmoothed_trigram


# we add the three word to the table and apply the add-one method
def smoothed_trigram(list_words, count):
    words_three = [list_words[i]+' '+list_words[i+1]+' '+list_words[i+2] 
            for i in range(len(list_words)-2)]
    set_words_three = set(words_three)
    
    words_pair = [list_words[i]+' '+list_words[i+1] for i in range(len(list_words)-1)]

    table_smoothed_trigram = dict()
    for words in set_words_three:
        dist_word = words.split()
        if dist_word[0] == '</s>':
            continue
        
        total_three_words = words_three.count(words) + 1
        
        total_words_pair = words_pair.count(dist_word[0]+' '+dist_word[1])+count
        
        prob_trigram = total_three_words / total_words_pair
        
        if dist_word[0] in table_smoothed_trigram:
            if dist_word[1] in table_smoothed_trigram[dist_word[0]]:
                table_smoothed_trigram[dist_word[0]][dist_word[1]].update({dist_word[2]: prob_trigram})
            else:
                table_smoothed_trigram[dist_word[0]].update({dist_word[1]: {}})
                table_smoothed_trigram[dist_word[0]][dist_word[1]].update({dist_word[2]: prob_trigram})
        else:
            table_smoothed_trigram.update({dist_word[0]: {dist_word[1]: {dist_word[2]: prob_trigram}}})
    
    
    set_words_pair = set(words_pair)
    set_word = set(list_words)
    
    # In this loop, we add other pairs that are not in the training set, 
    # and we do the probability calculation with add-one method.
    for words in set_words_pair:
        if '</s> ' in words:
            continue

        total_words_pair = words_pair.count(words) + count
        total_three_words = 1
        prob_smooth_trigram = total_three_words / total_words_pair
        
        dist_word = words.split()

        for word in set_word:
            
            if dist_word[0] not in table_smoothed_trigram:
                table_smoothed_trigram.update({dist_word[0]: {dist_word[1]: {word: prob_smooth_trigram}}})
                table_smoothed_trigram[dist_word[0]].update({word: {dist_word[1]: prob_smooth_trigram}})
            else:
                if dist_word[1] not in table_smoothed_trigram[dist_word[0]]:
                    table_smoothed_trigram[dist_word[0]].update({dist_word[1]: {word: prob_smooth_trigram}})
                if word not in table_smoothed_trigram[dist_word[0]]:
                    table_smoothed_trigram[dist_word[0]].update({word: {dist_word[1]: prob_smooth_trigram}})
     
            
            if dist_word[1] not in table_smoothed_trigram:
                table_smoothed_trigram.update({dist_word[1]: {dist_word[0]: {word: prob_smooth_trigram}}})
                table_smoothed_trigram[dist_word[1]].update({word: {dist_word[0]: prob_smooth_trigram}})
            else:
                if dist_word[0] not in table_smoothed_trigram[dist_word[1]]:
                    table_smoothed_trigram[dist_word[1]].update({dist_word[0]: {word: prob_smooth_trigram}})
                if word not in table_smoothed_trigram[dist_word[1]]:
                    table_smoothed_trigram[dist_word[1]].update({word: {dist_word[0]: prob_smooth_trigram}})

            if word not in table_smoothed_trigram:
                table_smoothed_trigram.update({word: {dist_word[0]: {dist_word[1]: prob_smooth_trigram}}})
                table_smoothed_trigram[word].update({dist_word[1]: {dist_word[0]: prob_smooth_trigram}})
            else:
                if dist_word[0] not in table_smoothed_trigram[word]:
                    table_smoothed_trigram[word].update({dist_word[0]: {dist_word[1]: prob_smooth_trigram}})
                if dist_word[1] not in table_smoothed_trigram[word]:
                    table_smoothed_trigram[word].update({dist_word[1]: {dist_word[0]: prob_smooth_trigram}})
    
    

    return table_smoothed_trigram
    
# The probabilities and perplexity of the mails in the test set are being calculated.
def estimate_perplexity_email(table_trigram, table_bigram, data, result):

    
    for i in range(len(data)):
        result.write('-----------Sentence '+str(i+1)+'----------- \n')
        sentence = '<s> <s> '+data[i]
        result.write(sentence+' </s>\n\n')
    
        words = sentence.split()
        # -------- trigram-------------
        estimate=1
        for i in range(len(words)-2):
            try:
                estimate *= table_trigram[words[i]][words[i+1]][words[i+2]]
            except:
                estimate = 1.0e-100

        N = len(words)
        total_log_prob = 0
        for i in range(N):
            total_log_prob += math.log2(estimate)
        perplexity = 2**((-1/N)*total_log_prob)
        result.write('---------Smoothed Trigram---------\n')
        result.write('Estimate e-mail: {} Perplexity: {}\n\n'.format(estimate, perplexity))
        # --------------------------------------------------

        # ----------bigram------------------
        estimate = 1
        for i in range(len(words)-1):
            try:
                estimate *= table_bigram[words[i]][words[i+1]]
            except:
                estimate = 1.0e-100
    
        total_log_prob = 0
        for i in range(N):
            total_log_prob += math.log2(estimate)
        perplexity = 2**((-1/N)*total_log_prob)
    
        result.write('---------Smoothed Bigram---------\n')
        result.write('Perplexity: {}\n'.format(estimate, perplexity))
        result.write('---------------------------------\n\n\n')     
      

# this method generates mail with Unigram, Bigram and Trigram.      
def generate_email(table_unigram ,table_bigram, table_trigram, result):
    
    punct = ['.', '?', '!', '</s>']
    
    result.write('------Generating E-mail wih Unigram-------------\n')
    for i in range(10):
        # unigram
        count = 1
        total = 0
        result.write('<s> ')
        while total < 1 and count < 30:
            word = random.choice(list(table_unigram.keys()))
            total += table_unigram[word]
            result.write(word+' ')
        
            if word in punct:
                result.write(word)
                break

            count +=1
    
        result.write(' </s>\n\n')
    result.write('-------------------------------------------------\n\n')

    result.write('------Generating E-mail wih Bigram-------------\n')
    # --------------bigram-------------------------------------
    for i in range(10):
        word_1 = random.choice(list(table_bigram['<s>'].keys()))
        word_2 = random.choice(list(table_bigram[word_1].keys()))
    
        count = 1 
        result.write('<s> ')
        while count < 30:
            result.write(word_1+' '+word_2+' ')
        
            word_1 = random.choice(list(table_bigram[word_2].keys()))
            if word_1 in punct:
                result.write(word_1)
                break
        
            word_2 = random.choice(list(table_bigram[word_1].keys()))
            if word_2 in punct:
                result.write(word_2)
                break

            count+=2
        result.write(' </s>\n\n')
    result.write('-------------------------------------------------\n\n')
    #------------------------------------------------------------


    result.write('------Generating E-mail wih Trigram-------------\n')
    # ------------trigram----------------------------------------
    for i in range(10):
        word_1 = random.choice(list(table_trigram['<s> <s>'].keys()))

        count=1
        result.write('<s> '+word_1+' ')

        while count < 30:
        
            word_2 = random.choice(list(table_trigram.keys()))
            if word_2 in punct:
                result.write(word_2)
                break
        
            word = random.choice(list(table_trigram[word_2].keys()))
            if word in punct:
                result.write(word)
                break
        
            result.write(word+' ')
            count+=2
        result.write(' </s>\n\n')


if __name__ == "__main__":
    
    dataset = "data.txt"
    email_data = read_data(dataset)

    all_data = email_data.split('\n')
    size = int((len(all_data)*3)/5)

    training_data = all_data[:size]
    test_data = all_data[size:]

    #result_text = sys.argv[2]
    #result = open(result_text, 'w')

    list_sentence = list_all_sentence(str(training_data), 2)
     
    #list_words = list_all_words(email_data)
    
    count = words_count(list_sentence)

    # unigram
    table_u_unigram = unsmoothed_unigram(list_sentence)
    table_s_unigram = smoothed_unigram(list_sentence, count)
    #print(table_s_unigram)
    
    #bigram
    table_u_bigram = unsmoothed_bigram(list_sentence)
    table_s_bigram = smoothed_bigram(list_sentence, count)
    print(table_s_bigram)


    """
    list_sentence = list_all_sentence(email_data, 3)
    #trigram
    table_u_trigram = unsmoothed_trigram(list_sentence)
    table_trigram = smoothed_trigram(list_sentence, count)
    
    # estimate and perplexity with smoothed_trigram and smoothed_bigram 
    estimate_perplexity_email(table_trigram, table_s_bigram, test_data, result)
    
    #generating email with unigram bigram trigram
    generate_email(table_u_unigram, table_u_bigram, table_u_trigram, result)

    result.close()
    """

