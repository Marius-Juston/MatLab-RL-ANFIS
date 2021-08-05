import sys

import gym
import matplotlib.pyplot as plt

from ddpg import DDPGagent
from model import *
from utils import *


def generate_txt(model):
    coeffs = (model.layer['consequent']._coeff).tolist()  ##print final coeffs in cnsequent layer.
    with open("coeffs.txt", 'w') as output:
        for row in coeffs:
            output.write(str(row) + '\n')

    mfs = []
    for i in range(len(model.input_keywords)):
        mfs.append(model.input_keywords[i])
        for j in range(model.number_of_mfs[model.input_keywords[i]]):
            mfs.append(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf{}'.format(j)].pretty())
    with open("mfs.txt", 'w') as output:
        for row in mfs:
            output.write(str(row) + '\n')


def mfs_print(model):
    for i in range(len(model.input_keywords)):
        for j in range(model.number_of_mfs[model.input_keywords[i]]):
            print(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf{}'.format(j)].pretty())


def _plot_mfs(var_name, fv, model):
    '''
        A simple utility function to plot the MFs for a variable.
        Supply the variable name, MFs and a set of x values to plot.
    '''
    # Sort x so we only plot each x-value once:
    # xsort, _ = x.sort()
    #    for mfname, yvals in fv.fuzzify(xsort):
    #        temp = 'mf5'
    #        if (mfname == temp) is False:
    #            plt.plot(xsort.tolist(), yvals.tolist(), label=mfname)
    zero_length = (model.number_of_mfs[model.input_keywords[0]])
    x = torch.zeros(10000)
    y = -5
    for i in range(10000):
        x[i] = torch.tensor(y)
        y += 0.001
    for mfname, yvals in fv.fuzzify(x):
        #        print(mfname)
        #        print(yvals)
        temp = 'mf{}'.format(zero_length)
        if (mfname == temp) is False:
            plt.plot(x, yvals.tolist(), label=mfname)
    plt.xlabel('Values for variable {} ({} MFs)'.format(var_name, fv.num_mfs))
    plt.ylabel('Membership')
    plt.legend(bbox_to_anchor=(1., 0.95))
    plt.show()


def plot_all_mfs(model):
    for i, (var_name, fv) in enumerate(model.layer.fuzzify.varmfs.items()):
        _plot_mfs(var_name, fv, model)


gym.logger.set_level(40)
env = NormalizedEnv(gym.make("Pendulum-v0"))
anf = Anfis().my_model()
# print(env.action_space.shape)
# env = gym.make('CartPole-v1')
print(env.action_space.shape)
agent = DDPGagent(env, anf)
noise = OUNoise(env.action_space)
batch_size = 128
rewards = []
avg_rewards = []

for episode in range(100):
    state = env.reset()
    noise.reset()
    episode_reward = 0

    for step in range(500):
        action = agent.get_action(state)
        #    action = np.tanh(action)
        #    print(action)
        action = noise.get_action(action, step)
        new_state, reward, done, _ = env.step(action)
        agent.memory.push(state, action, reward, new_state, done)
        if len(agent.memory) > batch_size:
            agent.update(batch_size)

        state = new_state
        episode_reward += reward
        if done:
            sys.stdout.write(
                "episode: {}, reward: {}, average _reward: {} \n".format(episode, np.round(episode_reward, decimals=2),
                                                                         np.mean(rewards[-10:])))
            break

    rewards.append(episode_reward)
    avg_rewards.append(np.mean(rewards[-10:]))
    print(episode)
    mfs_print(anf)
    if np.mean(rewards[-10:]) > -400:
        break

torch.save(agent, 'ddpg.model')
generate_txt(anf)
plot_all_mfs(anf)

plt.plot(rewards)
plt.plot(avg_rewards)
plt.plot()
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.show()
