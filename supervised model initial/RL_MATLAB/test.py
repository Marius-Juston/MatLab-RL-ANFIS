import sys
import gym
import torch
from ddpg import DDPGagent
from memory import *
gym.logger.set_level(40)
env = NormalizedEnv(gym.make("Pendulum-v0"))
noise = OUNoise(env.action_space)

state = env.reset()
agent = torch.load('ddpg.model')
step = 0
while 1:
    env.render()
    action = agent.get_action(state)

    new_state, reward, done, _ = env.step([action])
    print(new_state)
    print(type(new_state))
    print(reward)
    print(type(reward))
    print(done)
    print(type(done))
    if step%1.5 == 0:
        action = noise.get_action(action)
        new_state, reward, done, _ = env.step(action)


    state = new_state
    step += 1
#model_copy = copy.deepcopy(model)
