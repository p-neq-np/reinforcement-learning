import sys
sys.path.append("../")
from qagent import QAgent
from delivery import run_n_episodes, DeliveryQAgent
from Env import DeliveryEnvironment

env = DeliveryEnvironment(n_stops = 10, method = "hard_constraint")
#agent = QAgent(nA=env.action_space, nS=env.observation_space)
agent = DeliveryQAgent(env.observation_space,env.action_space)
run_n_episodes(env,agent,"training_100_stops_traffic.gif", n_episodes=1000)
env.render()
print('done')