import numpy as np


def ddpg(a, b, c, agent):
    new_state = np.array([a, b, c])
    action = np.array([np.float64(agent.get_action(new_state))])
    return action.item()
