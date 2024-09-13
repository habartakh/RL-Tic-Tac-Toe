import numpy as np

class MDP : 
    def __init__(self):
        self.states = set()
        self.terminal_states = set()
        self.actions = {}
        self.value_iter_policy = {}
        self.policy_iter_policy = {}
        
        
    
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
        theta = 10e-50
        delta = theta + 1  # the change in value estimates across all states
        discount_factor = 0.95
        
        init = [0 for _ in range (len(self.states))] 
        value_states = dict(zip(self.states , init)) # V_a(s) for each state
        self.value_iter_policy = dict(zip(self.states, init)) # for each state, determines best action to take (policy)
        
        while delta >= theta : 
            delta = 0 
            for state in self.states:             
                if state in self.terminal_states : 
                    value_states[state] = self.generate_reward(state)
                    self.value_iter_policy[state] = None
                    continue
                
                v = value_states[state]
                best_value = float("-inf")
                
                for action in self.actions[state]:
                    possible_next_states = self.possible_next_states(state,action)
                    possible_value = 0 
                    for possible_next_state in possible_next_states:                        
                        possible_reward = self.generate_reward(possible_next_state)
                        transition_prob = self.transition_function(state)
                        possible_value += transition_prob * (possible_reward + (discount_factor * value_states[possible_next_state]))
                       
                    if  possible_value > best_value : 
                        best_value  = possible_value
                        best_action = action
                            
                value_states[state] = best_value # update the value of the current state
                self.value_iter_policy[state] = best_action  # store the best action for the state
                
                delta = max(delta, abs(v-value_states[state]))  #update delta 
    
    
    # def policy_evaluation(self , policy):
    #     theta = 10e-50
    #     delta = theta + 1  # the change in value estimates across all states
    #     discount_factor = 0.95
        
    #     init = [0 for _ in range (len(self.states))] 
    #     value_states = dict(zip(self.states , init)) # V_a(s) for each state
        
    #     # Policy Evaluation
    #     while delta >= theta : 
    #         delta = 0 
    #         for state in self.states : 
    #             if state in self.terminal_states : 
    #                 print ("state in terminal_states")
    #                 continue
                
    #             expected_value = 0 
    #             v = value_states[state]
    #             action = policy[state]
    #             for possible_state in self.possible_next_states(state, action) : 
    #                 transition_prob = self.transition_function(possible_state)
    #                 expected_reward = self.generate_reward(possible_state)
    #                 expected_value += transition_prob * (expected_reward + discount_factor *value_states[possible_state])
                    
    #             value_states[state] = expected_value
                
    #         delta = max (delta, abs(v-value_states[state]))
    #         return value_states
        
        
    # def policy_iteration(self):
        
    #     self.policy_iter_policy =  self.value_iter_policy
    #     policy_eval_states = self.policy_evaluation(self.policy_iter_policy)
    #     # Policy Improvement 
        
    #     policy_stable = True
    #     for state in self.states :
    #         old_action = self.policy_iter_policy[state]
            
    #         # Update policy value for each state : self.policy_iter_policy[state]
    #          for action in self.actions[state]:
    #                 possible_next_states = self.possible_next_states(state,action)
    #                 possible_value = 0 
    #                 for possible_next_state in possible_next_states:                        
    #                     possible_reward = self.generate_reward(possible_next_state)
    #                     transition_prob = self.transition_function(state)
    #                     possible_value += transition_prob * (possible_reward + (discount_factor * value_states[possible_next_state]))
                       
    #                 best_value  = max(best_value, possible_value)
    #         self.policy_iter_policy[state] = 
            
            
    #         if old_action != self.policy_iter_policy[state] : 
    #             policy_stable = False 
        
    #     if policy_stable : 
    #         return policy_eval_states
        
    #     else : 
    #          policy_eval_states = self.policy_evaluation(self.policy_iter_policy)
    
    
    
    
    def generate_policy (self):
        self.generate_possible_states()
        self.generate_terminal_states()
        self.generate_actions()
        self.value_iteration()
    
    
if __name__ == "__main__":
    mdp = MDP()
    mdp.generate_policy()
    print(mdp.policy)
    # if ((0,0,0,0,0,0,0,0,0) in mdp.policy.keys()):
    #     print (mdp.policy[(0,0,0,0,0,0,0,0,0)])
                
                
            
    
    
    