import pygame as pg
class Pipe:
    def __init__(self, screen, speed) -> None:
        self.screen = screen
        self.speed = speed
        # Appearance and location 
        self.pipes = []
        self.pipesRect = []
        for i, type in enumerate(["green", "red"]):
            self.pipes.append(pg.image.load("flappy-bird-assets/sprites/pipe-" + type + ".png"))
            self.pipesRect.append(self.pipes[i].get_rect())
            self.pipesRect[i].centerx = pg.display.get_surface().get_width()
            self.pipesRect[i].bottom = pg.display.get_surface().get_height() - 56
        pass

    def move(self):
       pass 

    def display(self):
        self.screen.blit(self.pipes[0], self.pipesRect[0]) 
        pass