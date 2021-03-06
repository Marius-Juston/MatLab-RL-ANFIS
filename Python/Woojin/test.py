import gym
import torch

from utils import NormalizedEnv, OUNoise

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
    if step % 1.5 == 0:
        action = noise.get_action(action)
        new_state, reward, done, _ = env.step(action)

    print(len(agent.memory))

    state = new_state
    step += 1
