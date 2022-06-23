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
                temp.append(pg.image.load("flappy-bird-assets/sprites/" + bird + "-" + dir+ ".png"))
            self.sprites.append(temp)
    
    def display(self):
        img = self.sprites[self.state][self.currDir]
        rect = img.get_rect()
        rect.center = self.pos
        self.screen.blit(img, rect)