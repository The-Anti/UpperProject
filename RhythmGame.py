import pygame
from sys import exit


W = 1400
H = 800

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (80,80,80)
DARKBLUE = (0,0,139)

laneSize = 100
border_length = 25

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Ripoff Osu')
clock = pygame.time.Clock()

background = pygame.Surface((W,H))
bgRect = background.get_rect(center= (W/2,H/2))

playSurface = pygame.Surface(((laneSize*4 + border_length*7),800))
playRect = playSurface.get_rect(center= (W/2,H/2))

lane1 = pygame.Surface((laneSize,800))
lane1.fill((20,20,20))
lane1rect = lane1.get_rect(topleft = (playRect.left + border_length*2, playRect.top))

lane2 = pygame.Surface((laneSize,800))
lane2.fill((20,20,20))
lane2rect = lane2.get_rect(topleft = (lane1rect.right + border_length,0))

lane3 = pygame.Surface((laneSize,800))
lane3.fill((20,20,20))
lane3rect = lane3.get_rect(topleft = (lane2rect.right + border_length,0))

lane4 = pygame.Surface((laneSize,800))
lane4.fill((20,20,20))
lane4rect = lane4.get_rect(topleft = (lane3rect.right + border_length,0))




while True:
    for event in pygame.event.get():    #Event system
        if event.type == pygame.QUIT:   #If you leave the game, close the game
            pygame.quit()
            exit()

    bgColor = DARKBLUE
    background.fill(bgColor)
    screen.blit(background, bgRect)
    screen.blit(playSurface,playRect)
    screen.blit(lane1, lane1rect)
    screen.blit(lane2, lane2rect)
    screen.blit(lane3, lane3rect)
    screen.blit(lane4, lane4rect)

    pygame.display.flip()
    clock.tick(60)