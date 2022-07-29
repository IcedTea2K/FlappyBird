import pygame as pg
import random
class Pipe:
    GAP = 100
    def __init__(self, screen, mode, speed) -> None:
        type = ["green", "red"]
        self.screen = screen
        self.speed = speed
        # Appearance and location 
        self.pipes = []
        if mode == 0:
            self.pipes = pg.image.load("flappy-bird-assets/sprites/pipe-" + "green" + ".png")
        else:
            self.pipes = pg.image.load("flappy-bird-assets/sprites/pipe-" + "red" + ".png") 
        self.pos = [pg.display.get_surface().get_width(), pg.display.get_surface().get_height() - 112]
        w,h = self.pipes.get_size()
        self.botPipe = pg.transform.scale(self.pipes, (w, h*random.random())) # do not have to keep the original because it's only resized once
        w,h = self.botPipe.get_size()
        self.topPipe = pg.transform.scale(self.pipes, (w, self.pos[1] - h - self.GAP))
        self.topPipe = pg.transform.flip(self.topPipe, False, True)

    def move(self):
       self.pos[0] -= self.speed 

    def display(self):
        self.move()
        self.screen.blit(self.botPipe, self.botPipe.get_rect(left=self.pos[0], bottom = self.pos[1]))
        self.screen.blit(self.topPipe, self.pipes.get_rect(left=self.pos[0], top = 0))
        print(self.pipes.get_size())  
