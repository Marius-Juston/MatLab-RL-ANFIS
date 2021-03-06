import sys
import gym
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import anfis
from ddpg import DDPGagent
from memory import *
from model import *
def generate_txt(model):
    coeffs = (model.layer['consequent']._coeff).tolist()    ##print final coeffs in cnsequent layer.
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
    #xsort, _ = x.sort()
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

agent = torch.load('anfis_initialized.model')
agent2 = torch.load('abc.model')
model = agent.actor
mfs_print(model)
print(len(agent.memory))
print((model.layer['consequent']._coeff))
#print(agent.critic.linear2.weight)
print(torch.equal(agent.critic.linear2.weight,agent2.critic.linear2.weight))
print(torch.equal(agent.actor.layer['consequent']._coeff,agent2.actor.layer['consequent']._coeff))
#for i in range(128):
#    ddpg(0.0,0.0,0.0,i,False)
