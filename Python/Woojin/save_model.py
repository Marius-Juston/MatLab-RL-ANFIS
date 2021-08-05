import torch


def abc(agent):
    torch.save(agent, 'models/anfis_ddpg.model')
    torch.save(agent.actor, 'models/actor.model')
    torch.save(agent.actor_target, 'models/actor_target.model')
    torch.save(agent.critic, 'models/critic.model')
    torch.save(agent.critic_target, 'models/critic_target.model')
    return 0
