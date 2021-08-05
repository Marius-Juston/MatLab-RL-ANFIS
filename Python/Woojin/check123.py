import sys
import torch
import numpy as np
import matplotlib.pyplot as plt
import anfis
from ddpg import DDPGagent
from memory import *
from model import *

agent=torch.load('anfis_initialized.model')
print(agent.actor)
print(agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf0'].c)
