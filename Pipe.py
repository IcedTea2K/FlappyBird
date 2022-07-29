import pygame as pg
class Pipe:
    def __init__(self, screen, speed) -> None:
        self.screen = screen
        self.speed = speed
        # Appearance and location 
        self.pipes = []
        for i, type in enumerate(["green", "red"]):
            self.pipes.append(pg.image.load("flappy-bird-assets/sprites/pipe-" + type + ".png"))
            self.pos = (pg.display.get_surface().get_width(), pg.display.get_surface().get_height() - 112)

    def move(self):
       pass 

    def display(self):
        self.screen.blit(self.pipes[0], self.pipes[0].get_rect(centerx=self.pos[0], bottom = self.pos[1])) 
        pass
