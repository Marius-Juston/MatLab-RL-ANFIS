from memory import *


def ddpg(a, b, c, agent):
    # state = agent.curr_states
    new_state = np.array([a, b, c])
    #    agent.curr_states = new_state
    action = np.array([np.float64(agent.get_action(new_state))])
    # print(action)
    return action.item()
