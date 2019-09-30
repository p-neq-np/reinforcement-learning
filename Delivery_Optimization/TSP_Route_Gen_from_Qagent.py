#!/usr/bin/env python
# coding: utf-8

# In[10]:


# Base Data Science snippet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from tqdm import tqdm_notebook
import sys
sys.path.append("../")
from delivery import *
from delivery import run_episode, run_n_episodes
from Env import DeliveryEnvironment
from qagent import QAgent
import pymongo
from route_db import Storage
import datetime


# get_ipython().run_line_magic('matplotlib', 'inline')
# get_ipython().run_line_magic('load_ext', 'autoreload')
# get_ipython().run_line_magic('autoreload', '2')


# ### Points of interest and config

# In[13]:


n_points = 20
max_box = 10
n_stops = 10
n_samples = int(0.05*10**5)

pois = np.random.rand(n_points, 2) * max_box
print(pois)


# ### Simple TSP route gen

# In[14]:


dt = datetime.datetime.now().strftime("%d-%H-%M-%S")
# enable database 
st_table = "TSP10Gen"+dt
print("Table: ", st_table)
db = Storage(st_table)

for i in range(n_samples):
    if i % 1000 == 0:
        print("Test gen {} out of {} at {}".format(i, n_samples, datetime.datetime.now().strftime("%d-%H-%M-%S")))
    task_indices = np.random.choice(n_points, n_stops, replace=False)
    reverse_task_ind = np.column_stack((np.arange(n_stops), task_indices))
    task_locations = pois[task_indices, :]
    # no does_task_exist check
    env = DeliveryEnvironment(n_stops = n_stops, method = "distance", poi = task_locations)
    agent = QAgent(nA=env.action_space, nS=env.observation_space, alpha=0.8, gamma=0.8, eps_start=1, eps_decay=0.95, eps_min=0.01, sars='max')
    env, agent, reward = gen_n_episodes(env,agent, n_episodes=400)
    #env.render()
    route_indices = env.stops # need a getter?
    global_route_indices = reverse_task_ind[route_indices,1]
    # add to the database

    # each graph element will be seperated by colon (:)
    route_dict = {"input_graph": ':'.join(map(str, task_indices.tolist())), "route": ':'.join(map(str, global_route_indices.tolist())),
                  "reward": reward}
    res = db.insert_route(route_dict)

print('done')


# In[9]:


# todo
# generate CSV
db.print_table(limit=100)
#csv_path = "path" 
#db.generate_csv_from_table(st_table, csv_path)


# In[ ]:




