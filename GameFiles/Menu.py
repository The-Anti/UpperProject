import pygame, math
from sys import exit
import threading

W = 1400
H = 800

pygame.init()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Ripoff Osu')
clock = pygame.time.Clock()




#menu circle thing
#------------------------------------------------------------------------------------------------------
count = 0

playPosX = -150
playPosY = H/2

flagBounce = False  #flag checking if it overshot
flagFinal = False   #flag checking if it hit the center after overshoot

playButtonSurface = pygame.Surface((300,300))
playButtonSurface.fill((100,100,100))
playButtonRect = playButtonSurface.get_rect(center = (playPosX,playPosY))

playButtonImage = pygame.image.load('PlayButton.png').convert_alpha()       #Image for the tab menu
imageSize = 0.5     #starting size
sizeTrip = False    #flag for seeing if image has reached max size
rotation = 30       #starting rotation
diff = 0
animEnd = False

#tinting screen
opacity = 0
tint = pygame.Surface((W,H))
tint.fill((235,235,235))
tintRect = tint.get_rect(center=(W/2,H/2))


tintScreen = False

#Background
#------------------------------------------------------------------------------------------------------
background = pygame.image.load('Background.jpg').convert_alpha()
backgroundRect = background.get_rect(center = (W/2,H/2))
#------------------------------------------------------------------------------------------------------


#Starting Animation
#------------------------------------------------------------------------------------------------------
def startAnim():
    global animEnd, imageSize, sizeTrip, tintScreen, opacity, flagBounce, flagFinal, rotation, playPosX, playPosY, count
    if animEnd == False:
        if imageSize >= 1.7:
            sizeTrip = True

        if sizeTrip and imageSize <= 1:
            imageSize = 1

        if tintScreen:
            opacity += 5
        else:
            opacity = 0

        if flagBounce == False and flagFinal == False:  #Moving from off screen to overshoot
            rotation -= (1/2 * count)**2 + (1/4 * count)
            playPosX += count**2
            count += 0.2
            imageSize += 0.015
        elif flagFinal == False:    #Moving from overshoot to center
            count += 0.1
            playPosX -= count**3
            rotation += count
            if sizeTrip == False:
                imageSize += 0.02
            else:
                imageSize -= (1/6 * count)**2
            if playPosX <= W/2:
                playPosX = W/2

        if playPosX >= W/2 and flagBounce == False:     #Settings for center to overshoot
            count -= 4
            rotation -= (1/2 * count)**2 + (1/3 * count)
            tintScreen = True
        if playPosX >= W/2 + 150 and flagBounce == False:      #Settings overshoot to center
            flagBounce = True
            count = 0
            imageSize += 0.02
        if flagBounce == True and playPosX == W/2:      #Settings for center
            flagFinal = True
            count = 0
            rotation = 44
            imageSize = 1
            animEnd = True
            opacity = 255
    else:
        return
#------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------


while True:
    mousepos = pygame.mouse.get_pos()
    for event in pygame.event.get():    #Event system
        if event.type == pygame.QUIT:   #If you leave the game, close the game
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    #When you click, things below happen.
            #ALL CLICK DETECTION WILL GO HERE
            #-------------------------------------------------------------------------------
            if animEnd == True:
                if imageRect.collidepoint(mousepos):
                    print('clicked')
            #-------------------------------------------------------------------------------
    screen.fill((0,0,0))

    image = pygame.transform.scale_by(playButtonImage,imageSize)
    rotatedImage = pygame.transform.rotate(image,rotation)
    imageRect = rotatedImage.get_rect(center = (playPosX, playPosY))
    if animEnd == False:
        screen.blit(rotatedImage, imageRect)
        screen.blit(tint, tintRect)
        tint.set_alpha(opacity)
        startAnim()

    
    
    else:
        screen.blit(background, backgroundRect)
        screen.blit(rotatedImage, imageRect)
        rotation += 1
        if rotation >=360:
            rotation = 0
        screen.blit(tint, tintRect)
        tint.set_alpha(opacity)
        if opacity > 0:
            opacity -= 20
        else:
            opactiy = 0



    pygame.display.flip()
    clock.tick(60)
