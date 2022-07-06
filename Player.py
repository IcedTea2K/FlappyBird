import pygame as pg
class Player:
    velocity = pg.Vector2(0,0)
    fallForce = pg.Vector2(0, 0.25)
    flyForce = pg.Vector2(0,-1.75)
    currForce = pg.Vector2(0,0)
    def __init__(self, pos, screen, clock) -> None:
        self.screen = screen
        self.clock = clock
        self.pos = pos
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
    
    def map(self, val: float, old: tuple, new: tuple) -> float:
        xRange = old[1] - old[0] # old range
        yRange = new[1] - new[0] # new range
        ratio = float(val - old[0]) / float(xRange)
        return new[0] + (ratio * yRange)

    def move(self):
        if self.fly is True:
            self.velocity.y = 0
            self.currForce += self.flyForce
            self.fly = False
        if self.currForce != self.fallForce: self.currForce += self.fallForce

        self.velocity += self.currForce
        self.pos += self.velocity
    
    def detect(self, baseRect, pipeRect):
        if self.rect.colliderect(baseRect):
            return "base"
        elif self.rect.colliderect(pipeRect):
            return "pipe"
        return None

    def animate(self):
        frameCount = ((pg.time.get_ticks() / 1000) * 60)%60
        self.img = self.sprites[self.state][int(frameCount / 5) % len(self.sprites[self.state])]
        self.rect = self.img.get_rect()

    def display(self, baseRect, pipeRect):
        if self.detect(baseRect, pipeRect) is None:
            self.move()
        self.animate()
        self.rect.center = self.pos
        self.screen.blit(self.img, self.rect)
        