import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tensorflow as tf


# Create Graph  fir Linear Regression Model

linreg_graph = tf.Graph()
with linreg_graph.as_default():
    with tf.name_scope('inputs'):
        x_ph = tf.placeholder(tf.float32, [None], name='x')
        y_ph = tf.placeholder(tf.float32, [None], name='y')
        learning_rate = tf.placeholder(tf.float32, [], name='learning_rate')

    with tf.name_scope('model'):
        w = tf.Variable(tf.truncated_normal([]), name='w')
        b = tf.Variable(tf.constant(0, dtype=tf.float32), name='b')
        y_hat = tf.multiply(w, x_ph) + b

    with tf.name_scope('loss'):
        loss = tf.reduce_mean(tf.square(y_hat - y_ph), name='MSE')

    with tf.name_scope('train'):
        opt = tf.train.GradientDescentOptimizer
        train = opt(learning_rate).minimize(loss)

    with tf.name_scope('global_step'):
        global_step = tf.Variable(0, trainable=False, name='global_step')
        inc_step = tf.assign_add(global_step, 1, name='inc_step')

    with tf.name_scope('helpers'):
        init = tf.global_variables_initializer()

session = tf.Session(graph=linreg_graph)
session.run(init)


# true model: y = true_w*x + true_b
true_w, true_b = 3, 2


# create training data and make a feeder dict
x_train = np.random.uniform(-5, 5, size=[20])
epsilon = np.random.normal(loc=0, scale=1.5, size=[20])
y_train = (true_w*x_train) +true_b + epsilon
train_dict = {x_ph: x_train,
              y_ph: y_train,
              learning_rate: 0.05}

# test
x_test = np.array([-5.0, 5.0])
test_dict = {x_ph: x_test}



snapshots = []
print("{:2} {:^6s}".format("i", "MSE"))
for i in range(50):
    J, w_est, b_est, step, _ = session.run([loss, w, b, inc_step, train], feed_dict=train_dict)

    if not i % 5:
        print("{:<2d} {:>6.3f}".format(step, J))

    if step in [0, 1,4,10,49]:
        y_test = session.run(y_hat, feed_dict=test_dict)
        snapshots.append((i, y_test, w_est, b_est, J))


final_w_est, final_b_est = session.run([w,b])

_, _, w_est, b_est, losses = zip(*snapshots)


for i, snapshot in enumerate(snapshots):
    # extract needed components for current snapshot
    step, y_test, curr_w_est, curr_b_est, curr_loss = snapshot

    # setup outer figure
    fig = plt.figure(figsize=(16,4))
    title_fmt = 'Step: {} error: {:0.4f} w = {:0.4f} b = {:0.4f}'
    title_string = title_fmt.format(step, curr_loss, 
                                    curr_w_est, curr_b_est)
    fig.suptitle(title_string, size=20)

    # Scatter plot of data with predicted line
    ax = plt.subplot(131)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.grid(True)
    ax.scatter(x_train, y_train, c='r')
    ax.plot(x_test, y_test) # both curr train->test and estimated line

    # 3D view of estimated w and b values against loss
    ax = plt.subplot(132, projection='3d')
    ax.set_xlabel('w'); ax.set_ylabel('b'); ax.set_zlabel('loss')
    ax.plot(w_est, b_est, losses)
    ax.scatter(curr_w_est, curr_b_est, curr_loss, c='r')
    
    # Overhead view of approximate error curves
    ax = plt.subplot(133)
    ax.set_xlabel('w'); ax.set_ylabel('b'); ax.grid(True)
    for i in range(1,6):
        circ = mpl.patches.Circle([final_w_est, final_b_est], 
                                  .5 * i, fill=False)
        ax.add_patch(circ)
        
    ax.plot(w_est, b_est)                   # the path of w/b estimates
    ax.scatter(curr_w_est, curr_b_est, c='r') # really just one point
    ax.set_aspect('equal')
    #plt.show()



# with scikit
import sklearn.linear_model as sk_lm
model = sk_lm.LinearRegression()
model.fit(np.reshape(x_train, [20,1]), y_train)
print('sk linreg w: {:5.3f} b: {:5.3f}'.format(model.coef_[0],model.intercept_))

# compared with our estimates
print('our tflr  w: {:5.3f} b: {:5.3f}'.format(final_w_est, 
                                                    final_b_est))





















