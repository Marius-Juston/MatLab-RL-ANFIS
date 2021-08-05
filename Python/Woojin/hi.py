import torch


def abc(a, b, c):
    model = torch.load('models/anfis_model.npy')
    x = torch.tensor([[a, b, c]])
    x = model(x).item()
    return x
