import tensorflow as tf
import numpy as np
import sys


# train set and test set with vector 
def tensor(train_arr, train_y, test_arr, test_y):
    with tf.name_scope("input1"):
        x = tf.placeholder(tf.float32, shape=[None, 200])
        y = tf.placeholder(tf.float32, shape=[None, 2])
        learning_rate = 0.001

    with tf.name_scope("hidden1"):
        w_1 = tf.Variable(tf.truncated_normal([200, 100]))
        b_1 = tf.Variable(tf.zeros([100]))
        z_1 = tf.matmul(x, w_1) + b_1
        h_1 = tf.nn.relu(z_1)

    with tf.name_scope("hidden2"):
        w_2 = tf.Variable(tf.truncated_normal([100, 100]))
        b_2 = tf.Variable(tf.zeros([100]))
        z_2 = tf.matmul(h_1, w_2) + b_2
        h_2 = tf.nn.relu(z_2)

    with tf.name_scope("output"):
        w_3 = tf.Variable(tf.truncated_normal([100, 2]))
        b_3 = tf.Variable(tf.zeros([2]))
        out = tf.matmul(h_2, w_3) + b_3


    with tf.name_scope("loss"):
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits = out))
        train = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)
        
    
    init = tf.global_variables_initializer()
    
    with tf.Session() as sess:
        sess.run(init)

        for i in range(1000):
            loss_tr, _ = sess.run([loss, train], feed_dict={x: train_arr, y: train_y})

            print("loss: {}".format(loss_tr))
        
        pred = tf.nn.softmax(out)
        corr_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
        acc = tf.reduce_mean(tf.cast(corr_pred, tf.float32))
        print("Prediction:", acc.eval({x: test_arr, y: test_y}))


# read text and sum their vector 
def add_vector(pos, neg, vec, per_s):
    pos_sent = pos.split("\n")
    neg_sent = neg.split("\n")
    vector = vec.split("\n")
    
    # create dict for search words vectors
    vector_dict = dict()
    for i in range(len(vector)-1):
        vec_deneme = vector[i].split()
        words = vec_deneme[0].split(":")
        vector_dict[words[0]] = []
        vector_dict.setdefault(words[0], list()).append(words[1])
        for j in range(1,len(vec_deneme)):
            vector_dict.setdefault(words[0], list()).append(vec_deneme[j])

    
    total_arr = list()

    # sum positive vector
    for i in range(len(pos_sent)-1):
        np_list = list()
        sent_words=pos_sent[i].split()
        for j in range(len(sent_words)):
            if sent_words[j] in vector_dict:
                lst_word = vector_dict[sent_words[j]] 
                np_list.append(np.array(lst_word, dtype=np.float32))
        
        pos_vector = np.array(np_list).sum(axis=0)
        total_arr.append(pos_vector)
        #print(total_arr)

    # sum negative vector
    for i in range(len(neg_sent)-1):
        np_list = list()
        sent_words=neg_sent[i].split()
        for j in range(len(sent_words)):
            if sent_words[j] in vector_dict:
                lst_word = vector_dict[sent_words[j]] 
                np_list.append(np.array(lst_word, dtype=np.float32))

        neg_vector = np.array(np_list).sum(axis=0)
        total_arr.append(neg_vector)
    
    y_p = [[1.0, 0.0]] * (len(pos_sent)-1) 
    y_n = [[0.0, 1.0]] * (len(neg_sent)-1)

    true_y = y_p + y_n
    true_y = np.array(true_y, dtype=np.float32)
    total_arr = np.array(total_arr, dtype = np.float32)
    
    
    #shuffle array
    shuffle_arr = np.arange(len(total_arr))
    np.random.shuffle(shuffle_arr)
    total_arr = total_arr[shuffle_arr]
    true_y = true_y[shuffle_arr]
    
    #split train and test set
    train_num = len(total_arr) * (per_s/100)
    train_num = int(train_num)
    train_array = total_arr[0: train_num]
    train_y = true_y[0: train_num] 

    test_array = total_arr[train_num: len(total_arr)-1]
    test_y = true_y[train_num: len(true_y)-1]
    

    return train_array, train_y, test_array, test_y


if __name__ == "__main__":
    pos_txt = sys.argv[1]
    neg_txt = sys.argv[2]
    vector = sys.argv[3]
    per_s = int(sys.argv[4])

    # read positive.txt negative.txt vector.txt 
    with open(pos_txt, 'r') as f:
        pos = f.read()

    with open(neg_txt, 'r') as f:
        neg = f.read()

    with open(vector, 'r') as f:
        vector = f.read() 


    # Create vector sum with value from text and send to tensorflow
    train_arr, train_y, test_arr, test_y = add_vector(pos, neg, vector, per_s)
    tensor(train_arr, train_y, test_arr, test_y)







