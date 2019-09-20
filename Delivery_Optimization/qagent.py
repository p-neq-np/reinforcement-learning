from collections import defaultdict
import numpy as np
from scipy.special import softmax

#0.999,gamma = 0.95,lr = 0.8
class QAgent():
    def __init__(self, nA=6, nS=6, alpha=0.8, gamma=0.8, eps_start=1, eps_decay=0.95, eps_min=0.01, sars='max'):
        """ Initialize agent.

        Params
        ======
        - nA: number of actions available to the agent
        - alpha: update rate
        - gamma: discount rate
        - epsilon: starting epsilon value
        - eps_decay: epsilon decay value (linear decay)
        - eps_min: the min epsilon
        - sars: the update method
        ('max': sarsamax, 'soft': softmax update)
        """
        #'exp': expected_sarsa, 'sars': sarsa
        self.nA = nA
        self.nS = nS
        #self.Q = defaultdict(lambda: np.zeros(self.nA), dtype=np.float64)
        #self.Q = defaultdict(lambda: np.full(self.nA, 0, dtype=np.float64))
        self.Q = np.zeros([self.nS, self.nA])
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = eps_start
        self.eps_decay = eps_decay
        self.eps_min = eps_min
        self.sars = sars
        self.state_history = []

        if sars == 'max':
            self.train = lambda state, action, reward, next_state, done=False: \
                self.max_update(state, action, reward, next_state, done=False)
        elif sars == 'soft':
            self.train = lambda state, action, reward, next_state, done=False: \
                self.softmax_update(state, action, reward, next_state, done=False)
        elif sars == 'sars':
            self.train = lambda state, action, reward, next_state, done=False: \
                self.sarsa_update(state, action, reward, next_state, done=False)

    def reset_memory(self):
        self.state_history.clear()
        
    def remember_state(self, s):
        self.state_history.append(s)

    def update_epsilon(self):  # epsilon update

        """ Updates e-greedy(Q) beginning of each episode
        Linear Decay
        Params
        ======

        Returns
        =======
        - epsilon: updated epsilon value
        """
        if self.epsilon > self.eps_min:
            self.epsilon *= self.eps_decay
        #self.epsilon = max(self.epsilon * self.eps_decay,
        #                   self.eps_min)  # e <- e_i
        return self.epsilon

    def act(self, state):  # policy
        """ Given the state, select an action in e-greedy(Q) way
        Params
        ======
        - state: the current state of the environment
        - epsilon: the epsilon of e-greedy
        Returns
        =======
        - action: an integer, compatible with the task's action space
        - policy_s: current policy for given state
        
        """
        
        # The constraints check
        Q_t = np.copy(self.Q[state, :])
        # Avoid already visited states - Hard constraint?
        Q_t[self.state_history] = -np.inf
        
        # Epsilon greedy 
        if np.random.rand() > self.epsilon:
            action = np.argmax(Q_t)
        else:
            possible_states = [x for x in range(self.nA) if x not in self.state_history]
            action = np.random.choice(possible_states)
            
        return action
        
    
    def max_update(self, state, action, reward, next_state, done=False): #update step
        """ Update the agent's knowledge-> state-value function (Q),
        using the most recently sampled tuple with sarsa max
            
        Params
        ======
        - state: the previous state of the environment
        - action: the agent's previous choice of action
        - reward: last reward received
        - next_state: the current state of the environment
        - done: whether the episode is complete (True or False)
        """
        #Q_update = 0
        #if not done: # if done next state Q value is 0
        #    if self.sars == 'max': # sarsamax
                #np.random.
        #Q_update = np.max(self.Q[next_state])
        #old_Q = self.Q[state][action]
        #self.Q[state][action] = old_Q + (self.alpha * (reward + (self.gamma * Q_update) - old_Q))
        self.Q[state,action] = self.Q[state,action] + self.alpha * \
                               (reward + self.gamma * np.max(self.Q[next_state]) - self.Q[state,action])

    def softmax_update(self, state, action, reward, next_state, done=False):  # update step

        """ Update the agent's knowledge-> state-value function (Q),
        using the most recently sampled tuple with sarsa softmax.

        Params
        ======
        - state: the previous state of the environment
        - action: the agent's previous choice of action
        - reward: last reward received
        - next_state: the current state of the environment
        - done: whether the episode is complete (True or False)
        """

        possible_updates = softmax(self.Q[next_state])
        update = np.random.choice(self.nA, 1, p=possible_updates)
        self.Q[state, action] = self.Q[state, action] + self.alpha * \
                                (reward + self.gamma * self.Q[next_state, update] - self.Q[state, action])

    def sarsa_update(self, state, action, reward, next_state, done=False): # update step
        next_action = self.act(next_state)
        # print("state, next_state, action:", state, next_state, next_action)
        self.Q[state, action] = self.Q[state, action] + self.alpha * \
                                (reward + self.gamma * self.Q[next_state, next_action] - self.Q[state, action])
