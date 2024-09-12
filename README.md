Reinforcement Learning applied to Tic Tac Toe

 ## Overview
 
The goal of this project is to implement an agent capable of playing and winning Tic Tac Toe against a human
opponent. The agent starts first by placing X in a random case. The human opponent plays O.

The file main.py contains the implementation of the GUI of a Tic Tac Toe game using the Tkinter Python library
The file MDP.py contains the Markov Decision Process elements as well as the Value Iteration algorithm used to train 
our agent. 
 

 ## Value Iteration Algorithm 
 
With value iteration, the observations are as follows : 

    The actions generated do not depend on the Bellman's equation's discount factor and threshold.
    
    The agent focuses on taking actions that will lead to his victory. This only works in cases ending with a draw. 
    
    However, when the human opponent takes actions leading him to victory, rather than preventing him from winning,
the agent focuses on winning his own game. This results in the agent's lost. 