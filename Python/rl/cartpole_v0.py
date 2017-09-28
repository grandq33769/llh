'''
Pratice program for reinforcement learning (CartPole-v0)
Date : 2017/09/26
'''
import numpy as np
import gym

SHOW = True

if __name__ == '__main__':
    # print(gym.envs.registry.all())
    ENV = gym.make('CartPole-v0')
    # print(dir(ENV.action_space))
    for episode in range(20):
        observation = ENV.reset()
        # Upper bound & Lower bound of observation space
        # print(ENV.observation_space.high)
        # print(ENV.observation_space.low)
        # print(dir(ENV.observation_space))
        pre_obs = np.zeros(ENV.observation_space.shape)
        for t in range(1000):
            if SHOW:
                ENV.render()
            # print(observation)
            # print(dir(observation))
            action = ENV.action_space.sample()
            observation, reward, done, info = ENV.step(action)
            pre_obs = observation
            if done:
                print("Episode {} finished after {} timesteps".format(
                    episode + 1, t + 1))
                break
