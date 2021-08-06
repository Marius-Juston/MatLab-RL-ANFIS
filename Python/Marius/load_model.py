from consequent_layer import ConsequentLayerType

from joint_mamdani_membership import JointSymmetricTriangleMembership
from joint_membership_optimized import JointTrapMembershipV2
from trainer import make_joint_anfis, load_anfis


def load_full_model(location):
    i = [0, 0, 0, 0]

    x_joint_definitons = [
        ('distance', JointTrapMembershipV2(*i, constant_center=True)),
        ('theta_far', JointTrapMembershipV2(*i, constant_center=True)),
        ('theta_near', JointTrapMembershipV2(*i, constant_center=True))
    ]

    outputs = ['angular_velocity']

    mambani = JointSymmetricTriangleMembership(0, 0.5, 0.25, 0.25, False, x_joint_definitons[0][1].required_dtype())

    model = make_joint_anfis(x_joint_definitons, outputs, rules_type=ConsequentLayerType.MAMDANI, mamdani_defs=mambani,
                             matlab=True)

    load_anfis(model, location)

    return model
