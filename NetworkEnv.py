
import pandas as pd
import numpy as np

class NetworkEnv:
 # metadata = {'render.modes': ['human']}

    def __init__(self, env_name):
        self.env_name = env_name
        self.Node_1Q = np.zeros(10).T
        self.Node_2Q = np.zeros(10).T
        self.Node_3Q = np.zeros(10).T
        self.Node_4Q = np.zeros(10).T
        self.Node_5Q = np.zeros(10).T
        self.state_observation = np.zeros([10,5])
        self.action = np.zeros(5)
        self.N1_max_actions = 2
        self.N2_max_actions = 3
        self.N3_max_actions = 3
        self.N4_max_actions = 3
        self.N5_max_actions = 3
        self.done = False
        self.episode_length = 0

    def reset(self,df):
        # Reset the state of the environment to an initial state
        self.Node_1Q = np.array(df.loc[:,"N1Q"])
        self.Node_2Q = np.array(df.loc[:,"N2Q"])
        self.Node_3Q = np.array(df.loc[:,"N3Q"])
        self.Node_4Q = np.array(df.loc[:,"N4Q"])
        self.Node_5Q = np.array(df.loc[:,"N5Q"])
        self.state_observation = np.array([self.Node_1Q, self.Node_2Q, self.Node_3Q, self.Node_4Q, self.Node_5Q]).T
        self.reward=0
        self.done = False
    
    def random_action(self):
        raction_1 = np.random.randint(self.N1_max_actions + 1)
        raction_2 = np.random.randint(self.N2_max_actions + 1)
        raction_3 = np.random.randint(self.N3_max_actions + 1)
        raction_4 = np.random.randint(self.N4_max_actions + 1)
        raction_5 = np.random.randint(self.N5_max_actions + 1)
        random_action = np.array([raction_1, raction_2, raction_3, raction_4, raction_5])

        return random_action
    


    def step(self, action):
        # Execute one time step within the environment
        if  np.all((self.state_observation ==0)):
            self.done = True
            return self.state_observation, self.reward, self.done, self.episode_length
        elif self.episode_length > 200:
            self.done = True
            return self.state_observation, self.reward, self.done, self.episode_length

        self.action = action
        self.state_observation, self.reward = self.take_action()
        self.episode_length += 1
        if(self.episode_length >= 200):
            self.done = True

        return self.state_observation, self.reward, self.done, self.episode_length
        
    def random_step(self):
        self.action = self.random_action()
        print(self.action)
        self.state_observation, self.reward = self.take_action()
        return self.state_observation, self.reward, self.done, self.episode_length
        


    def qcontrol(self, l, size, filler):    ## Functon used after each timestep to keep a constant queuee size 
        length = len(l)
        if length>size:
            return l[:size]
        elif length<size:
            for i in range(0,size-length):
                l.append(filler)
                return l
        else:
            return l

    def take_action(self):
        action = self.action
        q=self.state_observation.tolist()
        tmp = q.pop(0)

        #Actions (0: No routing for all)
        #N1, 1:route to N2, 2: route to N5
        #N2, 1:route to N4, 2: route to N3, 3: route to N1
        #N3, 1:route to N2, 2: route to N4, 3: route to N5
        #N4, 1:route to N5, 2: route to N3, 3: route to N2
        #N5, 1:route to N1, 2: route to N3, 3: route to N4
        q1 = self.Node_1Q[1:].tolist()
        q2 = self.Node_2Q[1:].tolist()
        q3 = self.Node_3Q[1:].tolist()      ## Seperating into individual queues for manipulation since each one will
        q4 = self.Node_4Q[1:].tolist()      ## receive different quantity
        q5 = self.Node_5Q[1:].tolist()
        count = 0                         ## counter managing the multidiscrete action space
        reward = 0                        ## initializng reward for current episode
        for i in action:
            packet = tmp[count]
            if packet != 0:
                if count==0:
                    if i == 0:
                        q1.insert(0, packet)
                        reward += -10
                    elif i==1:
                        if packet!=2:
                            q2.insert(0,packet)         ## Managing routing algorithm for each qeueu starting by q1 and 
                            reward += -(10-q2.count(0))              ## along with each corresponding action, if the packet is routed 
                        else:                           ## to its destination it disapears from our env and we get a +10 reward
                            reward += 10                ## if not it is added to the top of the next queue with a reward of -1                
                    elif i==2:
                        if packet!=5:
                            q5.insert(0,packet)
                            reward += -(10-q5.count(0))
                        else:
                            reward += 10                 ## if statement are determined by the available actions based on 
                    count+=1                             ## network topology and encoded actions
                elif count==1:
                    if i == 0:
                        q2.insert(0, packet)
                        reward += -10
                    elif i==1:
                        if packet!=4:
                            q4.insert(0,packet)
                            reward += -(10-q4.count(0))
                        else:
                            reward += 10  
                    elif i==2:
                        if packet!=3:
                            q3.insert(0,packet)
                            reward += -(10-q3.count(0))
                        else:
                            reward += 10
                    elif i==3:
                        if packet!=1:
                            q1.insert(0,packet)
                            reward += -(10-q1.count(0))
                        else:
                            reward += 10
                    count+=1
                elif count==2:
                    if i == 0:
                        q3.insert(0,packet)
                        reward += -10
                    elif i==1:
                        if packet!=2:
                            q2.insert(0,packet)
                            reward += -(10-q2.count(0))
                        else:
                            reward += 10
                    elif i==2:
                        if packet!=4:
                            q4.insert(0,packet)
                            reward += -(10-q4.count(0))
                        else:
                            reward += 10
                    elif i==3:
                        if packet!=5:
                            q5.insert(0,packet)
                            reward += -(10-q5.count(0))
                        else:
                            reward += 10
                    count+=1
                elif count==3:
                    if i == 0:
                        q4.insert(0, packet)
                        reward += -10

                    elif i==1:
                        if packet!=5:
                            q5.insert(0,packet)
                            reward += -(10-q5.count(0))
                        else:
                            reward += 10
                    elif i==2:
                        if packet!=3:            
                            q3.insert(0,packet)
                            reward += -(10-q3.count(0))
                        else:
                            reward += 10
                    elif i==3:
                        if packet!=2:
                            q2.insert(0,packet)
                            reward += -(10-q2.count(0))
                        else:
                            reward += 10
                    count+=1
                elif count==4:
                    if i == 0:
                        q5.insert(0, packet)
                        reward += -10
                    elif i==1:
                        if packet!=1:
                            q1.insert(0,packet)
                            reward += -(10-q1.count(0))
                        else:
                            reward += 10
                    elif i==2:
                        if packet!=3:
                            q3.insert(0,packet)
                            reward += -(10-q3.count(0))
                        else:
                            reward += 10
                    elif i==3:
                        if packet!=4:
                            q4.insert(0,packet)
                            reward += -(10-q4.count(0))
                        else:
                            reward += 10
                    count+=1
            else:
              #  globals()[tt] = "q"+ str(count+1)
               # tt.insert(0,packet)

                if i == 0:
                    reward += 10
                else :
                    reward += -10

                count+=1


       
        q1=self.qcontrol(q1,10,0)                     ## qcontrol is called for each individual to ensure a constant queue size
        q2=self.qcontrol(q2,10,0)                     ## according to our observation space definition
        q3=self.qcontrol(q3,10,0)
        q4=self.qcontrol(q4,10,0)
        q5=self.qcontrol(q5,10,0)
        self.Node_1Q=np.array(q1)
        self.Node_2Q=np.array(q2)
        self.Node_3Q=np.array(q3)
        self.Node_4Q=np.array(q4)
        self.Node_5Q=np.array(q5)

        new_state = np.array([q1,q2,q3,q4,q5]).T
        ## reassembling o
        return new_state, reward

if __name__ == "__main__":
    #env_name = 'Pong-v0'
    NetworkEnv(env_name)
    #agent.test('Models/PongDeterministic-v4_PG_2.5e-05.h5')
    #agent.test('Models/Pong-v0_PG_2.5e-05.h5')


