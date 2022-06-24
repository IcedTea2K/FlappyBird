import pygame as pg

class Player:
    velocity = pg.Vector2(0,1)
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
        self.img =  self.sprites[self.state][self.currDir]
        self.rect = self.img.get_rect()
    
    def move(self):
        self.pos += self.velocity
    
    def detect(self, baseRect, pipeRect):
        if self.rect.colliderect(baseRect):
            return "base"
        elif self.rect.colliderect(pipeRect):
            return "pipe"
        return None

    def display(self, baseRect, pipeRect):
        if self.detect(baseRect, pipeRect) is None:
            self.move()
        
        self.rect.center = self.pos
        self.screen.blit(self.img, self.rect)