Reinforcement Learning applied to Tic Tac Toe

 ## Overview
 
The goal of this project is to implement an agent capable of playing and winning Tic Tac Toe against a human
opponent. The agent starts first by placing X in a random case. The human opponent plays O.

The file `main.py` contains the implementation of the GUI of a Tic Tac Toe game using the Tkinter Python library
The file `MDP.py` contains the Markov Decision Process elements. The Value Iteration and policy Iteration 
algorithms used to train 
the agent are contained in the file `rl_algorithms.py`. 

To play the game against the agent, please use the following command line : 
            `$ python3 main.py --algorithm "algorithm_name" `
 

 ## Value Iteration and Policy Uteration Algorithms 
 
With both algorithms, positive results are observed. The agent not only focuses on taking actions that will lead to his victory, 
he also tries to prevent the human opponent from winning.
Moreover, when faced with the choices of winning a game or preventing the opponent from winning, such as the following case : 

| x |   | o |
| o | o |   |
| x |   | x |

The agent places the X in the (2,3) case to prevent O from winning, instead of placing X in the (3,2) case
and thus winning the game. This may lead in those cases to a draw instead of a win.


    
    