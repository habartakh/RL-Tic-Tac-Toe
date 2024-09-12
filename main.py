import random
import tkinter as tk
from tkinter import messagebox
from MDP import MDP

class TicTacToe:
    def __init__(self, main_window, agent):
        self.window = main_window
        self.window.title("Tic Tac Toe")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                self.window,
                text=" ",
                fg="red",
                font=("Arial", 24),
                width=10,
                height=5,
                command=lambda row=i, col=j: self.on_button_click(row, col))
                # put the buttons in a grid structure 
                self.buttons[i][j].grid(row=i, column=j)
                
        # Game information 
        self.current_player = 1
        self.current_player_symbol = "x"
        self.game_set  = False
        self.game_board = [0 for _ in range(9)] # will be filled with "x" or "o"
        
        self.agent = agent 
        self.agent.generate_policy()
        self.agent_move()

        
    # when clicking on a button, fill it with the appropriate text 
    def on_button_click(self, row, col):
        if(self.game_board[row*3+col] == 0):
            self.buttons[row][col].configure(text = self.current_player_symbol)
            self.game_board[row*3+col] = self.current_player
              
        if self.check_winner() :
            if self.show_winner_message() : # Player clicked on YES button
                self.reset_game() # Play another round 
            else : # Player clicked on NO button
                self.window.destroy() # Close the game 
        
        elif self.check_draw() : 
           if  self.show_draw_message() : 
               self.reset_game()
           else : 
               self.window.destroy()
                 
        else : 
            self.switch_player() 
            if self.current_player == 1 : 
                self.agent_move()
        
        
    
    def check_winner(self):
       for i in range(3):
           if self.game_board[i*3] == self.game_board[i*3+1] == self.game_board[i*3+2] != 0 :
               return self.game_board[i*3]
        
           if self.game_board[i] ==self.game_board[3+i] == self.game_board[6+i] != 0 :
               return self.game_board[i]
        
       if self.game_board[4] == self.game_board[6] == self.game_board[2] and self.game_board[4] != 0 : 
            return  self.game_board[4]
        
       elif self.game_board[0] == self.game_board[4] == self.game_board[8] and self.game_board[0] != 0  :
            return self.game_board[0] 
        
       return False
        
    
    def show_winner_message(self):
        return messagebox.askyesno(None, "Player " + self.current_player_symbol + " won. Do you wish to play another round?")
      
    def show_draw_message(self) : 
        return messagebox.askyesno(None, "The game ended in a draw. Wanna try your luck again?")
        
    def check_draw(self):
        if (0 in self.game_board) == False and self.check_winner() == False :
            return True
        return False 
        
    def switch_player(self):
        if self.current_player == 1 : 
            # print ("current player is X. Switching to O")
            self.current_player = 2
            self.current_player_symbol = "o"
        
        else :
           # print ("current player is O. Switching to X")
            self.current_player = 1
            self.current_player_symbol = "x"
                
    def reset_game(self):
       for i in range (3):
           for j in range (3) : 
               self.buttons[i][j].configure(text = " ")
               self.game_board[i*3+j] = 0
       self.current_player = 1
       self.current_player_symbol ="x"
       self.agent_move()
               
   
    def agent_move(self):
        if self.game_board == [0,0,0,0,0,0,0,0,0] : 
            action = random.randint(0, 8)
        
        else : 
            action = self.agent.policy[tuple(self.game_board)]
            print ("action to take is : ", action)
        
        if action != None :  # in case action = None , do nothing 
            row = int (action / 3)
            col = int (action % 3)
            print ("Invoke button action")
            self.buttons[row][col].invoke()
            
                
    def run_game(self):
        # game will continue till there is a winner or a draw
        # self.agent_move()
        self.window.mainloop()
            
    
if __name__ == "__main__":
    main_window = tk.Tk()
    agent = MDP()
    game = TicTacToe(main_window, agent)
    game.run_game()
    
    
 
    