import numpy as np
import tensorflow as tf

# 0-D tensor (scalar) 
np_0d = np.array(4, dtype=np.int32)

# 1-D tensor (vector)
np_1d = np.array([1,2,3], dtype=np.int64)

# 2-D tensor (matrix)
np_2d = np.array([[1,2],
                  [3,4],
                  [5,6]], dtype=np.float32)
# 3-D tensor
np_3d = np.array([[[0, 0], [0, 1], [0, 2]],
                  [[1, 0], [1, 1], [1, 2]],
                  [[2, 0], [2, 1], [2, 2]]], dtype=np.int32)

np_defined_tensor = [np_0d, np_1d, np_2d, np_3d]


for ndt in np_defined_tensor:
    print(tf.constant(ndt))


# shape an tensor with NumPy

arr = np.arange(24).reshape(2,3,4)
print("In NumPy:", arr.shape, arr, sep="\n")


# shape an tensor with tf

shape_op = tf.shape(arr)
print("In TF:", shape_op, sep="\n")

shape = tf.Session().run(shape_op)
print("Shape of tensor:", shape)


# tf add with np array

a=np.array([1,2], dtype=np.int32)
b=np.array([3,4], dtype=np.int32)
c=tf.add(a,b)

result=tf.Session().run(c)
print("np array:", result)




