# Internet traffic optimization using Reinforcement Learning.

The following project is a proof of concept to examine the feasibility and usability of designing a Reinforcement Learning based network controller capable of making more efficient internet traffic and routing decisions to reduce congestion and dropped packets.

This repository is best described by the following [presentation](https://www.youtube.com/watch?v=2DApO34I_Y0&t=10s) delivered at the Data Science Retreat in Berlin.

## Description

Since its early days the internet has quickly become a main part of our daily lives. And while the volume of traffic keeps increasing exponentially, the content shared has also changed considerably, from simple text and images to High definition streaming, IoTs and cloud computing.

As this trend keeps going simply increasing capacity may no longer be enough. To keep up with the demand it is interesting to consider a solution using by reingeering the networks into smart networks capable of making decisions to maximize performance by using A.I techniques such as reinforcement Learning.

## The Environment

For the sake of our problem we decided to model our environment based on a random observed WAN (Wide area network) see figure below.


<p align="center">
<img src="https://github.com/khuss/RL_Network_Routing/blob/main/Images/WAN.png" width="400">
</p>

The WAN based network is defined in  `NetworkEnv.py` made of 5 nodes in a partial-mesh topology, connected by a full-duplex communication link, thus two linked nodes can send and receive packets to each other at the same time. Finally, the nodes all have a fixed queue size used as a First in First out to dispatch the packets to be processed.

The environemnt has therefore a multidiscrete state space that is determined by  `[number of nodes x queue size]`.

The specifications for the topology are defined in the `NetworkEnv` class definition and can be customized to another topolgy provided the `take_action` function is also changed accordingly.

### Step

At each time step, the environment will receive an action from an agent and move the packets at the top of each queue to update the state. The action is in the form of a 1x5 vector `[V1, V2, V3, V4, V5]` where VX is a neighbour of node X and the recipient of its top packet. If the top packet reaches its correct destination it disapears from the environment otherwise it is added to the queue (at the end).

### Reward

Designing the reward function is essential to optimize for the required behaviour. As we are looking to reduce congestion and dropped packets our reward is calculated in the following way:
* A packet delivered to the correct destination gets the maximum reward of: + total size of queue
* Otherwise to favor less congested routing decisions if the recipient's queue isnt full the reward will be: - occupied queue size
* In the last case that the destination is incorrect and the corresponding queue is full the maximum penalty will be given of : - total size of queue


## The Agent

From the defined custom environment above, the multidiscrete action space and the nature of the problem we have decided to train the policy optimization algorithm actor-critic  defined in the `agent.py`. The benefits of having the advantage actor-critic algorithm is the critic's use of state values which will be useful to determine not only the actor's training but also the "goodness of our position"

The actor-critic algorithm's s training process is defined in the figure below.


<p align="center">
<img src="https://github.com/khuss/RL_Network_Routing/blob/main/Images/A2C.png" width="800" height = "350">
</p>




In order for both the actor and the critic to interact with the state the following  convolutional networks were used.


<p align="center">
<img src="https://github.com/khuss/RL_Network_Routing/blob/main/Images/NN.png" width="800" height = "350">
</p>


## Getting started

To get started download and install the packages in the requirements file:

`pip install -r requirements.txt`

Clone the repository with either `ssh` or `https`, alternatively download the files seperately to build your own model and test.

Follow the example Notebook available in the repo to load the `Network_environment`, `A2C_agent`. A number of episodes is then created for training or testing the model.

Episodes consists of randomly filled queues, and the agent will either train on or "play" the games created

## Results

The following results compare our trained agent with a random agent after training on 3000 episodes.



<p align="center">
<img src="https://github.com/khuss/RL_Network_Routing/blob/main/Images/SecondModel_Score.png" width="800" height = "350">
</p>



This proves that the agent has learned to adapt its choices based on the content of the qeueus. 


<p align="center">
<img src="https://github.com/khuss/RL_Network_Routing/blob/main/Images/SecondModel_Runtime.png" width="800" height = "350">
</p>


It would now be interested to connect the environment to a traffic generator or real traffic and observe the variety of metrics available to compare to currently used Network traffic controllers.
