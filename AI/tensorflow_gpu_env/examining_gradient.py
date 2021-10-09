import tensorflow as tf


grad_graph = tf.Graph()
with grad_graph.as_default():
    a = tf.Variable(3.0)
    b = tf.square(a)
    opt = tf.train.GradientDescentOptimizer(0.05)
    grads = opt.compute_gradients(b, [a])
    init = tf.global_variables_initializer()

with tf.Session(graph=grad_graph) as session:
    session.run(init)
    print(session.run(grads))

