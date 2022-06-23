import sys
import pygame as pg
pg.init()

# Setting up the window
size = width, height = 288,512
speed = [2,2]
screen  = pg.display.set_mode(size) # create scene
pg.display.set_caption("Flappy Bird")
icon = pg.image.load("flappy-bird-assets/favicon.png")
pg.display.set_icon(icon)

# Background
dayBg = pg.image.load("flappy-bird-assets/sprites/background-day.png")
nightBg = pg.image.load("flappy-bird-assets/sprites/background-night.png")
# Player
playerImg = pg.image.load("flappy-bird-assets/sprites/bluebird-midflap.png")

# Game Loop
while True:
    screen.fill((255,128,255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit() # exit the program if the window is closed

    screen.blit(dayBg, (0,0)) # draw the background
    screen.blit(playerImg, (width/2, height/2)) 
    pg.display.update()