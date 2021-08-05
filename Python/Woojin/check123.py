from model import *

agent = torch.load('anfis_initialized.model')
print(agent.actor)
print(agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf0'].c)
