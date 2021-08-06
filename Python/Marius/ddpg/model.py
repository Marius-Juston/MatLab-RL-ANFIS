import torch
import torch.autograd
import torch.nn as nn
import torch.nn.functional as F

from anfis.consequent_layer import ConsequentLayerType
from anfis.joint_mamdani_membership import JointSymmetricTriangleMembership
from anfis.joint_membership_optimized import JointTrapMembershipV2
from anfis.trainer import make_joint_anfis


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


def ANFISmodel():
    input_vars = [
        [1.7802122831344604, -0.014350161887705326, -0.002436983399093151],
        [4.311977386474609, 0.038484424352645874, 1.1468671560287476],
        [7.7716193199157715, 0.049927543848752975, 0.19135497510433197]
    ]

    output_vars = [0.3702664375305176, 0.32249370217323303, 0.36133873462677, 0.410311758518219]

    x_joint_definitons = [
        ('distance', JointTrapMembershipV2(*input_vars[0], constant_center=True)),
        ('theta_far', JointTrapMembershipV2(*input_vars[1], constant_center=True)),
        ('theta_near', JointTrapMembershipV2(*input_vars[2], constant_center=True)),
    ]

    outputs = ['angular_velocity']

    mambani = JointSymmetricTriangleMembership(*output_vars, False, x_joint_definitons[0][1].required_dtype())

    rules_type = ConsequentLayerType.MAMDANI

    model = make_joint_anfis(x_joint_definitons, outputs, rules_type=rules_type, mamdani_defs=mambani)

    return model
