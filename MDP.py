import numpy as np

class MDP : 
    def __init__(self):
        self.states = set()
        self.terminal_states = set()
        self.actions = {}
        
        
    
    def generate_possible_states(self):
        
        # First generate all the board configurations possible and impossible ones 
        
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
            if self.check_win(state) or state.count(0) == 0 : 
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
    
    
    def value_iteration(self):
        
        theta = 10e-10
        delta = theta + 1  # the change in value estimates across all states
        discount_factor = 0.8
        
        init = [0 for _ in range (len(self.states))] 
        value_states = dict(zip(self.states , init)) # V_a(s) for each state
        best_action = dict(zip(self.states, init)) # for each state, determines best action to take (policy)
        
        while delta >= theta : 
            delta = 0 
            for state in self.states:
                print("current state is : ", state)
               
                
                if state in self.terminal_states : 
                    value_states[state] = self.generate_reward(state)
                    best_action[state] = None
                    continue
                
                v = value_states[state]
                best_value = float("-inf")
                
                for action in self.actions[state]:
                    # print("current action :", action)
                    possible_next_states = self.possible_next_states(state,action)
                    # print("possible next states : ", possible_next_states)
                    possible_value = 0 
                    
                    
                    for possible_next_state in possible_next_states:                        
                        possible_reward = self.generate_reward(possible_next_state)
                        transition_prob = self.transition_function(state)
                        # print(" self.transition_function(state) is :",  transition_prob)
                        # print("possible reward is : ", possible_reward)
                       
                        
                        possible_value += transition_prob * (possible_reward + (discount_factor * value_states[possible_next_state]))
                        # print ("possible v_s is : ", possible_value)
                       
                    
                    best_value  = max(best_value, possible_value)
                            
                value_states[state] = best_value # update the value of the current state
                best_action[state] = action  # store the best action for the state
                
                delta = max(delta, abs(v-value_states[state]))  #update delta 
                print("delta" , delta)
        
        return best_action
    
    
if __name__ == "__main__":
    mdp = MDP()
    mdp.generate_possible_states()
    #print ("all states are : ", toto.states)
    mdp.generate_terminal_states() # generate terminal states first because generate actions needs them
    # print("terminal states : ", toto.terminal_states)
    mdp.generate_actions()
    best_actions = mdp.value_iteration()
    print(best_actions)
                
                
            
    
    
    