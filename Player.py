import pygame as pg
class Player:
    def __init__(self, pos, screen, clock) -> None:
        # Game's Variables 
        self.screen = screen
        self.clock = clock
        # Initial State and Appearance
        self.sprites = []
        self.fly = False
        self.state = 0  # 0 - yellow, 1 - blue, 2 - red
        self.currDir = 1  # 0 - up, 1 - mid, 2 - down
        for bird in ['yellowbird', 'bluebird', 'redbird']:
            temp = []
            for dir in ['upflap', 'midflap', 'downflap']:
                temp.append(pg.image.load("flappy-bird-assets/sprites/" + bird + "-" + dir+ ".png"))
            self.sprites.append(temp)
        self.img =  self.sprites[self.state][self.currDir]
        self.rect = self.img.get_rect()
        # Birds characteristics - acceleration, speed, position, and rotation
        self.velocity = pg.Vector2(0,0)
        self.fallForce = pg.Vector2(0, 0.25)
        self.flyForce = pg.Vector2(0,-1.75)
        self.currForce = pg.Vector2(0,0)
        self.currAngle = 0 # current rotation 
        self.pos = pos
    
    def rotateImg(self, angle: float): # rotate the image counter clock-wise 
        # https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
        imgCenter = self.pos - pg.math.Vector2(self.rect.center)
        rotatedCenter = imgCenter.rotate(-angle)  # vector2.rotate is inverted to pygame.rotate
        newImgCenterPos = self.pos - rotatedCenter

        rotatedRect = self.img.get_rect(center=newImgCenterPos)
        rotatedImg = pg.transform.rotate(self.img, angle)
        return rotatedImg, rotatedRect

    def move(self):
        if self.fly is True:
            self.velocity.y = 0
            self.currForce += self.flyForce
            self.currAngle = 20 # rotate the bird upward when spacebar is pressed
            self.fly = False
        if self.currForce != self.fallForce: self.currForce += self.fallForce

        self.velocity += self.currForce
        
        self.pos += self.velocity
        if self.pos.y > self.screen.get_height() - 112:
            self.pos.y = self.screen.get_height() - 112 
        if self.velocity.y >= 4 and self.currAngle > -90:
            self.currAngle -= 5

    def animate(self):
        frameCount = ((pg.time.get_ticks() / 1000) * 60)%60
        self.img = self.sprites[self.state][int(frameCount / 5) % len(self.sprites[self.state])]
        self.rect = self.img.get_rect()

    def display(self, baseRect, pipeRect, gameState):
        self.rect.center = self.pos
        surface, newRect= self.rotateImg(self.currAngle) # newRect is the calculated position after being rotated
        self.screen.blit(surface, newRect)
        if newRect.colliderect(baseRect):
            return False
        else:
            if gameState >= 1:
                self.move()

        if any([newRect.colliderect(x) for x in pipeRect]) or (self.pos.y < 0 and any([pipe.x < self.pos.x for pipe in pipeRect])):
            self.fallForce.y = 1
            self.currForce.y = 0  # reset the velocity and acceleration to make falling seems
            self.velocity.y = 0 if self.velocity.y < 0 else self.velocity.y # more abrupt 
            return False        

        self.animate()
        return True # still alive 
        