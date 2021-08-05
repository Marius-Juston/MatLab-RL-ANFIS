import torch


def abc(a, b, c):
    agent = torch.load('models/anfis_ddpg.model')

    new_state = [a, b, c]
    action = agent.get_action(new_state)

    #    model = torch.load('models/anfis_model.npy')
    #    x = torch.tensor([[a,b,c]])
    #    x = model(x).item()
    return action
