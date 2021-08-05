import numpy as np


def ddpg(a, b, c, agent):
    state = agent.curr_states
    new_state = np.array([a, b, c])
    agent.curr_states = new_state
    agent.memory.push(state, action, reward, new_state, done)
    return agent
