import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf

#a = tf.constant(3.0, name="input1")
#b = tf.constant(2.0, name="input2")

a = tf.placeholder(tf.float32, name="input1")
b = tf.placeholder(tf.float32, name="input2")

c = tf.add(a, b, name = "add_node")
d = tf.multiply(a, c, name = "mul_node")

#print(d)

# to run graph we define tf session
sess = tf.Session()

feed_dict = {a: 3.0, b: 2.0}
out = sess.run(d, feed_dict=feed_dict)
print(out)
