import pygame as pyg

pyg.init()

DISPLAY_W = 800
DISPLAY_H = 800
TILE_SIZE = 50     #creates a 16x16 map,so 256 tiles in total

#map colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (4,238,161)
BROWN =(255,222,173)

playersNumber=2
def threeplayers():
    playersNumber=3


class GameModel():
    def __init__(self):
        self.widthMap = DISPLAY_W
        self.heightMap = DISPLAY_H
        
        window.fill(GREEN)
        

    def Map(self):
        
        #variables here



        # Event handler
        while True:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    quit()


            
            
            pyg.display.update()
            windowclock.tick(60)


window = pyg.display.set_mode((DISPLAY_W, DISPLAY_H))
if pyg.display.get_init is not True:
    print("error at initializatinon")
     

windowclock = pyg.time.Clock()

game = GameModel()
game.Map()