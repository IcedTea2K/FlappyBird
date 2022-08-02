import pygame as pg
import random
class Pipe:
    GAP = 100
    def __init__(self, screen, mode, speed) -> None:
        self.screen = screen
        self.speed = speed
        # Appearance and location 
        if mode == 0:
            self.pipe = pg.image.load("flappy-bird-assets/sprites/pipe-" + "green" + ".png")
        else:
            self.pipe = pg.image.load("flappy-bird-assets/sprites/pipe-" + "red" + ".png") 
        self.pos = [pg.display.get_surface().get_width(), pg.display.get_surface().get_height() - 112]
        w,h = self.pipe.get_size()
        self.botPipe = pg.transform.scale(self.pipe, (w, h*random.random())) # do not have to keep the original because it's only resized once
        self.botRect = self.botPipe.get_rect(left=self.pos[0], bottom = self.pos[1])
        w,h = self.botPipe.get_size()
        if not self.pos[1] - h - self.GAP <= 0:
            self.topPipe = pg.transform.scale(self.pipe, (w, self.pos[1] - h - self.GAP))
            self.topPipe = pg.transform.flip(self.topPipe, False, True) # flip to the top of the window
            self.topRect = self.topPipe.get_rect(left=self.pos[0], top = 0)
        else:
            self.topPipe = None
            self.topRect = None

    def move(self):
       self.pos[0] -= self.speed
       self.botRect.x = self.pos[0]
       if self.topPipe is not None:
            self.topRect.x = self.pos[0]

    def get_rect(self):
        if self.topPipe is None:
            return (self.botRect,)
        return (self.botRect, self.topRect)

    def display(self,moving):
        if moving:
            self.move()
        self.screen.blit(self.botPipe, self.botRect)
        if self.topPipe is not None:
            self.screen.blit(self.topPipe, self.topRect)
