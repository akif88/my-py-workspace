import tensorflow as tf
import numpy as np


# create new  graph. you can create more graph as well 

new_graph = tf.Graph()

with new_graph.as_default():
    a=tf.add(3,4)
    b=tf.multiply(a, 2)

sess_new = tf.Session(graph=new_graph).run(b)
print(sess_new)

