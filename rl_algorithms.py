import random
from MDP import MDP


class PolicyIteration (MDP) : 
    def __init__(self, threshold=10e-10, discount_factor=0.9): 
        super().__init__() # Inherit all the methods and attributes oh MDP
        self.is_stable = False
        self.theta = threshold # convergence threshold 
        self.discount_factor = discount_factor
        
        self.generate_possible_states()
        self.generate_terminal_states()
        self.generate_actions()
        
        # self.init = [0 for _ in range (len(self.states))] 
        self.v_s = dict(zip(self.states , [0 for _ in range (len(self.states))]))
        self.policy = dict(zip(self.states, [random.randint(0,8) for _ in range(len(self.states))]))
        
        print (self.policy[(2, 1, 0, 1, 2, 0, 0, 0, 1)])
        
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
    agent = PolicyIteration()
    agent.policy_iteration()
    print(agent.policy)                 
            
                
        

