import pygame, math
from sys import exit
import threading

W = 1400
H = 800

pygame.init()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Rhythmania')
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
        if imageSize >= 1.7:    #If the size of the disk is too big then trigger the flag that forces it to go smaller.
            sizeTrip = True

        if sizeTrip and imageSize <= 1:     #Uses the flag from above to set the size to normal.
            imageSize = 1

        if tintScreen:          #Tints the screen white when the flag is activated
            opacity += 7
        else:                   #When flag is not active, no tinting.
            opacity = 0

        if flagBounce == False and flagFinal == False:  #Moving from off screen to overshoot
            rotation -= (1/2 * count)**2 + (1/4 * count)    #Rotating clockwise following a quadratic graph
            playPosX += count**2    #Moves the disk right
            count += 0.2        
            imageSize += 0.015
        elif flagFinal == False:    #Moving from overshoot to centre
            count += 0.1
            playPosX -= count**3        #Moving disk left
            rotation += count
            if sizeTrip == False:       #If the disk is not big enough, increase size. Else start to shrink it quadratically.
                imageSize += 0.02
            else:
                imageSize -= (1/6 * count)**2
            if playPosX <= W/2:         #If the disk is to the left of the centre, blit it in the centre.
                playPosX = W/2

        if playPosX >= W/2 and flagBounce == False:     #Settings for center to overshoot
            count -= 4                                      #Rotate the disk clockwise a little faster and tint screen
            rotation -= (1/2 * count)**2 + (1/3 * count)
            tintScreen = True
        if playPosX >= W/2 + 150 and flagBounce == False:      #Settings overshoot to centre
            flagBounce = True                                  #Trigger the bounce flag for lower if statement
            count = 0
            imageSize += 0.02
        if flagBounce == True and playPosX == W/2:      #Settings for when the disk is in the centre
            flagFinal = True                            #Flag to say the animation has finished
            count = 0
            rotation = 44
            imageSize = 1
            opacity = 255
            animEnd = True
    else:
        return
#------------------------------------------------------------------------------------------------------

#Tab stuff
#------------------------------------------------------------------------------------------------------
tWidth = 220
tHeight = 100

sPosX = 575
sPosY = 260
#------------------------------------------------------------------------------------------------------
clicked = False

while True:
    mousepos = pygame.mouse.get_pos()
    for event in pygame.event.get():    #Event system
        if event.type == pygame.QUIT:   #If you leave the game, close the game
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    #When you click, things below happen.
            #ALL CLICK DETECTION WILL GO HERE
            #-------------------------------------------------------------------------------
            if animEnd == True:         #If the animation has played, the disk is clickable
                if imageRect.collidepoint(mousepos):
                    imageSize = 1.5
                    if clicked == True:
                        clicked = False
                    else:
                        clicked = True
            #-------------------------------------------------------------------------------
    screen.fill((0,0,0))

    #Setting up the disk
    image = pygame.transform.scale_by(playButtonImage,imageSize)        #Image itself
    rotatedImage = pygame.transform.rotate(image,rotation)              #Allowing image to be rotated
    imageRect = rotatedImage.get_rect(center = (playPosX, playPosY))    #Getting position of the image

    #Playing the animation
    if animEnd == False:
        screen.blit(rotatedImage, imageRect)
        screen.blit(tint, tintRect)
        tint.set_alpha(opacity)
        startAnim()
    #this heiarchy makes sure that the tint is always over the disk image and that the animation doesn't break.
    
    #AFTER THE ANIMATION PLAYED
    else:
        settingsTab = pygame.Surface((tWidth,tHeight),pygame.SRCALPHA)
        settingsTabRect =settingsTab.get_rect(topleft = (sPosX, sPosY))


        screen.blit(background, backgroundRect)
        rotation += 1       #Spins the disk counter-clockwise
        opacity -= 10
        if rotation >=360:  #Just keeping the rotation variable between 0 and 360
            rotation = 0
        if opacity <= 0:
            opacity = 0


        pygame.draw.rect(screen, (184, 52, 224), settingsTabRect, border_radius=100)
        screen.blit(rotatedImage, imageRect)        #Blits disk over the background
        if clicked:
            if sPosX > 500:
                sPosX -= 5
            if imageSize < 1.2:
                imageSize = 1.2
            if tWidth < 600:
                tWidth += (math.sqrt(600 - tWidth)) * 1.3
            if playPosX > 450:
                playPosX -= (math.sqrt(playPosX - 450))
                imageSize -= 0.01
            else:
                playPosX = 450
                imageSize = 1.2

        else:
            if sPosX < 600:
                sPosX += 5
            if imageSize < 1:
                imageSize = 1
            if tWidth > 180:
                tWidth -= (math.sqrt(tWidth - 180)) * 1.5
            if playPosX < 700:
                playPosX += (math.sqrt(700- playPosX))
                imageSize -= 0.017
            else:
                screen.blit(background, backgroundRect)
                screen.blit(rotatedImage, imageRect)
                playPosX = 700
                imageSize = 1
        screen.blit(tint, tintRect)
        tint.set_alpha(opacity)
    pygame.display.flip()
    clock.tick(60)
