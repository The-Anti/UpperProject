import pygame
from sys import exit

pygame.font.init()

text = pygame.font.Font('bedstead-002.002/bedstead.otf', 40)


W = 1400
H = 800

WHITE = (230,230,230)
BLACK = (0,0,0)
GREY = (126,126,126)
PRESSEDGREY = (66,66,66)
DARKBLUE = (0,0,139)
BLUE = (0,191,240)
VIOLET = (138,43,226)
RED = (255,20,34)
GREEN = (124,252,0)
DARKGREEN = (0,128,0)
LIGHTRED = (205,92,92)

laneSize = 110
border_length = 25

screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

background = pygame.Surface((W,H))
bgRect = background.get_rect(center= (W/2,H/2))

playSurface = pygame.Surface(((laneSize*4 + border_length*7),800))
playRect = playSurface.get_rect(center= (W/2,H/2))

def getLanes():
    global lane1, lane1rect, lane2, lane2rect, lane3, lane3rect, lane4, lane4rect
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

getLanes()

def drawLanes():
    screen.blit(lane1, lane1rect)
    screen.blit(lane2, lane2rect)
    screen.blit(lane3, lane3rect)
    screen.blit(lane4, lane4rect)

class JudgementNote():
    def __init__(self, lane):
        self.colour = GREY
        self.lane = lane
        self.judge = pygame.draw.circle(screen, self.colour, (self.lane.centerx, self.lane.centery + 300), 50)
        self.surface = pygame.Surface((100,100))
        self.rect = self.surface.get_rect(center=self.judge.center)
        self.flag = False
        self.pressed = False 
    
    def updateJudge(self):
        self.judge = pygame.draw.circle(screen, self.colour, (self.lane.centerx, self.lane.centery + 300), 50)

    def changeColour(self):
        if self.colour == GREY:
            self.colour = PRESSEDGREY
        else:
            self.colour = GREY
        self.pressed = True



class PressNote():
    def __init__(self, lane, speed, ):
        self.lane = lane
        if self.lane == lane1rect or self.lane == lane4rect:
            self.colour = BLUE
        else:
            self.colour = WHITE
        self.note = pygame.draw.circle(screen, self.colour, (self.lane.centerx, 0), 45)
        self.speed = speed
        self.newY = 0
        self.judgePos = 0
        self.judgement = 0

    def score(self):
        global combo, judgement, score, scale
        self.judgePos = 650 - self.note.y
        if self.judgePos in range(-15, 15): #MARVELOUS
            self.judgement = 100
            if judgement:
                judgement.pop()
                judgement.append('Perf')
            else:
                judgement.append('Perf')
        elif self.judgePos in range(-30, 30): #Perfect
            self.judgement = 75
            if judgement:
                judgement.pop()
                judgement.append('Great')
            else:
                judgement.append('Great')
        elif self.judgePos in range(-55, 55): #Great
            self.judgement = 50
            if judgement:
                judgement.pop()
                judgement.append('Good')
            else:
                judgement.append('Good')
        else:
            self.judgement = 25     #Good
            if judgement:
                judgement.pop()
                judgement.append('Bad')
            else:
                judgement.append('Bad')
        
        if self.judgement != 25:
            combo += 1
            scale = 1.4
        score += self.judgement
        return self.judgement

    def detect(self):
        if self.note.centery in range(725 - self.speed*10, 725 + self.speed*10):
            self.score()
            self.hit = True

    def updateNote(self):
        self.newY += self.speed
        self.note = pygame.draw.circle(screen, self.colour, (self.lane.centerx, self.newY), 45)



class holdNote():
    def __init__(self, lane, speed, length):
        self.lane = lane
        if self.lane == lane1rect or self.lane == lane4rect:
            self.colour = BLUE
        else:
            self.colour = WHITE
        self.length = length*25
        self.endNote = pygame.draw.circle(screen, self.colour, (self.lane.centerx, 0 - self.length), 45)
        self.startNote = pygame.draw.circle(screen, self.colour, (self.lane.centerx, 0), 45)
        self.line = pygame.draw.line(screen, self.colour, self.endNote.center, self.startNote.center, 45)
        self.speed = speed
        self.newY = 0
        self.judgePos = 0
        self.startJudgement = 0
        self.judgement = 0
        self.startHold = False
        self.delete = False

    def updateNote(self):
        self.newY += self.speed
        self.endNote = pygame.draw.circle(screen, self.colour, (self.lane.centerx, self.newY - self.length), 45)
        if self.startHold == False:
            self.startNote = pygame.draw.circle(screen, self.colour, (self.lane.centerx, self.newY), 45)
        else:
            self.startNote = pygame.draw.circle(screen, self.colour, (self.lane.centerx, 700), 45)
        self.line = pygame.draw.line(screen, self.colour, self.endNote.center, self.startNote.center, 45)

    def y(self):
        return self.startNote.y
    
    def detect(self):
        if self.startNote.centery in range(725 - self.speed*10, 725 + self.speed*10):
            self.startHold = True
            self.startScore()
    
    def trackHold(self, judge):
        global combo
        if judge.colour == PRESSEDGREY and self.startHold == True:
            return
        elif judge.colour == GREY and self.startHold == True and self.endNote.centery not in range(725 - self.speed*10, 725 + self.speed*10):
            combo = 0
            self.delete = True
        
    def endDetect(self):
        if self.endNote.centery in range(725 - self.speed*10, 725 + self.speed*10):
            self.score()

    def startScore(self):
        global combo, judgement, score, scale
        self.judgePos = 650 - self.startNote.y
        if self.judgePos in range(-15, 15): #MARVELOUS
            self.startJudgement = 100
            if judgement:
                judgement.pop()
                judgement.append('Perf')
            else:
                judgement.append('Perf')
        elif self.judgePos in range(-30, 30): #Perfect
            self.startJudgement = 75
            if judgement:
                judgement.pop()
                judgement.append('Great')
            else:
                judgement.append('Great')
        elif self.judgePos in range(-55, 55): #Great
            self.startJudgement = 50
            if judgement:
                judgement.pop()
                judgement.append('Good')
            else:
                judgement.append('Good')
        else:
            self.startJudgement = 25     #Good
            if judgement:
                judgement.pop()
                judgement.append('Bad')
            else:
                judgement.append('Bad')

        if self.startJudgement != 25:
            combo += 1
            scale = 1.4
        score += self.startJudgement

    def score(self):
        global combo, judgement, score, scale
        self.judgePos = 650 - self.endNote.y
        if self.judgePos in range(-15, 15): #PERFECT
            self.judgement = self.startJudgement + 100
            if judgement:
                judgement.pop()
                judgement.append('Perf')
            else:
                judgement.append('Perf')
        elif self.judgePos in range(-30, 30): #Great
            self.judgement = self.startJudgement + 75
            if judgement:
                judgement.pop()
                judgement.append('Great')
            else:
                judgement.append('Great')
        elif self.judgePos in range(-55, 55): #Good
            self.judgement = self.startJudgement + 50
            if judgement:
                judgement.pop()
                judgement.append('Good')
            else:
                judgement.append('Good')
        else:
            self.judgement = self.startJudgement + 25     #bad
            if judgement:
                judgement.pop()
                judgement.append('Bad')
            else:
                judgement.append('Bad')

        if self.judgement - self.startJudgement != 25:
            combo += 1
            scale = 1.4
        score += self.judgement
        return self.judgement
    


def spawnNote(type, lane, len=None):
    global lane1Notes,lane2Notes,lane3Notes,lane4Notes,noteSpeed
    if type == 'Tap':
        if lane == 1:
            lane1Notes.append(PressNote(lane1rect,noteSpeed))
        if lane == 2:
            lane2Notes.append(PressNote(lane2rect,noteSpeed))
        if lane == 3:
            lane3Notes.append(PressNote(lane3rect,noteSpeed))
        if lane == 4:
            lane4Notes.append(PressNote(lane4rect,noteSpeed))

    elif type == 'Hold':
        if lane == 1:
            lane1Notes.append(holdNote(lane1rect, noteSpeed, len))
        if lane == 2:
            lane2Notes.append(holdNote(lane2rect, noteSpeed, len))
        if lane == 3:
            lane3Notes.append(holdNote(lane3rect, noteSpeed, len))
        if lane == 4:
            lane4Notes.append(holdNote(lane4rect, noteSpeed, len))

judge1 = JudgementNote(lane1rect)
judge2 = JudgementNote(lane2rect)
judge3 = JudgementNote(lane3rect)
judge4 = JudgementNote(lane4rect)

lane1Notes = []
lane2Notes = []
lane3Notes = []
lane4Notes = []

judges = [judge1, judge2, judge3, judge4]

offset = 300

lane1spawning = pygame.USEREVENT+1
lane2spawning = pygame.USEREVENT+2
lane3spawning = pygame.USEREVENT+3
lane4spawning = pygame.USEREVENT+4

pygame.time.set_timer(lane1spawning, 750)
pygame.time.set_timer(lane2spawning, 1500)
pygame.time.set_timer(lane3spawning, 2000)
pygame.time.set_timer(lane4spawning, 1000)

combo = 0
scale = 1
comboText = text.render(f'combo: {combo}', True, WHITE)
comboBox = pygame.transform.scale_by(comboText, scale)
comboRect = comboBox.get_rect(bottomleft = (lane1rect.left - 400, lane1rect.bottom - 100))

perfectText = text.render('Perfect!', True, VIOLET)
greatText = text.render('Great', True, DARKGREEN)
goodText = text.render('Good', True, GREEN)
badText = text.render('Bad', True, LIGHTRED)
missText = text.render('Miss', True, RED)

judgement = []

judgeBox = pygame.Surface((300,40),pygame.SRCALPHA)
judgeRect = judgeBox.get_rect(center = (comboRect.centerx+125, comboRect.centery-75))
judgeBox.fill((0,0,0))

pressing = True

score = 0

noteSpeed = 15


while True:
    screen.blit(background, bgRect)
    for event in pygame.event.get():    #Event system
        if event.type == pygame.QUIT:   #If you leave the game, close the game
            pygame.quit()
            exit()
        
        #pressing key
        if event.type == pygame.KEYDOWN:
            keyPressed = pygame.key.name(event.key).upper()
            if keyPressed == 'A':
                if lane1Notes:
                    lane1Notes[0].detect()
                judge1.changeColour()
            if keyPressed == "S":
                judge2.changeColour()
                if lane2Notes:
                    lane2Notes[0].detect()
            if keyPressed == "K":
                judge3.changeColour()
                if lane3Notes:
                    lane3Notes[0].detect()
            if keyPressed == "L":
                judge4.changeColour()
                if lane4Notes:
                    lane4Notes[0].detect()

        #letting go of key
        elif event.type == pygame.KEYUP:
            keyPressed = pygame.key.name(event.key).upper()
            if keyPressed == 'A':
                judge1.changeColour()
                if lane1Notes:
                    if isinstance(lane1Notes[0],holdNote):
                        lane1Notes[0].endDetect()
            if keyPressed == "S":
                judge2.changeColour()
                if lane2Notes:
                    if isinstance(lane2Notes[0],holdNote):
                        lane2Notes[0].endDetect()
            if keyPressed == "K":
                judge3.changeColour()
                if lane3Notes:
                    if isinstance(lane3Notes[0],holdNote):
                        lane3Notes[0].endDetect()
            if keyPressed == "L":
                judge4.changeColour()
                if lane1Notes:
                    if isinstance(lane4Notes[0],holdNote):
                        lane4Notes[0].endDetect()

        #spawning
        if event.type == lane1spawning:
            spawnNote('Tap', 1)
        elif event.type == lane2spawning:
            spawnNote('Tap', 2)
        elif event.type == lane3spawning:
            spawnNote('Hold', 3, 10)
        elif event.type == lane4spawning:
            spawnNote('Hold', 4, 5)

    if scale <= 1:
        scale = 1
    else:
        scale -= 0.05

    comboText = text.render(f'combo: {combo}', True, WHITE)
    comboBox = pygame.transform.scale_by(comboText, scale)
    comboRect = comboBox.get_rect(bottomleft = (lane1rect.left - 400, lane1rect.bottom - 100))

    if judgement:
        if judgement[0] == 'Perf':
            screen.blit(perfectText,judgeRect)
        if judgement[0] == 'Great':
            screen.blit(greatText,judgeRect)
        if judgement[0] == 'Good':
            screen.blit(goodText,judgeRect)
        if judgement[0] == 'Bad':
            screen.blit(badText, judgeRect)
        if judgement[0] == 'Miss':
            screen.blit(missText,judgeRect)
            
    background.fill(BLACK)
    screen.blit(playSurface,playRect)
    screen.blit(comboText, comboRect)

    scoreText = text.render(f'score: {score}', True, WHITE)
    scoreRect = scoreText.get_rect(topleft = comboRect.bottomleft)
    screen.blit(scoreText, scoreRect)

    drawLanes()

    for judge in judges:
        judge.updateJudge()

    for note in lane1Notes:
        note.updateNote()

        if isinstance(note, PressNote):
            if note.note.y > 900:      #if note off screen
                lane1Notes.remove(note)
                combo = 0
                if judgement:
                    judgement.pop()
                    judgement.append('Miss')
                else:
                    judgement.append('Miss')
            elif note.judgement != 0:           #if tapped
                lane1Notes.remove(note)

        elif isinstance(note, holdNote):
            note.trackHold(judge1)
            if note.endNote.y > 900 or note.delete == True:
                lane1Notes.remove(note)
                combo = 0
                if judgement:
                    judgement.pop()
                    judgement.append('Miss')
                else:
                    judgement.append('Miss')
            elif note.judgement != 0:
                lane1Notes.remove(note)

    for note in lane2Notes:
        note.updateNote()

        if isinstance(note,PressNote):
            if note.note.y > 900:
                lane2Notes.remove(note)
                combo = 0
                if judgement:
                    judgement.pop()
                    judgement.append('Miss')
                else:
                    judgement.append('Miss')
            elif note.judgement != 0:
                lane2Notes.remove(note)

        elif isinstance(note, holdNote):
            note.trackHold(judge2)
            if note.endNote.y > 900 or note.delete == True:
                lane2Notes.remove(note)
                combo = 0
                if judgement:
                    judgement.pop()
                    judgement.append('Miss')
                else:
                    judgement.append('Miss')
            elif note.judgement != 0:
                lane2Notes.remove(note)

    for note in lane3Notes:
        note.updateNote()

        if isinstance(note, PressNote):
            if note.note.y > 900:
                lane3Notes.remove(note)
                combo = 0
                if judgement:
                    judgement.pop()
                    judgement.append('Miss')
                else:
                    judgement.append('Miss')
            elif note.judgement != 0:
                lane3Notes.remove(note)
        
        elif isinstance(note, holdNote):
            note.trackHold(judge3)
            if note.endNote.y > 900 or note.delete == True:
                lane3Notes.remove(note)
                combo = 0
                if judgement:
                    judgement.pop()
                    judgement.append('Miss')
                else:
                    judgement.append('Miss')
            elif note.judgement != 0:
                lane3Notes.remove(note)



    for note in lane4Notes:
        note.updateNote()

        if isinstance(note, PressNote):
            if note.y() > 900:   #if note off screen
                lane4Notes.remove(note)
                combo = 0
                if judgement:
                    judgement.pop()
                    judgement.append('Miss')
                else:
                    judgement.append('Miss')
            elif note.judgement != 0:       #if tapped
                lane4Notes.remove(note)

        elif isinstance(note, holdNote):
            note.trackHold(judge4)
            if note.endNote.y > 900 or note.delete == True:
                lane4Notes.remove(note)
                combo = 0
                if judgement:
                    judgement.pop()
                    judgement.append('Miss')
                else:
                    judgement.append('Miss')
            elif note.judgement != 0:
                lane4Notes.remove(note)
        

    pygame.display.flip()
    clock.tick(60)
