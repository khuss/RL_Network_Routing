# Internet traffic optimization using Reinforcement Learning.

The following project is a proof of concept to examine the feasibility and usability of designing a Reinforcement Learning based network controller capable of making more efficient internet traffic and routing decisions to reduce congestion and dropped packets.

This repository is best described by the following [presentation](https://www.youtube.com/watch?v=2DApO34I_Y0&t=10s) delivered at the Data Science Retreat in Berlin.

## Description

Since its early days the internet has quickly become a main part of our daily lives. And while the volume of traffic keeps increasing exponentially, the content shared has also changed considerably, from simple text and images to High definition streaming, IoTs and cloud computing.

As this trend keeps going simply increasing capacity may no longer be enough. To keep up with the demand it is interesting to consider a solution using by reingeering the networks into smart networks capable of making decisions to maximize performance by using A.I techniques such as reinforcement Learning.

## The Environment

For the sake of our problem we decided to model our environment based on a random observed WAN (Wide area network) see figure below.

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

In order for both the actor and the criticto interact with the state the following  convolutional networks were used.

## Traffic Generator

## Example Notebook

## Results
