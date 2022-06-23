import sys
import pygame as pg
pg.init()

# Setting up the Screen
size = width, height = 320,240
speed = [2,2]
screen  = pg.display.set_mode(size) # create scene
pg.display.set_caption("Flappy Bird")
icon = pg.image.load("flappy-bird-assets/favicon.png")
pg.display.set_icon(icon)

# Game Loop
while True:
    screen.fill((255,128,255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit() # exit the program if the window is closed

    pg.display.update()