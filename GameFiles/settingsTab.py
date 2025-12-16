#THIS IS A FILE USED BY MENU.PY
#WHEN FINISHED WITH THIS FILE
#DELETE EVERYTHING IN BETWEEN THE TRIPLE BRACKETS UNLESS STATED ABOVE
#ONLY USED TO HELP MAKE THE CODE


#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
import pygame, math
from sys import exit
import threading
import sqlite3

W = 1400
H = 800

pygame.init()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Rhythmania')
clock = pygame.time.Clock()


#Text stuff
#------------------------------------------------------------------------------------------------------
pygame.font.init()

bigText = pygame.font.Font('bedstead-002.002/bedstead.otf', 70)
text = pygame.font.Font('bedstead-002.002/bedstead.otf', 40)
subText = pygame.font.Font('bedstead-002.002/bedstead.otf', 25)
text_settings = text.render('Settings', True, (0,0,0))
text_play = text.render('Play', True, (0,0,0))
text_chart = text.render('Editor', True, (0,0,0))
#------------------------------------------------------------------------------------------------------




#menu circle thing
#------------------------------------------------------------------------------------------------------
count = 0

playPosX = -150  #THIS IS THE DISK, NOT TO BE CONFUSED WITH THE GREEN 'PLAY' BUTTON
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
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#DO NOT DELETE


sClicked = False
sMenuOpen = False
settingsMenu = pygame.Surface((W/3,H),pygame.SRCALPHA)
settingsMenu.fill((80,80,80))
settingsMenuRect = settingsMenu.get_rect(topleft = (-W/3,0))

settingsText = bigText.render("Settings", True, (0,0,0))

gTappingText = subText.render("Ghost Tapping", True, (0,0,0))

scrollText = subText.render("Scroll toggle", True, (0,0,0))
upScrollText = subText.render("(Upscroll)", True, (0,0,0))
downScrollText = subText.render("(Downscroll)", True, (0,0,0))
testtext = subText.render("unused", True, (0,0,0))

keybindsText = subText.render("Keybinds", True, (0,0,0))




#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------


background = pygame.image.load('Background.jpg').convert_alpha()
backgroundRect = background.get_rect(center = (W/2,H/2))


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
            imageSize = 1.2
            opacity = 255
            animEnd = True
    else:
        return
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#DO NOT DELETE
def closeSettings():
    global sMenuOpen, save
    if settingsMenuRect.centerx < 0:    #If menu is offscreen...
        settingsMenuRect.centerx -= math.sqrt(W/3 + settingsMenuRect.centerx)*3 #Keep it off screen
        sMenuOpen = False   #Menu is closed / off screen
    else:
        settingsMenuRect.centerx -= math.sqrt(W/4 - settingsMenuRect.centerx)
        if save == False and settingsMenuRect.centerx >= 215:       #check to make sure that data isn't saved multiple times a second AKA reduce lag
            save = True

    if settingsMenuRect.centerx < -W/3:     #If its offscreen, keep it offscreen at a specific point
        settingsMenuRect.centerx = -W/3
#------------------------------------------------------------------------------------------------------
def openSettings():
    global sMenuOpen, sClicked, keybindNotSetFlag, save
    if sClicked:    #If menu button is clicked
        if settingsMenuRect.centerx < 0:        #if its off screen
            settingsMenuRect.centerx += math.sqrt(W/3 + settingsMenuRect.centerx)*3 #move onto the screen
        else:
            sMenuOpen = True    #menu is open and on screen
            settingsMenuRect.centerx += math.sqrt(W/6 - settingsMenuRect.centerx)   #make it ease out
    elif not sClicked and not '_' in keybinds:  #Are the keybinds set and the user clicked off the menu?
        keybindNotSetFlag = False   #say that the keybinds are good
        closeSettings()
    else:
        save = False    #do not save
        keybindNotSetFlag = True    #a keybind is not set
        sClicked = True     #keep menu open
#------------------------------------------------------------------------------------------------------
#please do not touch this class, it took away 2 hours of my life
class tickBoxButton():
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.button = pygame.Surface((self.w, self.h),pygame.SRCALPHA)
        self.flag = False
    
    def updatePos(self,x,y):
        buttonRect = self.button.get_rect(center =(x,y))
        screen.blit(self.button,buttonRect)
        return buttonRect

    def clickDetect(self, mousepos, r):
        global ghostTappingBool
        if r.collidepoint(mousepos):
            if self.flag:   #if its turned off
                self.flag = False
                ghostTappingBool = False
            else:       #if its turned on
                self.flag = True
                ghostTappingBool = True
            
    def updateColour(self):
        if self.flag:
            self.button.fill((0,255,0))
            return "green"
        else:
            self.button.fill((255,0,0))
            return "red"

#toggle buttons that use the class above
gTappingButton = tickBoxButton(50,50)
scrollButton = tickBoxButton(50,50)
buttonList = [gTappingButton,scrollButton]

        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------


#Tab stuff
#------------------------------------------------------------------------------------------------------
tWidth = 220
tHeight = 90

sPosX = 575
sPosY = 260

pPosX = 625
pPosY = 360

cPosY = 460
#------------------------------------------------------------------------------------------------------
clicked = False
toggleFlag = False


#keybind stuff
#------------------------------------------------------------------------------------------------------
key1Value = 'A'
key2Value = 'S'
key3Value = 'D'
key4Value = 'F'

key1 = pygame.Surface((100,100),pygame.SRCALPHA)
key2 = pygame.Surface((100,100),pygame.SRCALPHA)
key3 = pygame.Surface((100,100),pygame.SRCALPHA)
key4 = pygame.Surface((100,100),pygame.SRCALPHA)

keys = [key1, key2, key3, key4]

#creating database
database = sqlite3.connect("Keybinds.db")
cur = database.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS keybinds'
' (id INTEGER NOT NULL PRIMARY KEY, key1 TEXT, key2 TEXT, key3 TEXT, key4 TEXT, ghost BOOLEAN, volume INTEGEER, notespeed REAL)')
#ID, KEYBINDS, GHOST TAPPING

cur.execute('INSERT OR IGNORE INTO keybinds (id,key1,key2,key3,key4,ghost,volume,notespeed) VALUES (1,?,?,?,?,?,?,?)', ('A', 'S', 'D', 'F',False, 50,1))
#Only 1 row, Keybinds set to (ASDF) and ghost tapping is OFF by DEFAULT

database.commit()

keybindNotSet = text.render('Invalid keybinds', True, (0,0,0))

#volumeStuff
volumeTxt = subText.render("Volume", True, (0,0,0))

acceptableVolumeCharacters = ["0","1","2",'3','4','5','6','7','8','9']

inputBox = pygame.Surface((50,50),pygame.SRCALPHA)
inputBox.fill((124,124,124))

volumeClicked = False
count = 0

currentVolume = 50



done = True
inputFirstNumber = True
hundredFlag = False
selected = None     #which keybind is selected
keyClicked = False  #boolean to show if a keybind was clicked
invalid = False     #check if keybind is repeated
keybindNotSetFlag = False   #check for a keybind being '_'
save = False                #save flag
ghostTappingBool = False    #boolean for ghost tapping
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#DO NOT DELETE
while True:

    for i in buttonList:
        i.updateColour()

    #setting up the text
    settingsTextRect = settingsText.get_rect(center=(settingsMenuRect.centerx,settingsMenuRect.centery - 300))

    scrollTextRect = scrollText.get_rect(center = (settingsMenuRect.centerx-100,settingsMenuRect.centery - 120))
    upScrollTextRect = upScrollText.get_rect(center = (settingsMenuRect.centerx-100,settingsMenuRect.centery - 80))
    downScrollTextRect = downScrollText.get_rect(center = (settingsMenuRect.centerx-100,settingsMenuRect.centery - 80))
    testtextrect = testtext.get_rect(center = (settingsMenuRect.centerx+150,settingsMenuRect.centery - 100))

    gTappingRect = gTappingText.get_rect(center=(settingsMenuRect.centerx - 100, settingsMenuRect.centery-200))

    keybindsTextRect = keybindsText.get_rect(center = (settingsMenuRect.centerx, settingsMenuRect.centery))

    key1Rect = key1.get_rect(center = (settingsMenuRect.centerx - 150, settingsMenuRect.centery + 100))
    key2Rect = key2.get_rect(center = (settingsMenuRect.centerx - 50, settingsMenuRect.centery + 100))
    key3Rect = key3.get_rect(center = (settingsMenuRect.centerx + 50, settingsMenuRect.centery + 100))
    key4Rect = key4.get_rect(center = (settingsMenuRect.centerx + 150, settingsMenuRect.centery + 100))

    keysRect = [key1Rect, key2Rect, key3Rect, key4Rect]

    keybinds = [key1Value, key2Value, key3Value, key4Value]

    key1txt = text.render(key1Value, True, (0,0,0))
    key2txt = text.render(key2Value, True, (0,0,0))
    key3txt = text.render(key3Value, True, (0,0,0))
    key4txt = text.render(key4Value, True, (0,0,0))

    invalidtxt = text.render("Keybind in use", True, (0,0,0))
    txtrect = invalidtxt.get_rect(center = (settingsMenuRect.centerx, settingsMenuRect.centery + 30))

    boxRect = inputBox.get_rect(center = (settingsMenuRect.centerx + 100, settingsMenuRect.centery + 200))
    keybindNotSetRect = keybindNotSet.get_rect(center = (settingsMenuRect.centerx, settingsMenuRect.centery +30))

    volume = subText.render(f"{currentVolume}", True, (0,0,0))


    mousepos = pygame.mouse.get_pos()
    mouseX,mouseY = mousepos


    #settings up keybind stuff
    
    #Setting up the disk
    image = pygame.transform.scale_by(playButtonImage,imageSize)        #Image itself
    rotatedImage = pygame.transform.rotate(image,rotation)              #Allowing image to be rotated
    imageRect = rotatedImage.get_rect(center = (playPosX, playPosY))    #Getting position of the image

    diskCenterX,diskCenterY = imageRect.center
    radius = rotatedImage.get_width() / 2
    distance = math.hypot(mouseX - diskCenterX, mouseY - diskCenterY)       #calculating the distance from the center of the disk to the mouse

    
    for event in pygame.event.get():    #Event system
        if event.type == pygame.QUIT:   #If you leave the game, close the game
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    #When you click, things below happen.
            #ALL CLICK DETECTION WILL GO HERE
            #-------------------------------------------------------------------------------
            if animEnd == True:         #If the animation has played, the disk is clickable
                if sClicked and not settingsMenuRect.collidepoint(mousepos):    #If settings is open and user clicked away from it
                    if not keybindNotSetFlag:       #Initiates the settings save and closes settings menu if if the keybinds are set properly
                        save = True
                    sClicked = False        #Close settings
                if distance <= radius and not sMenuOpen:      #if the mouse is over the disk and when the settings menu is not open
                    imageSize = 1.7
                    if clicked == True:
                        clicked = False
                    else:
                        clicked = True
                elif settingsTabRect.collidepoint(mousepos) and clicked:    #opening the menu
                    if sMenuOpen:
                        sClicked = False
                    else:
                        sClicked = True
                gTappingButton.clickDetect(mousepos, r=i.updatePos(settingsMenuRect.x+300, settingsMenuRect.y+200)) #allows buttons to be clicked
                scrollButton.clickDetect(mousepos, r=i.updatePos(settingsMenuRect.x+300, settingsMenuRect.y+300))

                if volumeClicked:       #toggling volume clicked
                    volumeClicked = False
                    if currentVolume == '' or currentVolume == '-':
                        currentVolume = 0

                if boxRect.collidepoint(mousepos):
                    volumeClicked = True
                    done = False
                    inputFirstNumber = False
                    hundredFlag = False

                    num1 = 0
                    num2 = 0
                    num3 = 0


            #Check if a keybind has been clicked to change
            if key1Rect.collidepoint(mousepos):
                selected = key1
                keyClicked = True
                key1Value = '_'
            elif key2Rect.collidepoint(mousepos):
                selected = key2
                keyClicked = True
                key2Value = '_'
            elif key3Rect.collidepoint(mousepos):
                selected = key3
                keyClicked = True
                key3Value = '_'
            elif key4Rect.collidepoint(mousepos):
                selected = key4
                keyClicked = True
                key4Value = '_'
            else:
                keyClicked = False

        if event.type == pygame.KEYDOWN and keyClicked == True: #if the user is changing a keybind
            keyPressed = pygame.key.name(event.key).upper()
            if keyPressed in keybinds:  #if the new keybind is already a keybind then dont allow
                invalid = True
            else:                       #otherwise allow new keybind
                if selected == key1:
                    key1Value = keyPressed
                elif selected == key2:
                    key2Value = keyPressed
                elif selected == key3:
                    key3Value = keyPressed
                elif selected == key4:
                    key4Value = keyPressed
                keyClicked = False
                invalid = False

        if event.type == pygame.KEYDOWN and volumeClicked:
            keyPressed = pygame.key.name(event.key).upper()
            if keyPressed in acceptableVolumeCharacters or keyPressed == "RETURN":
                if currentVolume == 10 and keyPressed == '0':
                    currentVolume = 100
                    done = True
                    save = True
                    volumeClicked = False
                    hundredFlag = True
                elif keyPressed == "RETURN":
                    done = True
                    save = True
                    volumeClicked = False
                elif inputFirstNumber and keyPressed in acceptableVolumeCharacters:
                    num2 = keyPressed
                    currentVolume = int(num1) * 10 + int(num2)
                else:
                    num1 = keyPressed
                    currentVolume = num1
                    inputFirstNumber = True


            #-------------------------------------------------------------------------------
    screen.fill((0,0,0))

    #Playing the animation
    if animEnd == False:
        screen.blit(rotatedImage, imageRect)
        screen.blit(tint, tintRect)
        tint.set_alpha(opacity)
        startAnim()
    #this heiarchy makes sure that the tint is always over the disk image and that the animation doesn't break.
    
    #AFTER THE ANIMATION PLAYED
    else:
        openSettings()
        screen.blit(background, backgroundRect)
        settingsTab = pygame.Surface((tWidth,tHeight),pygame.SRCALPHA)
        settingsTabRect =settingsTab.get_rect(topleft = (sPosX, sPosY))
        text_settings_rect = text_settings.get_rect(center = settingsTabRect.center)

        playTab = pygame.Surface((tWidth,tHeight),pygame.SRCALPHA)
        playTabRect = playTab.get_rect(topleft = (pPosX, pPosY))
        text_play_rect = text_play.get_rect(center = playTabRect.center)

        chartTab = pygame.Surface((tWidth,tHeight),pygame.SRCALPHA)
        chartTabRect = chartTab.get_rect(topleft = (sPosX, cPosY))
        text_chart_rect = text_play.get_rect(center = chartTabRect.center)

        rotation += 1       #Spins the disk counter-clockwise
        opacity -= 10
        if rotation >=360:  #Just keeping the rotation variable between 0 and 360
            rotation = 0
        if opacity <= 0:
            opacity = 0

        #--------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------

        pygame.draw.rect(screen, (184, 52, 224), settingsTabRect, border_radius=100)
        pygame.draw.rect(screen, (0,204,0),playTabRect, border_radius=100)
        pygame.draw.rect(screen, (247, 114, 45),chartTabRect, border_radius=100)
        screen.blit(text_settings,text_settings_rect)
        screen.blit(text_play, text_play_rect)
        screen.blit(text_chart, text_chart_rect)
        screen.blit(rotatedImage, imageRect)
        screen.blit(settingsMenu,settingsMenuRect)
        screen.blit(settingsText,settingsTextRect)
        screen.blit(gTappingText,gTappingRect)
        screen.blit(scrollText,scrollTextRect)
        if clicked:
            if sPosX > 500:     
                sPosX -= 5
            if pPosX > 550:
                pPosX -= 5
            if imageSize < 1.4:
                imageSize = 1.4
            if tWidth < 600:
                tWidth += (math.sqrt(600 - tWidth)) * 1.3
            if playPosX > 450:
                playPosX -= (math.sqrt(playPosX - 450))
                imageSize -= 0.01
            else:
                playPosX = 450
                imageSize = 1.4

        else:
            if sPosX < 600:
                sPosX += 5
            if pPosX < 650:
                pPosX += 5
            if imageSize < 1:
                imageSize = 1
            if tWidth > 180:
                tWidth -= (math.sqrt(tWidth - 180)) * 1.5
            if playPosX < 700:
                playPosX += (math.sqrt(700- playPosX))
                imageSize -= 0.017
            else:
                screen.blit(rotatedImage, imageRect)
                playPosX = 700
                imageSize = 1.2

        #--------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------
        #DO NOT DELETE
        if scrollButton.updateColour() == "green":
            screen.blit(downScrollText,downScrollTextRect)
        elif scrollButton.updateColour() == "red":
            screen.blit(upScrollText,upScrollTextRect)

        gTappingButton.updatePos(settingsMenuRect.x+300, settingsMenuRect.y+200)
        scrollButton.updatePos(settingsMenuRect.x+300, settingsMenuRect.y+300)
        screen.blit(testtext,testtextrect)

        screen.blit(tint, tintRect)
        tint.set_alpha(opacity)

        if invalid and not keybindNotSetFlag:
            screen.blit(invalidtxt, txtrect)
        if keybindNotSetFlag:
            screen.blit(keybindNotSet,keybindNotSetRect)

        for i in range(0, 4):
            if selected == keys[i] and keybinds[i] == '_' and keyClicked:
                keys[i].fill((100,100,100))
            else:
                keys[i].fill((200,200,200))

        if not done and not inputFirstNumber and volumeClicked:
            count += 1
            if count > 60:
                count = 0
            if count > 30:
                currentVolume = "-"
            else:
                currentVolume = ""

        


        if save:
            cur.execute('REPLACE INTO keybinds (id, key1, key2, key3, key4, ghost, volume) VALUES (1,?,?,?,?,?,?)', 
                        (key1Value, key2Value, key3Value, key4Value, ghostTappingBool,currentVolume))
            database.commit()
            save = False
            print('saving')

        screen.blit(keybindsText, keybindsTextRect)
        screen.blit(key1, key1Rect)
        screen.blit(key2, key2Rect)
        screen.blit(key3, key3Rect)
        screen.blit(key4, key4Rect)
        screen.blit(key1txt, (key1Rect.centerx - 15, key1Rect.centery - 20))
        screen.blit(key2txt, (key2Rect.centerx - 15, key2Rect.centery - 20))
        screen.blit(key3txt, (key3Rect.centerx - 15, key3Rect.centery - 20))
        screen.blit(key4txt, (key4Rect.centerx - 15, key4Rect.centery - 20))

        screen.blit(inputBox,boxRect)
        screen.blit(volumeTxt,(boxRect.centerx-150, boxRect.centery-15))
        if hundredFlag:
            screen.blit(volume,(boxRect.centerx-25, boxRect.centery-10))
        else:
            screen.blit(volume,(boxRect.centerx-15, boxRect.centery-10))


#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------


    pygame.display.flip()
    clock.tick(60)
