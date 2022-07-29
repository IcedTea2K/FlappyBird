from math import gamma
import sys
import pygame as pg
from Player import *
from Pipe import *
pg.init()

# Setting up the window
size = width, height = 288,512
speed = [2,2]
screen  = pg.display.set_mode(size) # create scene
fpsClock = pg.time.Clock()
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
pipes = [Pipe(screen, mode=1 , speed=1)]
SPAWN_RATE = 3 # every two seconds
# Player
mainPlayer = Player(pg.Vector2(width/2, height/2), screen, fpsClock)
# Custom Events
GAME_STATE = 1 # 0 - menu, 1 - playing, 2 - finished
SPAWN_PIPES_EVENT = pg.USEREVENT + 1
pg.time.set_timer(SPAWN_PIPES_EVENT, int(SPAWN_RATE*1000))
# Game Loop
while True:
    screen.fill((255,128,255)) # reseting the fram

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit() # exit the program if the window is closed
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and GAME_STATE == 1 :
                mainPlayer.fly = True
        elif event.type == pg.KEYUP and GAME_STATE == 1:
            if event.key == pg.K_SPACE and mainPlayer.fly is None:
                mainPlayer.fly = False
        elif event.type == SPAWN_PIPES_EVENT and GAME_STATE == 1:
            pipes.append(Pipe(screen, mode=1,speed=1))
    # Draw Background
    screen.blit(dayBg, (0,0)) 
    screen.blit(base, baseRect)
    for pipe in reversed(pipes): # remove the pipe without skipping the next pipe
        if pipe.pos[0] < -52:
            pipes.remove(pipe)
        else:
            pipe.display(GAME_STATE == 1)
    # Game play
    if not mainPlayer.display(baseRect, pipes[0].get_rect()): # always detect collision with the first pipe
        GAME_STATE = 2
    screen.blit(score[0], scoreRect[0])
    
    # screen.blit(playerImg, (width/2, height/2)) 
    pg.display.update()
    fpsClock.tick(60)