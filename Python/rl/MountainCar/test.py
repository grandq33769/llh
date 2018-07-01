import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import gym

# Parameter
BATCH_SIZE = 32
LR = 0.01                   # Learning rate
EPSILON = 0.9               # Probability of choosing the optimal action
GAMMA = 0.9                 # Reward Decay rate
TARGET_REPLACE_ITER = 100   # Target networt update step
MEMORY_CAPACITY = 2000      # Replay buffer
env = gym.make('MountainCarContinuous-v0') 
env = env.unwrapped
# N_ACTIONS = env.action_space.n  # Action of car
N_STATES = env.observation_space.shape[0]   # State information

# print("# of Actions: ", N_ACTIONS)
print("Dimensions of states", N_STATES)

print(dir(env.action_space))
print(env.action_space.high)

class Net(nn.Module):
    def __init__(self, ):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(N_STATES, 10)
        self.fc1.weight.data.normal_(0, 0.1)   # initialization
        self.out = nn.Linear(10, N_ACTIONS)
        self.out.weight.data.normal_(0, 0.1)   # initialization

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        actions_value = self.out(x)
        return actions_value
