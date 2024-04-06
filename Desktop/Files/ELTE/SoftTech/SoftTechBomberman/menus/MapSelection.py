import tkinter as tk
from tkinter import messagebox
from GameModel import GameModel
from StartGame import StartGame

class MapSelection(tk.Tk):
    def __init__(self, name, player_count):
        super().__init__()
        self.title("Map Selection")
        self.geometry("400x200")
        self.name = name
        self.player_count = player_count  # Store player count

        self.label = tk.Label(self, text=f'Hello {name}! Choose a Map:', font=('New Times Roman', 14))
        self.label.pack(pady=10)

        self.map_buttons = []  # Store map buttons to access them later

        # Create buttons for each map
        for i in range(1, 4):
            map_button = tk.Button(self, text=f'Map {i}', font=('Arial', 12), bg='cyan', command=lambda num=i: self.select_map(num))
            map_button.pack(pady=5)
            self.map_buttons.append(map_button)

    def select_map(self, map_number):
        map_file = f"map{map_number}.json"  # Assuming map files are named as map1.json, map2.json, map3.json
        self.destroy()  # Close the current window
        messagebox.showinfo("Map Selected", f"You selected Map {map_number}.\nStarting the game...")

        # Launch the game window with selected map and player count
        game = GameModel(map_file, self.player_count)
        game.Map()

if __name__ == "__main__":
    name = input("Enter your name: ")
    player_count = int(input("Enter the number of players: "))
    map_selection = MapSelection(name, player_count)
    map_selection.mainloop()
