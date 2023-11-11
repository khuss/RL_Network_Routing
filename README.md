# Internet traffic optimization using Reinforcement Learning.

The following project is a proof of concept to examine the feasibility and usability of designing a Reinforcement Learning based network controller capable of making more efficient internet traffic and routing decisions to reduce congestion and dropped packets.

This repository is best described by the following [presentation](https://www.youtube.com/watch?v=2DApO34I_Y0&t=10s) delivered at the Data Science Retreat in Berlin.

## Description

Since its early days the internet has quickly become a main part of our daily lives. And while the volume of traffic keeps increasing exponentially, the content shared has also changed considerably, from simple text and images to High definition streaming, IoTs and cloud computing.

As this trend keeps going simply increasing capacity may no longer be enough. To keep up with the demand it is interesting to consider a solution using by reingeering the networks into smart networks capable of making decisions to maximize performance by using A.I techniques such as reinforcement Learning.

## The Environment

For the sake of our problem we decided to model our environment based on a random observed WAN (Wide area network). 

The WAN based network is made of 5 nodes connected in a partial-mesh topology. The nodes are connected by a full-duplex communication link, thus two linked nodes can send and receive packets to each other at the same time. Finally, the nodes all have a fixed queue size (adjustable in the class declaration), along with the obtained total size of the observation state and the given number of actions.

### Action

## The Agent

## Traffic Generator

## Example Notebook

## Results
