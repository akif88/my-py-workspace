import tensorflow as tf
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import helpers_03

nn1_graph = tf.Graph()
with nn1_graph.as_default():
    with tf.name_scope("input"):
        x = tf.placeholder(tf.float32, shape=[None, 100])
        y = tf.placeholder(tf.float32, shape=[None]) # not used

    with tf.name_scope('hidden1'):
        w = tf.Variable(tf.truncated_normal([100, 300]), name='W')
        b = tf.Variable(tf.zeros([300]), name='b')
        z = tf.matmul(x,w) + b
        a = tf.nn.relu(z)

    with tf.name_scope('output'):
        w = tf.Variable(tf.truncated_normal([100, 2]), name='W')
        b = tf.Variable(tf.zeros([2]), name='b')
        z = tf.matmul(x,w) + b
        output = z

    with tf.name_scope('global_step'):
        global_step = tf.Variable(0, trainable=False, name='global_step')
        inc_step = tf.assign_add(global_step, 1, name='inc_step')

    with tf.name_scope('summaries'):
        for var in tf.trainable_variables():
            hist_summary = tf.summary.histogram(var.op.name, var)
        summary_op = tf.summary.merge_all()

    init = tf.global_variables_initializer()


x_tr = np.random.uniform(0, 500, 100).reshape(1,100)
feed_dict = {x: x_tr}




tb_base_path = 'tbout/nn1_graph'
tb_path = helpers_03.get_fresh_dir(tb_base_path)
sess = tf.Session(graph=nn1_graph)
writer = tf.summary.FileWriter(tb_path, graph=nn1_graph)
sess.run(init)
out = sess.run(output, feed_dict=feed_dict)
print(out)
summaries = sess.run(summary_op)
writer.add_summary(summaries)
writer.close()
sess.close()
