import pygame as pg
class Player:
    def __init__(self, pos: pg.Vector2, screen: pg.Surface, clock: pg.time.Clock) -> None:
        """A class for bird -- the main character"""
        # Game's Variables 
        self.screen = screen
        self.clock = clock
        # Initial State and Appearance
        self.sprites = [] # 2D array containing 3 colors each of which has 3 different flapping sprites
        self.fly = False
        self.state = 0  # 0 - yellow, 1 - blue, 2 - red
        for bird in ['yellowbird', 'bluebird', 'redbird']:
            temp = []
            for dir in ['upflap', 'midflap', 'downflap']:
                temp.append(pg.image.load("flappy-bird-assets/sprites/" + bird + "-" + dir+ ".png"))
            self.sprites.append(temp)
        self.img =  self.sprites[self.state][1]
        self.rect = self.img.get_rect()
        # Birds characteristics - acceleration, speed, position, and rotation
        self.velocity = pg.Vector2(0,0)
        self.fallForce = pg.Vector2(0, 0.25) # although force, it is also acceleration as bird is 1 unit in mas
        self.flyForce = pg.Vector2(0,-1.75)
        self.currForce = pg.Vector2(0,0) # final added up force
        self.currAngle = 0 # current rotation 
        self.pos = pg.Vector2(0,0)
        self.initPos = pg.Vector2(0,0)
        self.pos.update(pos)
        self.initPos.update(pos)
    
    def rotateImg(self, angle: float) -> None:
        """
        rotate the image counter clock-wise
        https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
        """
        imgCenter = self.pos - pg.math.Vector2(self.rect.center)
        rotatedCenter = imgCenter.rotate(-angle)  # vector2.rotate is inverted to pygame.rotate
        newImgCenterPos = self.pos - rotatedCenter

        rotatedRect = self.img.get_rect(center=newImgCenterPos)
        rotatedImg = pg.transform.rotate(self.img, angle)
        return rotatedImg, rotatedRect

    def move(self) -> None:
        """Move the bird based on user input and physics"""
        if self.fly is True:
            self.velocity.y = 0
            self.currForce += self.flyForce
            self.currAngle = 20 # rotate the bird upward when spacebar is pressed
            self.fly = False
        if self.currForce != self.fallForce: self.currForce += self.fallForce

        self.velocity += self.currForce # calculate the velocity
        self.pos += self.velocity # calculate the new position

        if self.pos.y > self.screen.get_height() - 112: # prevent bird from landing deep in the ground
            self.pos.y = self.screen.get_height() - 112 
        if self.velocity.y >= 4 and self.currAngle > -90: # boundaries for bird rotation
            self.currAngle -= 5

    def animate(self) -> None:
        """Animate the bird flapping"""
        # milis / 1000 = s * 60 = # of frame passed % 60 = current frame within 60fps cycle
        frameCount = ((pg.time.get_ticks() / 1000) * 60)%60 
        self.img = self.sprites[self.state][int(frameCount / 5) % len(self.sprites[self.state])] # frameCount/5 controls how fast is the animation
        self.rect = self.img.get_rect()

    def reset(self) -> None:
        """Reset all bird's stats"""
        self.state = 0
        self.pos.update(self.initPos)
        self.velocity = pg.Vector2(0,0)
        self.fallForce = pg.Vector2(0, 0.25)
        self.flyForce = pg.Vector2(0,-1.75)
        self.currForce = pg.Vector2(0,0)
        self.currAngle = 0 # current rotation 

    def display(self, baseRect: pg.Rect, pipeRect: pg.Rect, gameState: int):
        """Display the bird onto the screen while checking for collision"""
        self.rect.center = self.pos
        surface, newRect= self.rotateImg(self.currAngle) # newRect is the calculated position after being rotated
        self.screen.blit(surface, newRect)
        if newRect.colliderect(baseRect):
            return False # Dead
        else:
            if gameState >= 1: # physics still work even when bird hits pipe and dies
                self.move()

        if any([newRect.colliderect(x) for x in pipeRect]) or (self.pos.y < 0 and any([pipe.x < self.pos.x for pipe in pipeRect])):
            # check for collision
            self.fallForce.y = 1
            self.currForce.y = 0  # reset the velocity and acceleration to make falling seems
            self.velocity.y = 0 if self.velocity.y < 0 else self.velocity.y # more abrupt 
            return False # Dead

        self.animate()
        return True # still alive 
        