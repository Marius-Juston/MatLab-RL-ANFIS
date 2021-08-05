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


def ddpg(a,b,c):
    agent = torch.load('anfis_ddpg.model')

    new_state = np.array([a,b,c])
    action = agent.get_action(new_state).item()
    return action
