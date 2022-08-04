import sys
import pygame as pg
import queue
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
flashValue = 255
isFlashing = False
screenCover = pg.Surface((width, height))
isDay = True
dayBg = pg.image.load("flappy-bird-assets/sprites/background-day.png")
nightBg = pg.image.load("flappy-bird-assets/sprites/background-night.png")
menuScreen = pg.image.load("flappy-bird-assets/sprites/message.png")
menuScreenRect = menuScreen.get_rect(center=(width/2, height/2))
endScreen = pg.image.load("flappy-bird-assets/sprites/gameover.png")
endScreenRect = endScreen.get_rect(center=(width/2, height/3 + 30))
base =  pg.image.load("flappy-bird-assets/sprites/base.png")
baseRect = base.get_rect()
baseRect.center = width/2, height-56
# Sound Effects
soundQ = queue.Queue()
def loadSfx(effectNum: int) -> None:
    """
    0 - die sound, 1 - hit sound, 2 - point sound, 3 - wing sound, 4 - swoosh sound
    """
    pg.mixer.music.unload()
    if effectNum == 0: 
        pg.mixer.music.load("flappy-bird-assets/audio/die.wav", "wav")
    elif effectNum == 1:
        pg.mixer.music.load("flappy-bird-assets/audio/hit.wav", "wav")
    elif effectNum == 2:
        pg.mixer.music.load("flappy-bird-assets/audio/point.wav", "wav")
    elif effectNum == 3:
        pg.mixer.music.load("flappy-bird-assets/audio/wing.wav", "wav")
    elif effectNum == 4:
        pg.mixer.music.load("flappy-bird-assets/audio/swoosh.wav", "wav")
    
# Scores
score = []
currScore = 0
hasScored = False
for i in range(10):
    score.append(pg.image.load("flappy-bird-assets/sprites/" + str(i) + ".png"))
    score[i].convert()
def drawScore() -> None: 
    if currScore < 10:
        rect = score[currScore].get_rect(center=(width/2, height/6))
        screen.blit(score[currScore], rect)
        return
    tempScore = currScore
    digits = [] # container for all the digits of the current score
    while tempScore >0: # extract the digits of the score 
        digits.append(tempScore%10)
        tempScore = int(tempScore/10)

    for i, digit in reversed(list(enumerate(digits))): # has to reverse because last digits are added in first
        rect = score[digit].get_rect(center=(width/2, height/6))
        size = score[digit].get_size()
        offset = size[0] if digit != 1 else size[0]+4 # img for digit '1' has a slightly smaller size
        rect.move_ip(((len(digits)-1)/2.0 - i)*offset, 0) # adjust position based on digit location
        screen.blit(score[digit], rect)

# Pipes
currPipeMode = 0
pipes = [Pipe(screen, mode=currPipeMode, speed=1)]
# Player
mainPlayer = Player(pg.Vector2(142,304), screen, fpsClock)
# Custom Events
GAME_STATE = 0 # 0 - menu, 1 - playing, 2 - finished
SPAWN_PIPES_EVENT = pg.USEREVENT + 1
SWITCH_PIPE_EVENT = pg.USEREVENT + 2 
SWITCH_DAYTIME_EVENT = pg.USEREVENT + 3 # switch the background periodically 
SWITCH_BIRD_EVENT = pg.USEREVENT + 4
def setTimers() -> None:
    """Set timers for customized events"""
    pg.time.set_timer(SWITCH_DAYTIME_EVENT, 10000)
    pg.time.set_timer(SPAWN_PIPES_EVENT, 3000)
    pg.time.set_timer(SWITCH_PIPE_EVENT, 30000)
    pg.time.set_timer(SWITCH_BIRD_EVENT, 20000)
def stopTimers() -> None:
    """Stop the timers of customized events"""
    pg.time.set_timer(SWITCH_DAYTIME_EVENT, 0)
    pg.time.set_timer(SPAWN_PIPES_EVENT, 0)
    pg.time.set_timer(SWITCH_PIPE_EVENT, 0)
    pg.time.set_timer(SWITCH_BIRD_EVENT, 0)

# Game Loop
while True:
    # Game play
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit() # exit the program if the window is closed
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if GAME_STATE == 0: #start the game
                    GAME_STATE = 1
                    soundQ.put(3)
                    setTimers()
                elif GAME_STATE == 2 and not pg.mixer.music.get_busy(): # reset all stats
                    GAME_STATE = 0
                    soundQ.put(4) # play entering death menu soudn
                    currScore = 0
                    hasScored = False
                    isFlashing = False
                    isDay = True
                    pipes.clear() # clear out all current pipes
                    currPipeMode = 0
                    pipes = [Pipe(screen, mode=currPipeMode, speed=1)] # must add one in to prevent idx error
                    mainPlayer.reset()
                mainPlayer.fly = GAME_STATE != 2 # prevent bird from moving when on the ground
        elif event.type == pg.KEYUP and GAME_STATE == 1:
            if event.key == pg.K_SPACE:
                mainPlayer.fly = False
        elif event.type == SPAWN_PIPES_EVENT: # add pipes
            pipes.append(Pipe(screen, mode=currPipeMode,speed=1))
        elif event.type == SWITCH_PIPE_EVENT: # switch pipes' color
            currPipeMode = 1 if currPipeMode == 0 else 0
        elif event.type == SWITCH_DAYTIME_EVENT: # switch background daylight
            isDay = not isDay
        elif event.type == SWITCH_BIRD_EVENT: # switch bird's color
            if mainPlayer.state < 2:
                mainPlayer.state += 1
            else:
                mainPlayer.state = 0

    # Draw Background
    if isDay:
        screen.blit(dayBg, (0,0)) 
    else:
        screen.blit(nightBg, (0,0))
    screen.blit(base, baseRect) 

    for pipe in reversed(pipes): # remove the pipe without skipping the next pipe
        if pipe.pos[0] < -52: # remove pipes that are off the screen
            pipes.remove(pipe)
        else:
            pipe.display(GAME_STATE == 1)
    
    drawScore()

    # Game Master
    if GAME_STATE == 0: # Menu Screens
        screen.blit(menuScreen, menuScreenRect)
    elif GAME_STATE == 2: # show end screen
        screen.blit(endScreen, endScreenRect)
        stopTimers()

    nextPipe = None # check which pipe bird might collide next
    if len(pipes) > 1 and pipes[0].pos[0] < width/2 - 50:
        nextPipe = pipes[1]
        hasScored = False 
    else:
        nextPipe = pipes[0]
    if not mainPlayer.display(baseRect, nextPipe.get_rect(), GAME_STATE) and GAME_STATE!= 2: # check collision while displaying bird
        GAME_STATE = 2
        flashValue = 0 if not isFlashing else flashValue
        soundQ.put(1) # hitting sound
        if mainPlayer.pos.y < baseRect.y-10: # only when hitting the pipe
            soundQ.put(0) # falling sound 
    
    if mainPlayer.pos.x == nextPipe.pos[0] and mainPlayer.pos.y > 0 and not hasScored: # score calculations
        soundQ.put(2) 
        currScore+=1
        hasScored = True # scoring flag -- prevent player from scoring infinite point when bird happens to die at the same pos as pipe
    
    if soundQ.qsize() != 0 and not pg.mixer.music.get_busy(): # Sound Controller 
        tempSound = soundQ.get()
        loadSfx(tempSound)
        pg.mixer.music.play()

    if flashValue >= 0 and flashValue < 255: # flash when bird dies
        isFlashing = True
        screenCover.set_alpha(flashValue)
        screenCover.fill((0,0,0))
        screen.blit(screenCover, (0,0))
        flashValue += 50

    # print(time)
    pg.display.update()
    fpsClock.tick(60) 