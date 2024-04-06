import tkinter as tk
from tkinter import messagebox
import subprocess

class StartGame(tk.Tk):
    def __init__(self, player_count):
        super().__init__()
        self.title("Start Game")
        self.geometry("400x250")  # Increased height to accommodate player selection

        self.player_count = player_count
        self.players = []

        for i in range(self.player_count):
            self.create_player_entry(i)

        self.enter_button = tk.Button(self, text='Enter', font=('Arial', 12), bg='cyan', command=self.enter_names)
        self.enter_button.pack(pady=10)

    def create_player_entry(self, player_number):
        label = tk.Label(self, text=f'Enter Player {player_number + 1}\'s Name:', font=('New Times Roman', 14))
        label.pack(pady=5)

        entry = tk.Entry(self, font=('Arial', 12))
        entry.pack(pady=5)

        self.players.append(entry)

    def enter_names(self):
        names = [entry.get() for entry in self.players]
        if any(name.strip() == '' for name in names):
            messagebox.showerror("Error", "Please enter all player names.")
        else:
            self.destroy()  # Close the name entry window
            map_selection = MapSelection(names)  # Pass player names
            map_selection.mainloop()

class MapSelection(tk.Tk):
    def __init__(self, names):
        super().__init__()
        self.title("Map Selection")
        self.geometry("400x200")
        self.names = names

        self.label = tk.Label(self, text=f'Hello {", ".join(names)}! Choose a Map:', font=('New Times Roman', 14))
        self.label.pack(pady=10)

        self.map1_button = tk.Button(self, text='Map 1', font=('Arial', 12), bg='cyan', command=lambda: self.select_map(1))
        self.map1_button.pack(pady=5)

        self.map2_button = tk.Button(self, text='Map 2', font=('Arial', 12), bg='cyan', command=lambda: self.select_map(2))
        self.map2_button.pack(pady=5)

        self.map3_button = tk.Button(self, text='Map 3', font=('Arial', 12), bg='cyan', command=lambda: self.select_map(3))
        self.map3_button.pack(pady=5)

    def select_map(self, map_number):
        self.destroy()  # Close the current window
        messagebox.showinfo("Map Selected", f"You selected Map {map_number}.\nStarting the game...")

        # Launch the game window with selected map and player names
        subprocess.Popen(["python3", "GameModel.py", str(map_number), ",".join(self.names)])


if __name__ == "__main__":
    start_game_window = StartGame(2)  # Default to 2 players
    start_game_window.mainloop()