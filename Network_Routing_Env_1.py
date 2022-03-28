#!/usr/bin/env python
# coding: utf-8

# ### This is updated file with hot encoding

# In[1]:


import gym
from gym import spaces
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import os, sys


# In[2]:


class WanEnv(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self, df):
    super(WanEnv, self).__init__()
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions:
    self.action_space = spaces.MultiDiscrete([2,3,3,3,3])
    # Example for using image as input:
    self.observation_space = spaces.dict({
                                         'N1Q' : MultiDiscrete[5,5,5,5,5],
                                         'N2Q' : MultiDiscrete[5,5,5,5,5],
                                         'N3Q' : MultiDiscrete[5,5,5,5,5],
                                         'N4Q' : MultiDiscrete[5,5,5,5,5],
                                         'N5Q' : MultiDiscrete[5,5,5,5,5]}
                                        )
    #(low=0, high=255, shape=
     #               (HEIGHT, WIDTH, N_CHANNELS), dtype=np.uint8)

  def step(self, action):
    # Execute one time step within the environment
        self.take_action(action)
        reward, ob = self.take_action(action)
        return ob, reward
    
  def take_action(self, action):
        self.episode_over = self.backend.switch_link(action)
                
        self.ticks += 1
        tmp = []

        # check if episode ended by ERROR, then mark it in 'info'
        if self.episode_over:
            logging.info ('Episode ended by ERROR')
            self.info['exit_status'] = 'ERROR'

        # else Stop if max ticks over
        elif self.ticks == self.MAX_TICKS:
            logging.info ('Max ticks over, ending episode')
            self.episode_over = True
            self.info['exit_status'] = 'NORMAL'
    
  def reset(self):
    # Reset the state of the environment to an initial state
    self.N1Q = df.loc[:,["N1Q"]]
    self.N2Q = df.loc[:,["N2Q"]]
    self.N3Q = df.loc[:,["N3Q"]]
    self.N4Q = df.loc[:,["N4Q"]]
    self.N5Q = df.loc[:,["N5Q"]]
    self.reward=0
    self.done = False


# In[3]:


data = np.array([[4,4,1,2,3],[2,5,1,3,1],[0,0,0,0,4],[0,0,0,0,0],[0,0,0,0,5]])
action = [2,1,0,3,0]
df = pd.DataFrame(data, columns=["N1Q","N2Q","N3Q","N4Q","N5Q"])
print(df)
print(data)
print(action)


# In[4]:


def qcontrol(l, size, filler):    ## Functon used after each timestep to keep a constant queuee size 
    length = len(l)
    if length>size:
        return l[:5]
    elif length<size:
        for i in range(0,size-length):
            l.append(filler)
            return l
    else:
        return l


# In[5]:


def take_action(df,action):

    print(df)
    data = df.to_numpy()
    q=data.tolist()
    tmp = q.pop(0)

    #Actions (0: No routing for all)
    #N1, 1:route to N2, 2: route to N5
    #N2, 1:route to N4, 2: route to N3, 3: route to N1
    #N3, 1:route to N2, 2: route to N4, 3: route to N5
    #N4, 1:route to N5, 2: route to N3, 3: route to N2
    #N5, 1:route to N1, 2: route to N3, 3: route to N4
    q1 = data[:,0].tolist()[1:]   
    q2 = data[:,1].tolist()[1:]
    q3 = data[:,2].tolist()[1:]      ## Seperating into individual queues for manipulation since each one will
    q4 = data[:,3].tolist()[1:]      ## receive different quantity
    q5 = data[:,4].tolist()[1:]
    count = 0                         ## counter managing the multidiscrete action space
    reward = 0                        ## initializng reward for current episode
    for i in action:
        packet = tmp[count]
        if count==0:
            if i == 0:
                q1.insert(0, packet)
            elif i==1:
                if packet!=2:
                    q2.insert(0,packet)         ## Managing routing algorithm for each qeueu starting by q1 and 
                    reward += -1                ## along with each corresponding action, if the packet is routed 
                else:                           ## to its destination it disapears from our env and we get a +10 reward
                    reward += 10                ## if not it is added to the top of the next queue with a reward of -1                
            elif i==2:
                if packet!=5:
                    q5.insert(0,packet)
                    reward += -1
                else:
                    reward += 10                 ## if statement are determined by the available actions based on 
            count+=1                             ## network topology and encoded actions
        elif count==1:
            if i == 0:
                q2.insert(0, packet)
            elif i==1:
                if packet!=4:
                    q4.insert(0,packet)
                    reward += -1
                else:
                    reward += 10  
            elif i==2:
                if packet!=3:
                    q3.insert(0,packet)
                    reward += -1
                else:
                    reward += 10
            elif i==3:
                if packet!=1:
                    q1.insert(0,packet)
                    reward += -1
                else:
                    reward += 10
            count+=1
        elif count==2:
            if i == 0:
                q3.insert(0,packet)
            elif i==1:
                if packet!=2:
                    q2.insert(0,packet)
                    reward += -1
                else:
                    reward += 10
            elif i==2:
                if packet!=4:
                    q4.insert(0,packet)
                    reward += -1
                else:
                    reward += 10
            elif i==3:
                if packet!=5:
                    q5.insert(0,packet)
                    reward += -1
                else:
                    reward += 10
            count+=1
        elif count==3:
            if i == 0:
                q4.insert(0, packet)
                
            elif i==1:
                if packet!=5:
                    q5.insert(0,packet)
                    reward += -1
                else:
                    reward += 10
            elif i==2:
                if packet!=3:            
                    q3.insert(0,packet)
                    reward += -1
                else:
                    reward += 10
            elif i==3:
                if packet!=2:
                    q2.insert(0,packet)
                    reward += -1
                else:
                    reward += 10
            count+=1
        elif count==4:
            if i == 0:
                q5.insert(0, packet)
            elif i==1:
                if packet!=1:
                    q1.insert(0,packet)
                    reward += -1
                else:
                    reward += 10
            elif i==2:
                if packet!=3:
                    q3.insert(0,packet)
                    reward += -1
                else:
                    reward += 10
            elif i==3:
                if packet!=4:
                    q4.insert(0,packet)
                    reward += -1
                else:
                    reward += 10
            count+=1


    print(action)
    q1=qcontrol(q1,5,0)                     ## qcontrol is called for each individual to ensure a constant queue size
    q2=qcontrol(q2,5,0)                     ## according to our observation space definition
    q3=qcontrol(q3,5,0)
    q4=qcontrol(q4,5,0)
    q5=qcontrol(q5,5,0)
    new_state = np.array([q1,q2,q3,q4,q5]).T            ## reassembling o
    
    q1 =np.array(q1)
    ohq1 = np.zeros((q1.shape[0], q1.shape[0]+1))
    ohq1[np.arange(q1.size),q1]=1
#     print(ohq1)

    q2 =np.array(q2)
    ohq2 = np.zeros((q2.shape[0], q2.shape[0]+1))
    ohq2[np.arange(q2.size),q2]=1
#     print(ohq2)


    
    q3 =np.array(q3)
    ohq3 = np.zeros((q3.shape[0], q3.shape[0]+1))
    ohq3[np.arange(q3.size),q3]=1
    
#     print(ohq3)
    
    q4 =np.array(q4)
    ohq4 = np.zeros((q4.shape[0], q4.shape[0]+1))
    ohq4[np.arange(q4.size),q4]=1
    
#     print(ohq4)
    
    q5 =np.array(q5)
    ohq5 = np.zeros((q5.shape[0], q5.shape[0]+1))
    ohq5[np.arange(q5.size),q5]=1
    
    ns=np.dstack((ohq1,ohq2,ohq3,ohq4,ohq5))
    
    new_state_pandas = pd.DataFrame(new_state, columns = ["NQ1","NQ2","NQ3","NQ4","NQ%"])
    return new_state_pandas, reward, ns


# In[6]:


print(df)
print(action)
new_state, reward, ns = take_action(df,action)
print(ns)


# In[7]:


print(new_state)
print(reward)


# In[8]:


print(ns[0,:,:])


# In[ ]:




