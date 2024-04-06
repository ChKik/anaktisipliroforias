import pygame as pyg
import json

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class GameModel:
    def __init__(self, map_choice, player_count):
        pyg.init()
        self.display_w = 800
        self.display_h = 800
        self.tile_size = 50
        self.player_count = player_count  # Store player count
        self.load_map(map_choice)
        self.window = pyg.display.set_mode((self.display_w, self.display_h))
        self.windowclock = pyg.time.Clock()
        self.players = []

    def initialize_players(self):
        # Initialize players based on player_count
        if self.player_count == 2:
            self.players.append(Player(100, 100))  # Example positions, adjust as needed
            self.players.append(Player(700, 700))
        elif self.player_count == 3:
            self.players.append(Player(100, 100))
            self.players.append(Player(700, 700))
            self.players.append(Player(400, 400))

    def load_map(self, map_choice):
        map_files = {
            'map1': 'map1.json',
            'map2': 'map2.json',
            'map3': 'map3.json'
        }
        map_file = map_files.get(map_choice)
        if map_file is None:
            raise ValueError("Invalid map choice. Please choose map1, map2, or map3.")

        with open(map_file, 'r') as f:
            self.map_data = json.load(f)
        self.initialize_players()  # Initialize players after loading map

    def draw_map(self):
        for y, row in enumerate(self.map_data['layers'][0]['data']):
            for x, tile_id in enumerate(row):
                if tile_id != 0:  # 0 indicates an empty tile
                    tile_image = self.map_data['tilesets'][0]['tiles'][tile_id - 1]['image']
                    tile_image = pyg.image.load(tile_image)
                    self.window.blit(tile_image, (x * self.tile_size, y * self.tile_size))

    def draw_players(self):
        for player in self.players:
            # Draw player sprite or representation
            pyg.draw.circle(self.window, (255, 0, 0), (player.x, player.y), 20)  # Placeholder drawing

    def Map(self):
        running = True
        while running:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    running = False

            self.window.fill((255, 255, 255))
            self.draw_map()
            self.draw_players()
            pyg.display.update()
            self.windowclock.tick(60)

if __name__ == "__main__":
    try:
        map_choice = input("Choose map (map1, map2, map3): ")
        game = GameModel(map_choice.strip(), 2)  # Example player count
        game.Map()
    except EOFError:
        print("\nInput was terminated unexpectedly. Please provide valid input.")

