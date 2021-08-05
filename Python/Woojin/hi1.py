import torch


def abc(a, b, c):
    agent = torch.load('models/anfis_ddpg.model')

    new_state = [a, b, c]
    action = agent.get_action(new_state)
    return action
