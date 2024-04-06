import tkinter as tk
from tkinter import *
import subprocess

#from ..GameEngine import map


X_MENU_PADDING = 30
Y_MENU_PADDING = 30

class StartMenu:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x800")
        self.root.title("Bomberman Game")

        # Background Image
        self.bg = PhotoImage(file="bomberman_background.png")
        self.background_label = Label(self.root, image=self.bg)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame for white box
        self.white_box_frame = tk.Frame(self.root, bg="white")
        self.white_box_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER, relwidth=0.6, relheight=0.4)

        # Title
        self.label = tk.Label(self.white_box_frame, text='Welcome to the Bomberman game!', font=('New Times Roman', 20), bd=4, relief=tk.RAISED, bg='red')
        self.label.pack(pady=20)

        # Button Frame
        self.buttonframe = tk.Frame(self.white_box_frame, bg='white')
        self.buttonframe.pack(expand=True)

        # Create New Game Button
        self.create_game_button = tk.Button(self.buttonframe, text='Create New Game', font=('Arial', 18), bg='cyan', command=self.show_start_game)
        self.create_game_button.pack(pady=10)


        # Quit Button
        self.quit_button = tk.Button(self.buttonframe, text='Quit', font=('Arial', 18), bg='cyan', command=self.root.quit)
        self.quit_button.pack(pady=10)

       # self.center_window()  # Center the window
        self.root.mainloop()

    #       COMMENTED FOR NOW,REMOVE LATER. ITS FOR THE PLAYERS NAMES
    def show_start_game(self):   
        self.root.destroy()  # Close the main menu window
    #     player_count = 2  # Set the default player count
    #     startgame_window = StartGame(player_count)  # Pass the player count
    #
    #     startgame_window.mainloop()


    def temptestfunc(self):
        print("test activated")
        self.root.destroy()  # Close the main menu window

    def center_window(self):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width - self.root.winfo_width()) // 2
        y_coordinate = (screen_height - self.root.winfo_height()) // 2
        self.root.geometry("+{}+{}".format(x_coordinate, y_coordinate))

if __name__ == "__main__":
    StartMenu()