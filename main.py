import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class TicTacToe:
    def __init__(self, main_window):
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
        self.current_player = "x"
        self.game_set  = False
        self.game_board = [[" " for _ in range(3)] for _ in range(3)] # will be filled with "x" or "o"

        
    # when clicking on a button, fill it with the appropriate text 
    def on_button_click(self, row, col):
        if(self.game_board[row][col] == " "):
            self.buttons[row][col].configure(text = self.current_player)
            self.game_board[row][col] = self.current_player
            
       
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
        
        
    def check_winner(self):
        for row in self.game_board : 
            if row[0] == row[1] == row[2] != " " :
                return True
        
        for col in range (3):
            if self.game_board[0][col] == self.game_board[1][col] == self.game_board[2][col] != " " :
                return True 
        
        
        if (self.game_board[0][0] == self.game_board[1][1] == self.game_board[2][2] != " "
        or self.game_board[0][2] == self.game_board[1][1] == self.game_board[2][0] != " "):
            return True 
        
        return False
        
    def show_winner_message(self):
        return messagebox.askyesno(None, "Player " + self.current_player + " won. Do you wish to play another round?")
      
    def show_draw_message(self) : 
        return messagebox.askyesno(None, "The game ended in a draw. Wanna try your luck again?")
        
    def check_draw(self):
        if any(" " in row for row in self.game_board) == False and self.check_winner()==False :
            return True
        return False 
        
    def switch_player(self):
       # print ("Inside switch player method !")
        if self.current_player == "x" : 
            # print ("current player is X. Switching to O")
            self.current_player = "o"
        
        else :
           # print ("current player is O. Switching to X")
            self.current_player = "x"
                
    def reset_game(self):
       for i in range (3):
           for j in range (3) : 
               self.buttons[i][j].configure(text = " ")
               self.game_board[i][j] = " "
       self.current_player = "x"
               
               
    def run_game(self):
        # game will continue till there is a winner or a draw
        self.window.mainloop()
            
    
if __name__ == "__main__":
    main_window = tk.Tk()
    game = TicTacToe(main_window)
    game.run_game()
    
    
 
    