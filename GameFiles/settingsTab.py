# #THIS IS A FILE USED BY MENU.PY

import pygame, math
import sqlite3

W = 1400
H = 800

pygame.init()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Rhythmania')
clock = pygame.time.Clock()


# #Text stuff
# #------------------------------------------------------------------------------------------------------
pygame.font.init()

bigText = pygame.font.Font('bedstead-002.002/bedstead.otf', 70)
text = pygame.font.Font('bedstead-002.002/bedstead.otf', 40)
subText = pygame.font.Font('bedstead-002.002/bedstead.otf', 25)
subberText = pygame.font.Font('bedstead-002.002/bedstead.otf', 20)
text_settings = text.render('Settings', True, (0,0,0))
text_play = text.render('Play', True, (0,0,0))
text_chart = text.render('Editor', True, (0,0,0))

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

# #------------------------------------------------------------------------------------------------------


background = pygame.image.load('Background.jpg').convert_alpha()
backgroundRect = background.get_rect(center = (W/2,H/2))


# #please do not touch this class, it took away 2 hours of my life
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
        return all
            
    def updateColour(self):
        if self.flag:
            self.button.fill((0,255,0))
            return "green"
        else:
            self.button.fill((255,0,0))
            return "red"


class settings():
    #NOT IN WHILE LOOP
    def __init__(self):
        print('Running')
        global text, bigText, subText, subberText
        global ghostTappingBool
        self.sClicked = False
        self.sMenuOpen = False
        self.settingsMenu = pygame.Surface((W/3,H),pygame.SRCALPHA)
        self.settingsMenu.fill((80,80,80))
        self.settingsMenuRect = self.settingsMenu.get_rect(topleft = (-W/3,0))

        self.settingsText = bigText.render("Settings", True, (0,0,0))

        self.gTappingText = subText.render("Ghost Tapping", True, (0,0,0))

        self.scrollText = subText.render("Scroll toggle", True, (0,0,0))
        self.upScrollText = subText.render("(Upscroll)", True, (0,0,0))
        self.downScrollText = subText.render("(Downscroll)", True, (0,0,0))
        self.testtext = subText.render("unused", True, (0,0,0))

        self.keybindsText = subText.render("Keybinds", True, (0,0,0))
        self.gTappingButton = tickBoxButton(50,50)
        self.scrollButton = tickBoxButton(50,50)
        self.buttonList = [self.gTappingButton,self.scrollButton]
        self.key1Value = 'A'
        self.key2Value = 'S'
        self.key3Value = 'D'
        self.key4Value = 'F'

        self.key1 = pygame.Surface((100,100),pygame.SRCALPHA)
        self.key2 = pygame.Surface((100,100),pygame.SRCALPHA)
        self.key3 = pygame.Surface((100,100),pygame.SRCALPHA)
        self.key4 = pygame.Surface((100,100),pygame.SRCALPHA)

        self.keys = [self.key1, self.key2, self.key3, self.key4]

        self.keybindNotSet = text.render('Invalid settings', True, (0,0,0))

        self.volumeTxt = subText.render("Volume", True, (0,0,0))

        self.acceptableVolumeCharacters = ["0","1","2",'3','4','5','6','7','8','9']

        self.inputBox = pygame.Surface((50,50),pygame.SRCALPHA)
        self.inputBox.fill((124,124,124))

        self.scrollSpeedBox = pygame.Surface((50,50),pygame.SRCALPHA)
        self.scrollSpeedBox.fill((124,124,124))

        self.UpScrollSpeedBox = pygame.Surface((50,50),pygame.SRCALPHA)
        self.UpScrollSpeedBox.fill((124,124,124))
        self.IncreaseSpeedText = subberText.render('+0.1', True, (0,0,0))

        self.DownScrollSpeedBox = pygame.Surface((50,50),pygame.SRCALPHA)
        self.DownScrollSpeedBox.fill((124,124,124))
        self.DecreaseSpeedText = subberText.render('-0.1', True, (0,0,0))

        self.volumeClicked = False
        self.count = 0

        self.currentVolume = 50
        self.currentScrollSpeed = 1.0


        self.done = True
        self.inputFirstNumber = True
        self.hundredFlag = False
        self.selected = None     #which keybind is selected
        self.keyClicked = False  #boolean to show if a keybind was clicked
        self.invalid = False     #check if keybind is repeated
        self.keybindNotSetFlag = False   #check for a keybind being '_'
        self.save = False                #save flag
        ghostTappingBool = False    #boolean for ghost tapping

        self.settingsTextRect = self.settingsText.get_rect(center=(self.settingsMenuRect.centerx,self.settingsMenuRect.centery - 300))

        self.scrollTextRect = self.scrollText.get_rect(center = (self.settingsMenuRect.centerx-100,self.settingsMenuRect.centery - 120))
        self.upScrollTextRect = self.upScrollText.get_rect(center = (self.settingsMenuRect.centerx-100,self.settingsMenuRect.centery - 80))
        self.downScrollTextRect = self.downScrollText.get_rect(center = (self.settingsMenuRect.centerx-100,self.settingsMenuRect.centery - 80))
        self.testtextrect = self.testtext.get_rect(center = (self.settingsMenuRect.centerx+150,self.settingsMenuRect.centery - 100))

        self.gTappingRect = self.gTappingText.get_rect(center=(self.settingsMenuRect.centerx - 100, self.settingsMenuRect.centery-200))

        self.keybindsTextRect = self.keybindsText.get_rect(center = (self.settingsMenuRect.centerx, self.settingsMenuRect.centery))

        self.key1Rect = self.key1.get_rect(center = (self.settingsMenuRect.centerx - 150, self.settingsMenuRect.centery + 100))
        self.key2Rect = self.key2.get_rect(center = (self.settingsMenuRect.centerx - 50, self.settingsMenuRect.centery + 100))
        self.key3Rect = self.key3.get_rect(center = (self.settingsMenuRect.centerx + 50, self.settingsMenuRect.centery + 100))
        self.key4Rect = self.key4.get_rect(center = (self.settingsMenuRect.centerx + 150, self.settingsMenuRect.centery + 100))

        self.keysRect = [self.key1Rect, self.key2Rect, self.key3Rect, self.key4Rect]

        self.keybinds = [self.key1Value, self.key2Value, self.key3Value, self.key4Value]

        self.key1txt = text.render(self.key1Value, True, (0,0,0))
        self.key2txt = text.render(self.key2Value, True, (0,0,0))
        self.key3txt = text.render(self.key3Value, True, (0,0,0))
        self.key4txt = text.render(self.key4Value, True, (0,0,0))

        self.invalidtxt = text.render("Keybind in use", True, (0,0,0))
        self.txtrect = self.invalidtxt.get_rect(center = (self.settingsMenuRect.centerx, self.settingsMenuRect.centery + 30))

        self.boxRect = self.inputBox.get_rect(center = (self.settingsMenuRect.centerx + 100, self.settingsMenuRect.centery + 200))
        self.keybindNotSetRect = self.keybindNotSet.get_rect(center = (self.settingsMenuRect.centerx, self.settingsMenuRect.centery +30))

        self.volume = subText.render(f"{self.currentVolume}", True, (0,0,0))

        self.scrollSpeedBoxRect = self.scrollSpeedBox.get_rect(center = (self.settingsMenuRect.centerx, self.settingsMenuRect.centery + 300))
        self.UpScrollSpeedBoxRect = self.UpScrollSpeedBox.get_rect(center = (self.settingsMenuRect.centerx + 100, self.settingsMenuRect.centery + 300))
        self.DownScrollSpeedBoxRect = self.DownScrollSpeedBox.get_rect(center = (self.settingsMenuRect.centerx - 100, self.settingsMenuRect.centery + 300))

        self.currentScrollSpeed = round(self.currentScrollSpeed, 1)
        self.scrollSpeed = subText.render(f"{self.currentScrollSpeed}", True, (0,0,0))

        self.database = sqlite3.connect("Settings.db")
        self.cur = self.database.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS settings'
        ' (id INTEGER NOT NULL PRIMARY KEY, key1 TEXT, key2 TEXT, key3 TEXT, key4 TEXT, ghost BOOLEAN, volume INTEGEER, notespeed REAL)')
        #ID, KEYBINDS, GHOST TAPPING

        self.cur.execute('INSERT OR IGNORE INTO settings (id,key1,key2,key3,key4,ghost,volume,notespeed) VALUES (1,?,?,?,?,?,?,?)', ('A', 'S', 'D', 'F',False, 50,1.0))




    def closeSettings(self):
        if self.settingsMenuRect.centerx < 0:    #If menu is offscreen...
            self.settingsMenuRect.centerx -= math.sqrt(W/3 + self.settingsMenuRect.centerx)*3 #Keep it off screen
            self.sMenuOpen = False   #Menu is closed / off screen
        else:
            self.settingsMenuRect.centerx -= math.sqrt(W/4 - self.settingsMenuRect.centerx)
            ('Close')
            if self.save == False and self.settingsMenuRect.centerx >= 215:       #check to make sure that data isn't saved multiple times a second AKA reduce lag
                self.save = True

        if self.settingsMenuRect.centerx < -W/3:     #If its offscreen, keep it offscreen at a specific point
            self.settingsMenuRect.centerx = -W/3
        
        return all

    def openSettings(self):
        if self.sClicked:    #If menu button is clicked
            if self.settingsMenuRect.centerx < 0:        #if its off screen
                self.settingsMenuRect.centerx += math.sqrt(W/3 + self.settingsMenuRect.centerx)*3 #move onto the screen
                print('Open')
            else:
                self.sMenuOpen = True    #menu is open and on screen
                self.settingsMenuRect.centerx += math.sqrt(W/6 - self.settingsMenuRect.centerx)   #make it ease out
                print('test')
        elif not self.sClicked and not '_' in self.keybinds:  #Are the keybinds set and the user clicked off the menu?
            self.keybindNotSetFlag = False   #say that the keybinds are good
            self.closeSettings()
        else:
            self.save = False    #do not save
            self.keybindNotSetFlag = True    #a keybind is not set
            self.sClicked = True     #keep menu open
        
        return all


    def loopedSettings(self):
        #IN WHILE LOOP
        for i in self.buttonList:
            i.updateColour()

        #setting up the text
        self.settingsTextRect = self.settingsText.get_rect(center=(self.settingsMenuRect.centerx,self.settingsMenuRect.centery - 300))

        self.scrollTextRect = self.scrollText.get_rect(center = (self.settingsMenuRect.centerx-100,self.settingsMenuRect.centery - 120))
        self.upScrollTextRect = self.upScrollText.get_rect(center = (self.settingsMenuRect.centerx-100,self.settingsMenuRect.centery - 80))
        self.downScrollTextRect = self.downScrollText.get_rect(center = (self.settingsMenuRect.centerx-100,self.settingsMenuRect.centery - 80))
        self.testtextrect = self.testtext.get_rect(center = (self.settingsMenuRect.centerx+150,self.settingsMenuRect.centery - 100))

        self.gTappingRect = self.gTappingText.get_rect(center=(self.settingsMenuRect.centerx - 100, self.settingsMenuRect.centery-200))

        self.keybindsTextRect = self.keybindsText.get_rect(center = (self.settingsMenuRect.centerx, self.settingsMenuRect.centery))

        self.key1Rect = self.key1.get_rect(center = (self.settingsMenuRect.centerx - 150, self.settingsMenuRect.centery + 100))
        self.key2Rect = self.key2.get_rect(center = (self.settingsMenuRect.centerx - 50, self.settingsMenuRect.centery + 100))
        self.key3Rect = self.key3.get_rect(center = (self.settingsMenuRect.centerx + 50, self.settingsMenuRect.centery + 100))
        self.key4Rect = self.key4.get_rect(center = (self.settingsMenuRect.centerx + 150, self.settingsMenuRect.centery + 100))

        self.keysRect = [self.key1Rect, self.key2Rect, self.key3Rect, self.key4Rect]

        self.keybinds = [self.key1Value, self.key2Value, self.key3Value, self.key4Value]

        self.key1txt = text.render(self.key1Value, True, (0,0,0))
        self.key2txt = text.render(self.key2Value, True, (0,0,0))
        self.key3txt = text.render(self.key3Value, True, (0,0,0))
        self.key4txt = text.render(self.key4Value, True, (0,0,0))

        self.invalidtxt = text.render("Keybind in use", True, (0,0,0))
        self.txtrect = self.invalidtxt.get_rect(center = (self.settingsMenuRect.centerx, self.settingsMenuRect.centery + 30))

        self.boxRect = self.inputBox.get_rect(center = (self.settingsMenuRect.centerx + 100, self.settingsMenuRect.centery + 200))
        self.keybindNotSetRect = self.keybindNotSet.get_rect(center = (self.settingsMenuRect.centerx, self.settingsMenuRect.centery +30))

        self.volume = subText.render(f"{self.currentVolume}", True, (0,0,0))

        self.scrollSpeedBoxRect = self.scrollSpeedBox.get_rect(center = (self.settingsMenuRect.centerx, self.settingsMenuRect.centery + 300))
        self.UpScrollSpeedBoxRect = self.UpScrollSpeedBox.get_rect(center = (self.settingsMenuRect.centerx + 100, self.settingsMenuRect.centery + 300))
        self.DownScrollSpeedBoxRect = self.DownScrollSpeedBox.get_rect(center = (self.settingsMenuRect.centerx - 100, self.settingsMenuRect.centery + 300))

        self.currentScrollSpeed = round(self.currentScrollSpeed, 1)
        self.scrollSpeed = subText.render(f"{self.currentScrollSpeed}", True, (0,0,0))
        return all

    def ClickedSettings(self,mousepos):
        global num1, num2
        self.gTappingButton.clickDetect(mousepos, r=self.gTappingButton.updatePos(self.settingsMenuRect.x+300, self.settingsMenuRect.y+200)) #allows buttons to be clicked
        self.scrollButton.clickDetect(mousepos, r=self.scrollButton.updatePos(self.settingsMenuRect.x+300, self.settingsMenuRect.y+300))

        if self.volumeClicked:       #toggling volume clicked
                self.volumeClicked = False
                if self.currentVolume == '' or self.currentVolume == '-':
                        self.currentVolume = 0

        if self.boxRect.collidepoint(mousepos):
                    self.volumeClicked = True
                    self.done = False
                    self.inputFirstNumber = False
                    self.hundredFlag = False

                    num1 = 0
                    num2 = 0

        if self.DownScrollSpeedBoxRect.collidepoint(mousepos):
                    self.currentScrollSpeed -= 0.1
        elif self.UpScrollSpeedBoxRect.collidepoint(mousepos):
                    self.currentScrollSpeed += 0.1


            #Check if a keybind has been clicked to change
        if self.key1Rect.collidepoint(mousepos):
                self.selected = self.key1
                self.keyClicked = True
                self.key1Value = '_'
        elif self.key2Rect.collidepoint(mousepos):
                self.selected = self.key2
                self.keyClicked = True
                self.key2Value = '_'
        elif self.key3Rect.collidepoint(mousepos):
                self.selected = self.key3
                self.keyClicked = True
                self.key3Value = '_'
        elif self.key4Rect.collidepoint(mousepos):
                self.selected = self.key4
                self.keyClicked = True
                self.key4Value = '_'
        else:
                self.keyClicked = False
        return all
        
    def eventKeybinds(self, keyPressed):
            # keyPressed = pygame.key.name(event.key).upper()
            if keyPressed in self.keybinds:  #if the new keybind is already a keybind then dont allow
                self.invalid = True
            else:                       #otherwise allow new keybind
                if self.selected == self.key1:
                    self.key1Value = keyPressed
                elif self.selected == self.key2:
                    self.key2Value = keyPressed
                elif self.selected == self.key3:
                    self.key3Value = keyPressed
                elif self.selected == self.key4:
                    self.key4Value = keyPressed
                self.keyClicked = False
                self.invalid = False
            return all
                
    def eventVolume(self, keyPressed):
            global num1, num2
            #keyPressed = pygame.key.name(event.key).upper()
            if keyPressed in self.acceptableVolumeCharacters or keyPressed == "RETURN":
                if self.currentVolume == 10 and keyPressed == '0':
                    self.currentVolume = 100
                    self.done = True
                    self.save = True
                    self.volumeClicked = False
                    self.hundredFlag = True
                elif keyPressed == "RETURN":
                    self.done = True
                    self.save = True
                    self.volumeClicked = False
                elif self.inputFirstNumber and keyPressed in self.acceptableVolumeCharacters:
                    num2 = keyPressed
                    self.currentVolume = int(num1) * 10 + int(num2)
                else:
                    num1 = keyPressed
                    self.currentVolume = num1
                    self.inputFirstNumber = True
            return all
    
    def settingsTabClicked(self,mousepos):
        print(self.sMenuOpen)
        if self.sClicked and not self.settingsMenuRect.collidepoint(mousepos):    #If settings is open and user clicked away from it
            if not self.keybindNotSetFlag:       #Initiates the settings save and closes settings menu if if the keybinds are set properly
                self.save = True
                self.sClicked = False        #Close settings

    def sClickedSetting(self):
        print(self.sMenuOpen)
        if self.sMenuOpen:
            self.sClicked = False
        else:
            self.sClicked = True


    def mainLoop1(self):
        self.openSettings()
        screen.blit(self.settingsMenu,self.settingsMenuRect)
        screen.blit(self.settingsText,self.settingsTextRect)
        screen.blit(self.gTappingText,self.gTappingRect)
        screen.blit(self.scrollText,self.scrollTextRect)
        return all

    def mainLoop2(self):
        global screen

        self.openSettings()
        screen.blit(self.settingsMenu,self.settingsMenuRect)
        screen.blit(self.settingsText,self.settingsTextRect)
        screen.blit(self.gTappingText,self.gTappingRect)
        screen.blit(self.scrollText,self.scrollTextRect)

        if self.scrollButton.updateColour() == "green":
            screen.blit(self.downScrollText,self.downScrollTextRect)
        elif self.scrollButton.updateColour() == "red":
            screen.blit(self.upScrollText,self.upScrollTextRect)

        self.gTappingButton.updatePos(self.settingsMenuRect.x+300, self.settingsMenuRect.y+200)
        self.scrollButton.updatePos(self.settingsMenuRect.x+300, self.settingsMenuRect.y+300)
        screen.blit(self.testtext,self.testtextrect)

        if self.invalid and not self.keybindNotSetFlag:
            screen.blit(self.invalidtxt, self.txtrect)
        if self.keybindNotSetFlag:
            screen.blit(self.keybindNotSet,self.keybindNotSetRect)

        for i in range(0, 4):
            if self.selected == self.keys[i] and self.keybinds[i] == '_' and self.keyClicked:
                self.keys[i].fill((100,100,100))
            else:
                self.keys[i].fill((200,200,200))

        if not self.done and not self.inputFirstNumber and self.volumeClicked:
            self.count += 1
            if self.count > 60:
                self.count = 0
            if self.count > 30:
                self.currentVolume = "-"
            else:
                self.currentVolume = ""

        self.updateDatabase()

        screen.blit(self.keybindsText, self.keybindsTextRect)
        screen.blit(self.key1, self.key1Rect)
        screen.blit(self.key2, self.key2Rect)
        screen.blit(self.key3, self.key3Rect)
        screen.blit(self.key4, self.key4Rect)
        screen.blit(self.key1txt, (self.key1Rect.centerx - 15, self.key1Rect.centery - 20))
        screen.blit(self.key2txt, (self.key2Rect.centerx - 15, self.key2Rect.centery - 20))
        screen.blit(self.key3txt, (self.key3Rect.centerx - 15, self.key3Rect.centery - 20))
        screen.blit(self.key4txt, (self.key4Rect.centerx - 15, self.key4Rect.centery - 20))

        screen.blit(self.scrollSpeedBox,self.scrollSpeedBoxRect)
        screen.blit(self.scrollSpeed,(self.scrollSpeedBoxRect.centerx-22, self.scrollSpeedBoxRect.centery-10))
        screen.blit(self.UpScrollSpeedBox, self.UpScrollSpeedBoxRect)
        screen.blit(self.IncreaseSpeedText, (self.UpScrollSpeedBoxRect.centerx-25, self.UpScrollSpeedBoxRect.centery-10))
        screen.blit(self.DownScrollSpeedBox, self.DownScrollSpeedBoxRect)
        screen.blit(self.DecreaseSpeedText, (self.DownScrollSpeedBoxRect.centerx-25, self.DownScrollSpeedBoxRect.centery-10))

        screen.blit(self.inputBox,self.boxRect)
        screen.blit(self.volumeTxt,(self.boxRect.centerx-150, self.boxRect.centery-15))
        if self.hundredFlag:
            screen.blit(self.volume,(self.boxRect.centerx-25, self.boxRect.centery-10))
        else:
            screen.blit(self.volume,(self.boxRect.centerx-15, self.boxRect.centery-10))

        return all


    def updateDatabase(self):
        global ghostTappingBool
        if self.save:
            self.cur.execute('REPLACE INTO settings (id, key1, key2, key3, key4, ghost, volume,notespeed) VALUES (1,?,?,?,?,?,?,?)', 
                        (self.key1Value, self.key2Value, self.key3Value, self.key4Value, ghostTappingBool,self.currentVolume,self.currentScrollSpeed))
            self.database.commit()
            self.save = False
        return all
