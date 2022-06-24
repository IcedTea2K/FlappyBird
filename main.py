import sys
import pygame as pg
from Player import *
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
base =  pg.image.load("flappy-bird-assets/sprites/base.png")
baseRect = base.get_rect()
baseRect.center = width/2, height-56
# Scores
score = []
scoreRect = []
for i in range(10):
    score.append(pg.image.load("flappy-bird-assets/sprites/" + str(i) + ".png"))
    scoreRect.append(score[i].get_rect())
    scoreRect[i].center = width/2,height/5
    score[i].convert()
# Pipes
pipes = []
pipesRect = []
for i, type in enumerate(["green", "red"]):
    pipes.append(pg.image.load("flappy-bird-assets/sprites/pipe-" + type + ".png"))
    pipesRect.append(pipes[i].get_rect())
    pipesRect[i].centerx = width
    pipesRect[i].bottom = baseRect.y

# Player
mainPlayer = Player((width/2, height/2), screen)

# Game Loop
while True:
    screen.fill((255,128,255)) # reseting the fram

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit() # exit the program if the window is closed

    # Draw Background
    screen.blit(dayBg, (0,0)) 
    screen.blit(score[0], scoreRect[0])
    screen.blit(base, baseRect)
    screen.blit(pipes[0], pipesRect[0])
    # Game play
    mainPlayer.display(baseRect, pipesRect[0])
    # screen.blit(playerImg, (width/2, height/2)) 
    pg.display.update()