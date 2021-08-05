import sys
import torch
import numpy as np
import matplotlib.pyplot as plt
import anfis
from ddpg import DDPGagent
from memory import *
from model import *

def abc(agent):
 # torch.save(agent,'anfis_ddpg.model', _use_new_zipfile_serialization=False)
  torch.save(agent,'anfis_ddpg.model')
  torch.save(agent.actor, 'actor.model')
  torch.save(agent.actor_target, 'actor_target.model')
  torch.save(agent.critic, 'critic.model')
  torch.save(agent.critic_target, 'critic_target.model')
  return 0
