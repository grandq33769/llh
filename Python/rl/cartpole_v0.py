'''
Pratice program for reinforcement learning (CartPole-v0)
Date : 2017/09/26
'''
import gym

if __name__ == '__main__':
    ENV = gym.make('CartPole-v0')
    for episode in range(20):
        observation = ENV.reset()
        for t in range(100):
            print(observation)
            action = ENV.action_space.sample()
            observation, reward, done, info = ENV.step(action)
            if done:
                print("Episode finished after {} timesteps".format(t + 1))
                break
