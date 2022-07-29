import pygame as pg
class Pipe:
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

    def move(self):
       self.pos[0] -= self.speed 
       print(self.pos)

    def display(self):
        self.move()
        self.screen.blit(self.pipes, self.pipes.get_rect(left=self.pos[0], bottom = self.pos[1])) 
