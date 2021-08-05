import torch
import torch.autograd
import torch.optim as optim
import torch.nn as nn
import anfis

from model import *
from memory import *


def averaging(model,input):
    #far
    left = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf1'].a.item())
    right = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf3'].d.item())
    avg = (left + right) / 2
    left = -avg
    right = avg
    with torch.no_grad():
        model.layer['fuzzify'].varmfs[input].mfdefs['mf1'].a.copy_(torch.tensor(left,dtype=torch.float))
        model.layer['fuzzify'].varmfs[input].mfdefs['mf3'].d.copy_(torch.tensor(right,dtype=torch.float))

    #close far
    left = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf1'].b.item())
    right = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf3'].c.item())
    avg = (left + right) / 2
    left = -avg
    right = avg
    with torch.no_grad():
        model.layer['fuzzify'].varmfs[input].mfdefs['mf1'].b.copy_(torch.tensor(left,dtype=torch.float))
        model.layer['fuzzify'].varmfs[input].mfdefs['mf3'].c.copy_(torch.tensor(right,dtype=torch.float))

    #near
    left = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].a.item())
    right = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].d.item())
    avg = (left + right) / 2
    left = -avg
    right = avg
    with torch.no_grad():
        if input == 'distance_line':
            if left > -0.125:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].a.copy_(torch.tensor(-0.125,dtype=torch.float))
            else:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].a.copy_(torch.tensor(left,dtype=torch.float))
            if right < 0.125:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].d.copy_(torch.tensor(0.125,dtype=torch.float))
            else:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].d.copy_(torch.tensor(right,dtype=torch.float))
        elif input == 'theta_near':
            if left > -0.125:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].a.copy_(torch.tensor(-0.125,dtype=torch.float))
            else:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].a.copy_(torch.tensor(left,dtype=torch.float))
            if right < 0.125:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].d.copy_(torch.tensor(0.125,dtype=torch.float))
            else:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].d.copy_(torch.tensor(right,dtype=torch.float))
    #with torch.no_grad():
    #    model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].a.copy_(torch.tensor(left,dtype=torch.float))
    #    model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].d.copy_(torch.tensor(right,dtype=torch.float))

    #close_near
    left = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].b.item())
    right = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].c.item())
    avg = (left + right) / 2
    left = -avg
    right = avg
    with torch.no_grad():
        if input == 'distance_line':
            if left > -0.05:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].b.copy_(torch.tensor(-0.05,dtype=torch.float))
            else:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].b.copy_(torch.tensor(left,dtype=torch.float))
            if right < 0.05:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].c.copy_(torch.tensor(0.05,dtype=torch.float))
            else:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].c.copy_(torch.tensor(right,dtype=torch.float))
        elif input == 'theta_near':
            if left > -0.025:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].b.copy_(torch.tensor(-0.025,dtype=torch.float))
            else:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].b.copy_(torch.tensor(left,dtype=torch.float))
            if right < 0.025:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].c.copy_(torch.tensor(0.025,dtype=torch.float))
            else:
                model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].c.copy_(torch.tensor(right,dtype=torch.float))
    #    model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].b.copy_(torch.tensor(left,dtype=torch.float))
    #    model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].c.copy_(torch.tensor(right,dtype=torch.float))

def mfs_constraint(model):

    for i in range(len(model.input_keywords)):
        for j in range(model.number_of_mfs[model.input_keywords[i]]):
            averaging(model, model.input_keywords[i])

            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf0'].c = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf1'].a.item())
            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf0'].d = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf1'].b.item())
            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf1'].c = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf2'].a.item())

            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf1'].d = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf2'].b.item())
            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf3'].a = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf2'].c.item())
            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf3'].b = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf2'].d.item())
            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf4'].a = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf3'].c.item())
            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf4'].b = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf3'].d.item())


class DDPGagent:
    def __init__(self, num_inputs, num_outputs, anf, hidden_size=128, actor_learning_rate=1e-3, critic_learning_rate=1e-4, gamma=0.99, tau=1e-3, max_memory_size=50000):
        # Params
        self.num_states = num_inputs
        #self.num_actions = env.action_space.shape
        self.num_actions = num_outputs
        self.gamma = gamma
        self.tau = tau
        self.curr_states = np.array([0,0,0])
        # Networks
    #    self.actor = Actor(self.num_states, hidden_size, self.num_actions)
    #    self.actor_target = Actor(self.num_states, hidden_size, self.num_actions)
        self.actor = anf
        self.actor_target = anf
        self.critic = Critic(self.num_states + self.num_actions, hidden_size, self.num_actions)
        self.critic_target = Critic(self.num_states + self.num_actions, hidden_size, self.num_actions)

        for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
            target_param.data.copy_(param.data)

        for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
            target_param.data.copy_(param.data)

        # Training
        self.memory = Memory(max_memory_size)
    #    self.critic_criterion  = nn.MSELoss()
        self.critic_criterion  = torch.nn.MSELoss(reduction='sum')
        self.actor_optimizer  = optim.SGD(self.actor.parameters(), lr=1e-6*7, momentum=0.99)
    #    self.actor_optimizer  = optim.Adam(self.actor.parameters(), lr=actor_learning_rate)
        self.critic_optimizer = optim.SGD(self.critic.parameters(), lr=critic_learning_rate, momentum=0.99)
    #    self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=critic_learning_rate)

    def get_action(self, state):
        state = Variable(torch.from_numpy(state).float().unsqueeze(0))
        action = self.actor.forward(state)
        action = action.detach().numpy()[0,0]
        return action

    def update(self, batch_size):
        states, actions, rewards, next_states, _ = self.memory.sample(batch_size)
        states = torch.FloatTensor(states)
        #print(actions)
        actions = torch.FloatTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        actions = torch.reshape(actions,(batch_size,1))

        # Critic loss
        Qvals = self.critic.forward(states, actions)
        next_actions = self.actor_target.forward(next_states)
        next_Q = self.critic_target.forward(next_states, next_actions.detach())
        Qprime = rewards + self.gamma * next_Q
        critic_loss = self.critic_criterion(Qvals, Qprime)/5.
        if critic_loss.item() > 20:
            critic_loss = critic_loss / critic_loss.item() * 20.0

        # Actor loss
        policy_loss = -self.critic.forward(states, self.actor.forward(states)).mean()/-10.
      #  print("critic_loss")
      #  print(critic_loss)
      #  print("policy_loss")
      #  print(policy_loss)
        #print(self.actor.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf2'].a)
        # update networks
        self.actor_optimizer.zero_grad()
        policy_loss.backward()
        self.actor_optimizer.step()
        mfs_constraint(self.actor)
    #    (self.actor.layer['consequent']._coeff)[3] = torch.tensor([[0.0,0.0,0.0,0.0]])
    #    (self.actor.layer['consequent']._coeff)[4] = torch.tensor([[0.0,0.0,0.0,0.0]])
    #    (self.actor.layer['consequent']._coeff)[20] = torch.tensor([[0.0,0.0,0.0,0.0]])
    #    (self.actor.layer['consequent']._coeff)[21] = torch.tensor([[0.0,0.0,0.0,0.0]])
    #    (self.actor.layer['consequent']._coeff)[2] = torch.tensor([[0.0,0.0,0.0,0.0]])
    #    (self.actor.layer['consequent']._coeff)[7] = torch.tensor([[0.0,0.0,0.0,0.0]])
    #    (self.actor.layer['consequent']._coeff)[13] = torch.tensor([[0.0,0.0,0.0,0.0]])
    #    (self.actor.layer['consequent']._coeff)[18] = torch.tensor([[0.0,0.0,0.0,0.0]])
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        # update target networks
        for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
            target_param.data.copy_(param.data * self.tau + target_param.data * (1.0 - self.tau))

        for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
            target_param.data.copy_(param.data * self.tau + target_param.data * (1.0 - self.tau))
