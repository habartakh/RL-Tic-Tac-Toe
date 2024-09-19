import random
from MDP import MDP

class ValueIteration(MDP):
    def __init__(self, threshold=10e-10,discount_factor=0.9):
        super().__init__() # Inherit all the methods and attributes of MDP
        self.theta = threshold # convergence threshold 
        self.discount_factor = discount_factor
        
        self.generate_possible_states()
        self.generate_terminal_states()
        self.generate_actions()
         
        init = [0 for _ in range (len(self.states))] 
        self.v_a = dict(zip(self.states,init)) # V_a(s) for each state s
        self.policy = dict(zip(self.states,init)) # for each state, determines best action to take (policy)
        
        
    def value_iteration(self):
        delta = self.theta + 1
        
        while delta >= self.theta : 
          delta = 0 
          for state in self.states:             
              if state in self.terminal_states : 
                  self.v_a[state] = self.generate_reward(state)
                  self.policy[state] = None
                  continue
              
              v = self.v_a[state]
              best_value = float("-inf")
              
              for action in self.actions[state]:
                  possible_next_states = self.possible_next_states(state,action)
                  possible_value = 0 
                  for possible_next_state in possible_next_states:                        
                      possible_reward = self.generate_reward(possible_next_state)
                      transition_prob = self.transition_function(state)
                      possible_value += transition_prob * (possible_reward + (self.discount_factor * self.v_a[possible_next_state]))
                     
                  if  possible_value > best_value : 
                      best_value  = possible_value
                      best_action = action
                          
              self.v_a[state] = best_value # update the value of the current state
              self.policy[state] = best_action  # store the best action for the state
              
              delta = max(delta, abs(v-self.v_a[state]))  #update delta 
    
    
    
class PolicyIteration(MDP): 
    def __init__(self, threshold=10e-10, discount_factor=0.9): 
        super().__init__()
        self.is_stable = False
        self.theta = threshold # convergence threshold 
        self.discount_factor = discount_factor
        
        self.generate_possible_states()
        self.generate_terminal_states()
        self.generate_actions()
        
        self.v_s = {}
        self.policy = {}
        
        for state in self.states : 
            self.v_s[state] = 0 
            self.policy[state] = random.choice(self.actions[state]) if self.actions[state] else None
        
        
    def policy_evaluation(self): 
        converge = False
        while converge == False : 
            delta = 0
            for state in self.states : 
                if state in self.terminal_states : 
                    self.v_s[state] = self.generate_reward(state)
                    continue
                
                v = self.v_s[state]
                action = self.policy[state]
                self.v_s[state] = 0 
                
                for possible_next_state in self.possible_next_states(state,action):
                    if possible_next_state in self.states :
                        reward =  self.generate_reward(possible_next_state)
                        self.v_s[state] += reward + self.discount_factor * self.v_s[possible_next_state]
                
                delta = max(delta, abs(self.v_s[state] - v))
                
            if delta < self.theta :
                converge = True
                
                
    def policy_improvement(self):
        change_happened = False
        for state in self.states : 
            if state in self.terminal_states:
                continue 
            
            temp = self.policy[state]
            best_value = float("-inf")
            for action in self.actions[state] : 
                expected_value = 0 
                for possible_next_state in self.possible_next_states(state,action): 
                    expected_value += self.transition_function(possible_next_state) * self.v_s[possible_next_state]
               
                if expected_value > best_value : 
                    best_value = expected_value
                    self.policy[state] = action 
            if temp !=   self.policy[state] : 
                change_happened = True

        return change_happened   


    def policy_iteration(self): 
        while self.is_stable == False : 
            self.policy_evaluation()
            change = self.policy_improvement()
            
            if change == False : 
                self.is_stable = True
                
                
if __name__ == "__main__" : 
    agent1 = ValueIteration()
    agent1.value_iteration()
    print(agent1.policy)
    # agent2 = PolicyIteration()
    # agent2.policy_iteration()
    # print(agent2.policy)                 
            
                
        

