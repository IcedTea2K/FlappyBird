import pygame as pg

class Player:
    def __init__(self, pos, screen) -> None:
        self.screen = screen
        self.pos = pos
        self.state = 0 # 0 - yellow, 1 - blue, 2 - red
        self.currDir = 1 # 0 - up, 1 - mid, 2 - down
        self.sprites = []
        for bird in ['yellowbird', 'bluebird', 'redbird']:
            temp = []
            for dir in ['upflap', 'midflap', 'downflap']:
                str = "flappy-bird-assets/sprites/" + bird + "-" + dir+ ".png"
                temp.append(pg.image.load("flappy-bird-assets/sprites/" + bird + "-" + dir+ ".png"))
            self.sprites.append(temp)
    
    def display(self):
        self.screen.blit(self.sprites[self.state][self.currDir], self.pos)