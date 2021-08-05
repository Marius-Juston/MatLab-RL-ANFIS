import sys
import torch
import numpy as np
import matplotlib.pyplot as plt
import anfis
from ddpg import DDPGagent
from memory import *
from model import *

def ddpg(a,b,c,agent):

    #state = agent.curr_states
    state = agent.curr_states
    new_state = np.array([a,b,c])
#    print(state)
#    print(new_state)
    agent.curr_states = new_state
#    action = np.array([np.float64(agent.get_action(new_state))])
    #reward = np.float64(reward)
#    print(len(agent.memory))
    agent.memory.push(state, action, reward, new_state, done)
    return agent
