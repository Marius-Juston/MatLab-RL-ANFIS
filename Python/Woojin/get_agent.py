import math
import random

import matplotlib.pyplot as plt
import numpy as np
import torch


def generate_txt(model):
    coeffs = model.layer['consequent']._coeff.tolist()  ##print final coeffs in cnsequent layer.
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
    """
        A simple utility function to plot the MFs for a variable.
        Supply the variable name, MFs and a set of x values to plot.
    """
    zero_length = (model.number_of_mfs[model.input_keywords[0]])
    x = torch.zeros(10000)
    y = -5
    for i in range(10000):
        x[i] = torch.tensor(y)
        y += 0.001
    for mfname, yvals in fv.fuzzify(x):
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


def weight_mod(agent):
    randomlist = random.sample(range(0, len(agent.critic.linear1.weight)), int(len(agent.critic.linear1.weight) / 2))
    with torch.no_grad():
        for num in randomlist:
            your_new_weights = torch.nn.init.kaiming_normal_(torch.empty(1, 4, requires_grad=True), a=math.sqrt(5))
            agent.critic.linear1.weight[num].copy_(your_new_weights[0])
    return agent


def ddpg(a, b, c, reward, done, agent, action, total_reward, over_fit, dis_error):
    batch_size = 128
    state = agent.curr_states
    new_state = np.array([a, b, c])
    agent.curr_states = new_state
    agent.memory.push(state, action, reward, new_state, done)

    if len(agent.memory) > batch_size and dis_error > 0.1:
        agent.update(batch_size)

    return agent
