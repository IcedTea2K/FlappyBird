from hmac import new
import pygame as pg

class Player:
    velocity = pg.Vector2(0,0)
    fallForce = pg.Vector2(0, 0.25)
    flyForce = pg.Vector2(0,-1.75)
    currForce = pg.Vector2(0,0)
    prevPos = pg.Vector2(0.0)
    topHeight = 20
    def __init__(self, pos, screen) -> None:
        self.screen = screen
        self.pos = pos
        self.prevPos.update(self.pos)
        self.state = 0 # 0 - yellow, 1 - blue, 2 - red
        self.fly = False
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
        if self.fly is True:
            self.velocity.y = 0
            self.currForce += self.flyForce
            self.fly = False
        if self.currForce != self.fallForce: self.currForce += self.fallForce

        # if self.fly is True:
        #     self.velocity += self.flyForce
        #     self.fly = False
        
        # if self.fly is True:
        #     if self.pos.y >= (self.prevPos.y -self.topHeight):
        #         self.velocity += self.flyForce
        #     else:
        #         self.fly = False
        #     print("pos: " + str(self.pos) + "     " + "top: " + str (self.prevPos.y - self.topHeight))
            # print(self.fly)
        print(str(self.currForce) + " " + str(self.velocity))
        self.velocity += self.currForce
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