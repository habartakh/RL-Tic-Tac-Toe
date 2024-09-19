import numpy as np

class MDP : 
    def __init__(self):
        self.states = set()
        self.terminal_states = set()
        self.actions = {}
        
    def generate_possible_states(self):
        
        # First generate all the board possible and impossible configurations 
        
        # A single board configuration is modeled by a nonuple 
        # which makes calculations simpler than a 3*3 matrix such as:
        # 0 : Empty case ; 1 : X ; 2 : O
            
        def generate_all_configurations():
            all_configs = set()
            for values in np.ndindex(3, 3, 3, 3, 3, 3, 3, 3, 3):
                state = tuple(values)
                all_configs.add(state)
            return all_configs
    
       
        # checks if there is only one winner either X or O
        def not_only_one_winner(state):  
            horizontal_wins , vertical_wins = 0, 0
            for i in range(3):
                
                if (state[i*3] == state[i*3+1] == state[i*3+2] and state[i*3] == 1) or (state[i*3] == state[i*3+1] == state[i*3+2] and state[i*3] == 2):
                    horizontal_wins += 1
          
                if (state[i] == state[3+i] == state[6+i] and state[i] == 1) or (state[i] == state[3+i] == state[6+i] and state[i] == 2):
                    vertical_wins += 1
          
            return horizontal_wins == 2 or vertical_wins == 2 
        
        self.states = generate_all_configurations()
        
        for state in self.states.copy() : 
            
            # The agent will be the one starting with "X", thus there will be more X than O
            if state.count(1)<state.count(2):
                self.states.remove(state)
            
            # If each player plays once, there cannot be more than one symbol than the other 
            elif abs(state.count(1) - state.count(2)) > 1:
                self.states.remove(state)
            
            elif not_only_one_winner(state): 
                self.states.remove(state)
                
        
    def check_win(self , state):
        for i in range(3):
            if state[i*3] == state[i*3+1] == state[i*3+2] and state[i*3] != 0:
              return state[i*3]
          
            if state[i] == state[3+i] == state[6+i] and state[i] != 0:
              return state[i]
          
        if state[4] == state[6] == state[2] and state[4] != 0:
          return state[4]
        
        elif state[0] == state[4] == state[8] and state[0] != 0:
          return state[0]
        
        else:
          return False


    def generate_terminal_states(self):
        for state in self.states: 
            if state.count(0) == 0 or self.check_win(state)  : 
                self.terminal_states.add(state)
                

    def generate_actions (self):  
        # for each state, we will store the indices of the cases where the agent can place the X
        for state in self.states : 
            self.actions[state] = None
            if state not in self.terminal_states : 
                self.actions[state] = []
                for i in range (len(state)):
                    if state[i] == 0 :
                        self.actions[state].append(i)
    
                        
    def transition_function(self, state):
        # if the game is over, return 0
        if state in self.terminal_states:
            return 0
        # if the game is not over, return the probabilities of each possible next action
        elif  len(self.actions[state]) == 1 : 
              return 1 
        else:
            return 1/(len(self.actions[state])-1)
    
    def generate_reward(self, state):
        if self.check_win(state)==1 : 
            return 1
        if self.check_win(state)==2:
            return -1 
        return 0
    
    def possible_next_states(self, state, action):
        new_state = list(state)
        new_state[action] = 1 # fill the case with X

        if self.check_win(new_state):
            return []
        
        # Then, look for all new possible states 
        possible_next_states = []
        
        for i, case in enumerate(new_state):
            next_new_state = new_state.copy()
            if case == 0:
                next_new_state[i] = 2
                possible_next_states.append(tuple(next_new_state))
        
        return possible_next_states
            
    
    
                
            
    
    
    