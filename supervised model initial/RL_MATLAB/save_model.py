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

def abc():
  torch.save(agent,'anfis_ddpg.model', _use_new_zipfile_serialization=False)
