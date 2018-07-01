"""
This class implements the critic neural network.  This class primarily needs to be able to (i) construct a q-network that maps states
and actions to a numerical reward and (ii) implement a gradient descent process that updates parameters so the Q-function is closer
to the target estimates.
"""

import tensorflow as tf
import math

# Actor/Critic Neural Network Architecture
LAYER_1_SIZE = 400
LAYER_2_SIZE = 300

class CriticNetwork(object):

    def __init__(self, sess, state_dim, action_dim, learning_rate, tau, num_actor_vars):
        self.sess = sess
        self.s_dim = state_dim
        self.a_dim = action_dim
        self.learning_rate = learning_rate
        self.tau = tau

        # Build the critic network
        self.inputs, self.action, self.out = self.create_critic_network(nn_type = "non_target")

        # Again collect variables to be used for gradient udpates
        self.network_params = tf.trainable_variables()[num_actor_vars:]

        # Build the target critic network
        self.target_inputs, self.target_action, self.target_out = self.create_critic_network(nn_type = "target")

        self.target_network_params = tf.trainable_variables()[(len(self.network_params) + num_actor_vars):]
        self.num_train_vars = len(self.target_network_params)

        # Update target network with weights from non_target network
        self.update_target_network_params = [self.target_network_params[i].assign(tf.multiply(self.network_params[i], self.tau) + tf.multiply(self.target_network_params[i], 1. - self.tau))
                for i in range(len(self.target_network_params))]

        self.predicted_q_value = tf.placeholder(tf.float32, [None, 1])

        # Define loss function, which is the mean squared error the target Q-value and the current estimate
        self.loss = tf.reduce_mean(tf.squared_difference(self.predicted_q_value, self.out))
        # Use ADAM to perform gradient descent on the loss value
        self.optimize = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)

        self.action_grads = tf.gradients(self.out, self.action)

    # Perform gradient descent to move the Q-value closer to the target value
    def train(self, inputs, action, predicted_q_value):
        return self.sess.run([self.out, self.optimize], feed_dict={
                self.inputs: inputs,
                self.action: action,
                self.predicted_q_value: predicted_q_value
        })

    def predict(self, inputs, action):
        return self.sess.run(self.out, feed_dict={self.inputs: inputs, self.action: action})

    def predict_target(self, inputs, action):
        return self.sess.run(self.target_out, feed_dict={
            self.target_inputs: inputs,
            self.target_action: action
        })

    def action_gradients(self, inputs, actions):
        return self.sess.run(self.action_grads, feed_dict={
            self.inputs: inputs,
            self.action: actions
        })

    def update_target_network(self):
        # update_target_network_params = [self.target_network_params[i].assign(tf.multiply(self.network_params[i], self.tau) + tf.multiply(self.target_network_params[i], 1. - self.tau)) for i in range(len(self.target_network_params))]
        self.sess.run(self.update_target_network_params)


    # Implement critic neural network that maps states and actions to a long-term reward
    def create_critic_network(self,nn_type):

        # First layer only uses states as input.  Action is integrated into second layer
        states = tf.placeholder(tf.float32, shape = [None, self.s_dim])
        actions = tf.placeholder(tf.float32, shape = [None, self.a_dim])
        h1_state = tf.layers.dense(inputs = states, units = LAYER_1_SIZE, activation=tf.nn.relu)

        # Second hidden layers combines first hidden layers and actions
        h2_w_states = tf.Variable(tf.random_uniform([LAYER_1_SIZE, LAYER_2_SIZE],minval = -1/math.sqrt(self.s_dim),maxval = 1/math.sqrt(self.s_dim)))
        h2_w_actions = tf.Variable(tf.random_uniform([self.a_dim, LAYER_2_SIZE],minval = -1/math.sqrt(self.s_dim),maxval = 1/math.sqrt(self.s_dim)))
        h2_b = tf.Variable(tf.random_uniform([LAYER_2_SIZE],-1/math.sqrt(LAYER_1_SIZE),1/math.sqrt(LAYER_1_SIZE)))
        h2_in = tf.matmul(h1_state,h2_w_states) + tf.matmul(actions,h2_w_actions) + h2_b
        h2 = tf.nn.relu(h2_in)

        # Final layer outputs the Q value prediction given the state, action pair
        init = tf.random_uniform_initializer(minval = -.003, maxval = 0.003)
        q_value = tf.layers.dense(inputs = h2, units = 1, kernel_initializer = init, bias_initializer = init)

        return states, actions, q_value
