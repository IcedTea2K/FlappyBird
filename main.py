import sys, pygame
pygame.init()

size = width, height = 320,240
speed = [2,2]
screen  = pygame.display.set_mode(size) # create scene

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    print(event)
    screen.fill((0,0,0))
    pygame.display.flip()
