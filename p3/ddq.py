import numpy as np
import tensorflow as tf

class Decider(object):
    def __init__(self, shape):
      self.observation_shape = shape

    def observation_batch_shape(self, batch_size):
        return tuple([batch_size] + list(self.observation_shape))

    def create_variables(self):
      pass

    def act(self, sess, observation):
        #assert observation.shape == self.observation_shape
        a = tf.concat([
          # buttons
          tf.random_uniform([13]),
          # directions
          tf.reshape(tf.random_uniform([2,2]), [4]),
          # sleeps
          tf.random_uniform([2]),
        ], 0)
        a = tf.map_fn(lambda x: x - 0.95, a)
        a = tf.nn.relu(a)
        return sess.run(a)
