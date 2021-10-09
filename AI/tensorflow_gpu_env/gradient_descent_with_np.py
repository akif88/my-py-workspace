import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf


# Cost function: x^2
def J(x):
    return x*x

# Gradient of x^2 = 2*x
def J_grad(x):
    return 2*x

# Create datapoint to generate a gradient slope line
def grad_graph_helper(fn, mid, error, delta):
    x = np.linspace(mid-delta, mid+delta)
    print(x)
    y = error - (mid-x)*fn(mid)
    return x,y

# plot x^2 with a given gradient slope and annotations
def make_plot(ax, x, error, grad):
    grad_x, grad_y = grad_graph_helper(J_grad, x, error, 1)
    xs = np.linspace(-10, 10, 300)
    Js = J(xs)

    ax.set_xlabel('x'); ax.set_ylabel('J'); ax.grid(True)

    ax.plot(xs, Js)
    ax.plot(grad_x, grad_y, c='g', linewidth = 2)
    ax.scatter(x, error, c='r', marker='s', s=50, zorder=6)

    if grad < 0:
        text_fill, x_add, error_add = ("< 0", "right"), 2, 10
    else:
        text_fill, x_add, error_add = ("> 0", "left"), -9, 10

    ax.annotate("Grad is {}; move to the {}".format(*text_fill), [x, error], [x+x_add, error+error_add],
            arrowprops={'arrowstyle': '->'})


def descend(x, learning_rate, steps=50, graph_steps=[0,5,15,49]):
    x = float(x)
    fig, axes = plt.subplots(ncols=1, nrows=len(graph_steps), figsize=(12,4*len(graph_steps)))

    axes = iter(axes)
    for step in range(steps):
        error, grad = J(x), J_grad(x)
        if step in graph_steps:
            ax = next(axes)
            ax.set_title('Step: {}'.format(step))
            make_plot(ax,x,error, grad)

        x -= learning_rate*grad
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    descend(9.0, 0.05)














