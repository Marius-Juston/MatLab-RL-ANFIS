import torch
import torch.autograd
import torch.nn as nn
import torch.nn.functional as F

import anfis
from membership import TriangularMembFunc, TrapezoidalMembFunc, Zero


class Critic(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Critic, self).__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, output_size)

    def forward(self, state, action):
        """
        Params state and actions are torch tensors
        """
        x = torch.cat([state, action], 1)
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.linear3(x)

        return x


class Anfis():
    def __init__(self):
        super(Anfis, self).__init__()

    def my_model(self):
        invardefs = [
            ('distance_line', [TrapezoidalMembFunc(-100, -100, -1.9209120273590088, -1.2210495471954346, 1),
                               TrapezoidalMembFunc(-1.9209120273590088, -1.2210495471954346, -0.7004659175872803,
                                                   -0.0035696756094694138, 2),
                               TrapezoidalMembFunc(-0.7004659175872803, -0.0035696756094694138, 0.0035696756094694138,
                                                   0.7004659175872803, 3),
                               TrapezoidalMembFunc(0.0035696756094694138, 0.7004659175872803, 1.2210495471954346,
                                                   1.9209120273590088, 4),
                               TrapezoidalMembFunc(1.2210495471954346, 1.9209120273590088, 100, 100, 5),
                               Zero()]),
            ('theta_far', [TrapezoidalMembFunc(-3.15, -3.15, -2.352747917175293, -1.284698486328125, 1),
                           TrapezoidalMembFunc(-2.352747917175293, -1.284698486328125, -1.177300214767456,
                                               -0.14307035505771637, 2),
                           TrapezoidalMembFunc(-1.177300214767456, -0.14307035505771637, 0.14307035505771637,
                                               1.177300214767456, 3),
                           TrapezoidalMembFunc(0.14307035505771637, 1.177300214767456, 1.284698486328125,
                                               2.352747917175293, 4),
                           TrapezoidalMembFunc(1.284698486328125, 2.352747917175293, 3.15, 3.15, 5),
                           Zero()]),
            ('theta_near', [TrapezoidalMembFunc(-3.15, -3.15, -1.6965510845184326, -0.9778405427932739, 1),
                            TrapezoidalMembFunc(-1.6965510845184326, -0.9778405427932739, -0.40821388363838196,
                                                -0.006021264940500259, 2),
                            TrapezoidalMembFunc(-0.40821388363838196, -0.006021264940500259, 0.006021264940500259,
                                                0.40821388363838196, 3),
                            TrapezoidalMembFunc(0.006021264940500259, 0.40821388363838196, 0.9778405427932739,
                                                1.6965510845184326, 4),
                            TrapezoidalMembFunc(0.9778405427932739, 1.6965510845184326, 3.15, 3.15, 5),
                            Zero()])
        ]
        outvars = ['control_law']

        mamdani_out = [
            ('right3', [TriangularMembFunc(-1.25, -1, -0.75)]),
            ('right2', [TriangularMembFunc(-1, -0.75, -0.5)]),
            ('rigt1', [TriangularMembFunc(-0.75, -0.5, 0)]),
            ('zero', [TriangularMembFunc(-0.5, 0, 0.5)]),
            ('left1', [TriangularMembFunc(0, 0.5, 0.75)]),
            ('left2', [TriangularMembFunc(0.5, 0.75, 1)]),
            ('left3', [TriangularMembFunc(0.75, 1, 1.25)])
        ]

        input_keywords = []  # list
        number_of_mfs = {}  # dict
        for i in range(len(invardefs)):
            input_keywords.append(invardefs[i][0])
            number_of_mfs[invardefs[i][0]] = len(invardefs[i][1]) - 1
        anf = anfis.AnfisNet('ANFIS', invardefs, outvars, mamdani_out, input_keywords, number_of_mfs, False)
        return anf
