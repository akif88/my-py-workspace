import tensorflow as tf
import random

graph = tf.Graph()

with graph.as_default():
    # Input placeholders
    a = tf.placeholder(tf.float32, name="a")
    b = tf.placeholder(tf.float32, name="b")
    
    # Perform +, -, *, and / operations
    plus = tf.add(a, b, name="a_plus_b")
    minus = tf.subtract(a, b, name="a_minus_b")
    times = tf.multiply(a, b, name="a_times_b")
    divided = tf.divide(a, b, name="a_divided_by_b")

    # Summaries for operations
    plus_summ = tf.summary.scalar("plus_op_summary", plus)
    minus_summ = tf.summary.scalar("minus_op_summary", minus)
    times_summ = tf.summary.scalar("times_op_summary", times)
    divided_summ = tf.summary.scalar("divided_op_summary", divided)
    
    # Global step counter and its increment operation
    global_step = tf.Variable(0, trainable=False, dtype=tf.int32, name="global_step")
    inc_step = tf.assign(global_step, global_step + 1, name="increment_step")
    init = tf.global_variables_initializer()
    
    # Group all summaries together
    merged = tf.summary.merge_all()

# we use get_fresh_dir so that we can keep track of different
# runs of our graph; here, it will creates directories like:
# tbout/basic_summaries/1 
# tbout/basic_summaries/2 
# tbout/basic_summaries/3
from helpers_01 import get_fresh_dir

sess = tf.Session(graph=graph)
writer = tf.summary.FileWriter(get_fresh_dir('tbout/basic_summaries'), 
                               graph=graph)
sess.run(init)


for i in range(20):
    rand_a = random.uniform(0, 25)
    rand_b = random.uniform(0, 25)
    feed_dict = {a: rand_a, b: rand_b}
    step, summaries = sess.run([inc_step, merged], feed_dict=feed_dict)
    writer.add_summary(summaries, global_step=step)
    writer.flush()

sess.close()
writer.close()
