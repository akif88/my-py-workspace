import tensorflow as tf


my_var = tf.Variable(0, name="my_var")

sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)

increment = my_var.assign(my_var+1)
for i in range(10):
    print(sess.run(increment), end = " ")


sess.run(init)
for i in range(10):
    print(sess.run(increment), end = " ")
