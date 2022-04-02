import os
import tensorflow.keras as keras
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D

class ActorCriticNetwork(keras.Model):
    def __init__(self, action_space, fc1_dims=512, fc2_dims=256,
            name='actor_critic', chkpt_dir='tmp/actor_critic'):
        super(ActorCriticNetwork, self).__init__()
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.actions = action_space
        self.model_name = name
        self.checkpoint_dir = chkpt_dir
        self.checkpoint_file = os.path.join(self.checkpoint_dir, name+'_ac')

        self.conv1 = Conv2D(32, 3, activation="relu")
        self.maxPool = MaxPooling2D((2, 2))
        self.Flatten = Flatten()
        self.fc1 = Dense(self.fc1_dims, activation='relu')
        self.fc2 = Dense(self.fc2_dims, activation='relu')
        self.v1 = Dense(1, activation=None)
        self.v2 = Dense(1, activation=None)
        self.v3 = Dense(1, activation=None)
        self.v4 = Dense(1, activation=None)
        self.v5 = Dense(1, activation=None)
        self.pi1 = Dense(action_space[0], activation='softmax')
        self.pi2 = Dense(action_space[1], activation='softmax')
        self.pi3 = Dense(action_space[2], activation='softmax')
        self.pi4 = Dense(action_space[3], activation='softmax')
        self.pi5 = Dense(action_space[4], activation='softmax')


    def call(self, state):
        value = self.conv1(state)
        value = self.maxPool(value)
        value = self.Flatten(value)
        value = self.fc1(value)
        value = self.fc2(value)

        v1 = self.v1(value)
        v2 = self.v2(value)
        v3 = self.v3(value)
        v4 = self.v4(value)
        v5 = self.v5(value)

        pi1 = self.pi1(value)
        pi2 = self.pi2(value)
        pi3 = self.pi3(value)
        pi4 = self.pi4(value)
        pi5 = self.pi5(value)

        v = [v1, v2, v3, v4, v5]
        pi = [pi1, pi2, pi3, pi4, pi5]

        return v, pi