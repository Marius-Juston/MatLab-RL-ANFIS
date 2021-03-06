import math
import random

import torch


def weight_mod(agent):
    randomlist = random.sample(range(0, len(agent.critic.linear1.weight)), int(len(agent.critic.linear1.weight) / 2))
    with torch.no_grad():
        for num in randomlist:
            your_new_weights = torch.nn.init.kaiming_normal_(torch.empty(1, 4, requires_grad=True), a=math.sqrt(5))
            agent.critic.linear1.weight[num].copy_(your_new_weights[0])
    return agent


def enable(agent):
    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf1'].a.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf1'].b.requires_grad = True

    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf2'].a.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf2'].b.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf2'].c.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf2'].d.requires_grad = True

    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf3'].c.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf3'].d.requires_grad = True
    ##
    agent.actor.layer['fuzzify'].varmfs['theta_far'].mfdefs['mf1'].a.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['theta_far'].mfdefs['mf1'].b.requires_grad = True

    agent.actor.layer['fuzzify'].varmfs['theta_far'].mfdefs['mf2'].a.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['theta_far'].mfdefs['mf2'].b.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['theta_far'].mfdefs['mf2'].c.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['theta_far'].mfdefs['mf2'].d.requires_grad = True

    agent.actor.layer['fuzzify'].varmfs['theta_far'].mfdefs['mf3'].c.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['theta_far'].mfdefs['mf3'].d.requires_grad = True
    ##
    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf1'].a.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf1'].b.requires_grad = True

    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf2'].a.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf2'].b.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf2'].c.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf2'].d.requires_grad = True

    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf3'].c.requires_grad = True
    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf3'].d.requires_grad = True

    return agent


def disable(agent):
    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf1'].a.requires_grad = False
    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf1'].b.requires_grad = False

    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf2'].a.requires_grad = False
    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf2'].b.requires_grad = False
    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf2'].c.requires_grad = False
    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf2'].d.requires_grad = False

    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf3'].c.requires_grad = False
    agent.actor.layer['fuzzify'].varmfs['distance_line'].mfdefs['mf3'].d.requires_grad = False
    ##
    ##
    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf1'].a.requires_grad = False
    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf1'].b.requires_grad = False

    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf2'].a.requires_grad = False
    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf2'].b.requires_grad = False
    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf2'].c.requires_grad = False
    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf2'].d.requires_grad = False

    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf3'].c.requires_grad = False
    agent.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf3'].d.requires_grad = False

    return agent


def ddpg(over_fit, curr_epoch):
    agent = torch.load('models/anfis_ddpg.model')
    if over_fit == 1:
        if curr_epoch == 34:
            torch.save(agent, 'anfis_ddpg34.model')
    return agent
