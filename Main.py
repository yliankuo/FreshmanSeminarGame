import pygame
import xml.etree.ElementTree as ET
import random
import time

current = None
face = None
screen = None
happy = 0
human = 0
robot = 0
cash = 0
efficiency = 0
tolerance = 0
wage = 0
price = 0

newevent = False
hfaces = []
rfaces = []
pos = None

dqueue = []
tm = time.time()
added = False
newdialogue = False
oldid = 0
delay = False
equeue = ["0"]
prevface = -1
mouseup = True

entities = 0
cqueue = []
entqueue = []

class Chip:
    def __init__(self, asset, x, y, xs, ys):
        self.asset = asset
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys

class Entity:
    def __init__(self, asset, x, y, xs, ys, type,dir,act):
        self.asset = asset
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys
        self.dir = dir
        self.odir = dir
        self.anim = 0
        self.placed = False
        self.type = type
        self.act = act

def updateEvent():
    global newevent
    global delay
    if not current != None and newevent:
        newevent = True
        delay = False

def updateRobots(ef):
    global entqueue
    for e in entqueue:
        if(e.type == "Robot"):
            e.xs = ef
            e.ys = ef

def genFaces():
    global hfaces
    global rfaces
    hfaces.append(pygame.transform.scale(pygame.image.load("Assets/Faces/Male1.png"),(120,93)))
    hfaces.append(pygame.transform.scale(pygame.image.load("Assets/Faces/Male2.png"),(120,93)))
    hfaces.append(pygame.transform.scale(pygame.image.load("Assets/Faces/Male3.png"),(120,93)))
    hfaces.append(pygame.transform.scale(pygame.image.load("Assets/Faces/Male4.png"),(120,93)))
    hfaces.append(pygame.transform.scale(pygame.image.load("Assets/Faces/Female1.png"),(120,93)))
    hfaces.append(pygame.transform.scale(pygame.image.load("Assets/Faces/Female2.png"),(120,93)))
    hfaces.append(pygame.transform.scale(pygame.image.load("Assets/Faces/Female3.png"),(120,93)))
    hfaces.append(pygame.transform.scale(pygame.image.load("Assets/Faces/Female4.png"),(120,93)))
    rfaces.append(pygame.transform.scale(pygame.image.load("Assets/Faces/Robot1.png"),(120,93)))
    rfaces.append(pygame.transform.scale(pygame.image.load("Assets/Faces/Robot2.png"),(120,93)))
    rfaces.append(pygame.transform.scale(pygame.image.load("Assets/Faces/Robot3.png"),(120,93)))

def drawText(surface, text, color, rect, font, aa=True, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

def drawUI():
    global screen
    background = pygame.image.load("Assets/UI/Background.png")
    background = pygame.transform.scale(background, (720, 560))
    table = pygame.image.load("Assets/UI/Table.png")
    table2 = pygame.image.load("Assets/UI/Table2.png")
    chatbox = pygame.image.load("Assets/UI/ChatBox.png")
    chatbox = pygame.transform.scale(chatbox, (720, 140))
    optionbox = pygame.image.load("Assets/UI/OptionBox.png")
    optionbox = pygame.transform.scale(optionbox,(560,280))
    computerscreen = pygame.transform.scale(pygame.image.load("Assets/UI/ComputerScreen.png"),(560,420))
    happycounter = pygame.transform.scale(pygame.image.load("Assets/UI/HappyCounter.png"),(130,30))
    robcounter = pygame.transform.scale(pygame.image.load("Assets/UI/RobotCounter.png"),(130,30))
    humcounter = pygame.transform.scale(pygame.image.load("Assets/UI/HumanCounter.png"),(130,30))
    cashcounter = pygame.transform.scale(pygame.image.load("Assets/UI/CashCounter.png"),(130,30))
    screen.blit(background, [0, 0])
    screen.blit(table, [180, 35])
    screen.blit(table, [280, 35])
    screen.blit(table, [30, 205])
    screen.blit(table, [405, 450])
    screen.blit(table, [405, 275])
    screen.blit(table, [555, 275])
    screen.blit(table2, [175, 520])
    screen.blit(pygame.image.load("Assets/UI/Table3.png"), [0, 248])
    screen.blit(chatbox, [0, 560])
    screen.blit(optionbox,[720,420])
    screen.blit(computerscreen,[720,0])
    screen.blit(happycounter, [770,58])
    screen.blit(robcounter, [880, 58])
    screen.blit(humcounter, [990, 58])
    screen.blit(cashcounter, [1100, 58])

def drawOptions(options):
    global screen
    buttonBox = pygame.transform.scale(pygame.image.load("Assets/UI/ButtonBox.png"),(210,101))
    buttonBoxHover = pygame.transform.scale(pygame.image.load("Assets/UI/ButtonBoxHover.png"),(210,101))
    global pos
    coords = pos
    if(coords[0] in range(780,990) and coords[1] in range(459,568)):
        screen.blit(buttonBoxHover, [780, 459])
    else:
        screen.blit(buttonBox, [780, 459])
    if (coords[0] in range(1010, 1240) and coords[1] in range(459, 568)):
        screen.blit(buttonBoxHover, [1010, 459])
    else:
        screen.blit(buttonBox, [1010, 459])
    if (coords[0] in range(780, 990) and coords[1] in range(568, 669)):
        screen.blit(buttonBoxHover, [780, 568])
    else:
        screen.blit(buttonBox, [780, 568])
    if (coords[0] in range(1010, 1240) and coords[1] in range(568, 669)):
        screen.blit(buttonBoxHover, [1010, 568])
    else:
        screen.blit(buttonBox, [1010, 568])
    if(len(dqueue) > 0): return
    font = pygame.font.SysFont('Courier', 14)
    o1RectText = pygame.Rect(790,467,190,66)
    o2RectText = pygame.Rect(1020, 467, 190, 66)
    o3RectText = pygame.Rect(790,576,190,66)
    o4RectText = pygame.Rect(1020,576,190,66)
    if options.find("o1").find("message").text != "NONE":
        drawText(screen, options.find("o1").find("message").text, (0, 0, 0), o1RectText, font)
    if options.find("o2").find("message").text != "NONE":
        drawText(screen, options.find("o2").find("message").text, (0, 0, 0), o2RectText, font)
    if options.find("o3").find("message").text != "":
        drawText(screen, options.find("o3").find("message").text, (0, 0, 0), o3RectText, font)
    if options.find("o4").find("message").text != "":
        drawText(screen, options.find("o4").find("message").text, (0, 0, 0), o4RectText, font)

def drawDialogue():
    global tm
    global dqueue
    global newdialogue
    global screen
    global newevent
    global face
    global hfaces
    global rfaces
    global oldid
    global prevface
    if len(dqueue) > 0:
        if time.time() - tm > 5:
            dqueue.pop(0)
            tm = time.time()
        else:
            id = dqueue[0]
            dialogue = ET.parse("Assets/Dialogue.xml").getroot()
            cdia = None
            for dia in dialogue:
                if dia.find("id").text == id:
                    cdia = dia
            if cdia == None:
                return
            if oldid != id:
                tm = time.time()
                tfaces = None
                tlen = 0
                if cdia.find("entity").text == "Person":
                    tfaces = hfaces
                    tlen = human
                else:
                    tfaces = rfaces
                    tlen = robot
                tface = random.randint(0, tlen - 1)
                while tface == prevface:
                    tface = random.randint(0, tlen - 1)
                prevface = tface
                face = tfaces[tface]
                oldid = id
                if cdia.find("dialogue").text != None:
                    dqueue.append(cdia.find("dialogue").text)
            diaRectText = pygame.Rect(200, 583, 450, 93)
            if face == None:
                return
            screen.blit(face, [50, 583])
            font = pygame.font.SysFont('Courier', 15)
            drawText(screen, cdia.find("message").text, (255, 255, 255), diaRectText, font)
    else:
        tm = time.time()

def cardinalMove(entity):
    if entity.type == "Human":
        if entity.dir == 0:
            entity.anim = 0
            if entity.odir == 1:
                entity.asset = pygame.image.load("Assets/Sprites/Human/HB.png")
            if entity.odir == 2:
                entity.asset = pygame.image.load("Assets/Sprites/Human/HR.png")
            if entity.odir == 3:
                entity.asset = pygame.image.load("Assets/Sprites/Human/HF.png")
            if entity.odir == 4:
                entity.asset = pygame.image.load("Assets/Sprites/Human/HL.png")
        if entity.dir == 1:
            entity.y -= entity.ys
            entity.anim += 1
            if entity.anim >= 0:
                entity.asset = pygame.image.load("Assets/Sprites/Human/HB1.png")
            if entity.anim > 4 :
                entity.asset = pygame.image.load("Assets/Sprites/Human/HB2.png")
            if entity.anim > 7:
                entity.anim = 0

        if entity.dir == 2:
            entity.x += entity.xs
            entity.anim += 1
            if entity.anim >= 0:
                entity.asset = pygame.image.load("Assets/Sprites/Human/HR1.png")
            if entity.anim > 4:
                entity.asset = pygame.image.load("Assets/Sprites/Human/HR2.png")
            if entity.anim > 7:
                entity.anim = 0
        if entity.dir == 3:
            entity.y += entity.ys
            entity.anim += 1
            if entity.anim >= 0:
                entity.asset = pygame.image.load("Assets/Sprites/Human/HF1.png")
            if entity.anim > 4 :
                entity.asset = pygame.image.load("Assets/Sprites/Human/HF2.png")
            if entity.anim > 7:
                entity.anim = 0
        if entity.dir == 4:
            entity.x -= entity.xs
            entity.anim += 1
            if entity.anim >= 0:
                entity.asset = pygame.image.load("Assets/Sprites/Human/HL1.png")
            if entity.anim > 4 :
                entity.asset = pygame.image.load("Assets/Sprites/Human/HL2.png")
            if entity.anim > 7:
                entity.anim = 0
    if entity.type == "Robot":
        if entity.dir == 1:
            entity.y -= entity.ys
            entity.asset = pygame.image.load("Assets/Sprites/Robot/RB.png")
        if entity.dir == 2:
            entity.x += entity.xs
            entity.asset = pygame.image.load("Assets/Sprites/Robot/RR.png")
        if entity.dir == 3:
            entity.y += entity.ys
            entity.asset = pygame.image.load("Assets/Sprites/Robot/RF.png")
        if entity.dir == 4:
            entity.x -= entity.xs
            entity.asset = pygame.image.load("Assets/Sprites/Robot/RL.png")
    return entity

def drawEntity():
    global screen
    global entqueue
    global equeue
    global dqueue
    #0: None, 1: Up, 2: Right, 3: Down, 4: Left
    etemp = entqueue.copy()
    for i in range(0,len(etemp)):
        e = etemp[i]
        screen.blit(e.asset,[e.x,e.y])
        if(len(dqueue) == 0):
            continue
        if e.act == 1:
            e = a1(e)
        if e.act == 2:
            e = a2(e)
        if e.act == 3:
            e = a3(e)
        if e.act == 4:
            e = a4(e)
        if e.act == 5:
            e = a5(e)
        if e.act == 6:
            e = a6(e)
        if e.act == 7:
            e = a7(e)
        if e.act == 8:
            e = a8(e)
        entqueue[i] = cardinalMove(e)

def drawChip():
    global screen
    global cqueue
    ctemp = cqueue.copy()
    tlist = []
    moved = False
    for i in range(0,len(ctemp)):
        c = ctemp[i]
        screen.blit(c.asset,[c.x,c.y])
        if(len(dqueue) == 0):
            continue
        if c.y < 525:
            cqueue[i].y += c.ys
        elif c.y >= 525 and c.x < 550:
            cqueue[i].x += c.xs
        elif c.y >= 525 and c.y < 535:
            cqueue[i].y += c.ys
        elif c.y >= 535:
            tlist.append(i)
    if len(tlist) > 0:
        for i in sorted(tlist,reverse=True):
            cqueue.pop(i)

def drawFactory():
    drawEntity()
    drawChip()

def drawInfo(message):
    global screen
    global human
    global happy
    global robot
    global cash
    compRectText = pygame.Rect(780,93,440,272)
    font = pygame.font.SysFont('Courier', 15)
    uifont = pygame.font.SysFont('Courier', 12)
    happyRectText = pygame.Rect(820, 68, 50,16)
    drawText(screen, str(happy), (0,0,0), happyRectText,uifont)
    robotRectText = pygame.Rect(925, 68, 50,16)
    drawText(screen, str(robot), (0,0,0), robotRectText,uifont)
    humanRectText = pygame.Rect(1035, 68, 50,16)
    drawText(screen, str(human), (0,0,0), humanRectText,uifont)
    cashRectText = pygame.Rect(1140, 68, 80,16)
    drawText(screen, str(cash), (0,0,0), cashRectText,uifont)
    if message != None:
        drawText(screen, message, (255, 255, 255), compRectText, font)

def parseRange(string):
    if string == None:
        return range(-100000,-100000)
    i = string.index(",")
    return range(int(string[:i]),int(string[i+1:]) + 1)

def drawEvents():
    global newevent
    global added
    global dqueue
    global delay
    if not newevent:
        global current
        events = ET.parse("Assets/Events.xml").getroot()
        if len(equeue) == 0:
            for event in events:
                req = event.find("req")
                if happy in parseRange(req.find("happy").text) and human in parseRange(req.find("human").text) and robot in parseRange(req.find("robot").text) and cash in parseRange(req.find("cash").text):
                    current = event
        else:
            id = equeue[0]
            for event in events:
                if event.find("id").text == id:
                    current = event
            delay = False
    if current == None:
        drawInfo(None)
        return
    drawInfo(current.find("message").text)
    drawOptions(current.find("options"))
    if not delay and not newevent:
        delay = True
        added = False
        if len(equeue) > 0:
            equeue.pop(0)
    if current.find("dialogue") != None and current.find("dialogue").text not in dqueue and not added:
        dqueue.append(current.find("dialogue").text)
        added = True

def updatePos():
    global pos
    pos = pygame.mouse.get_pos()

def getChoice(coords):
    global human
    global happy
    global robot
    global cash
    global newevent
    global current
    global dqueue
    global entities
    global efficiency
    choice = None
    if (len(dqueue) > 0): return
    if current == None:
        return
    if (coords[0] in range(780, 990) and coords[1] in range(459, 560)):
        choice = current.find("options").find("o1")
    if (coords[0] in range(1010, 1240) and coords[1] in range(459, 560)):
        choice = current.find("options").find("o2")
    if (coords[0] in range(780, 990) and coords[1] in range(568, 669)):
        choice = current.find("options").find("o3")
    if (coords[0] in range(1010, 1240) and coords[1] in range(568, 669)):
        choice = current.find("options").find("o4")
    if choice != None and choice.find("message").text != None :
        oent = entities
        human = human + int(choice.find("result").find("human").text)
        entities = human + robot
        if entities > oent:
            for i in range(oent+1,entities + 1):
                if i == 1:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Human/HF.png"), 40, 280, 3, 3, "Human", 3, 1))
                if i == 2:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Human/HF.png"), 60, 230, 3, 3, "Human", 3, 2))
                if i == 3:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Human/HF.png"), 220, 50, 3, 3, "Human", 3, 3))
                if i == 4:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Human/HF.png"), 320, 50, 3, 3, "Human", 3, 4))
                if i == 5:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Human/HF.png"), 210, 480, 3, 3, "Human", 1, 5))
                if i == 6:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Human/HF.png"), 590, 290, 3, 3, "Human", 4, 6))
                if i == 7:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Human/HF.png"), 440, 290, 3, 3, "Human", 4, 7))
                if i == 8:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Human/HF.png"), 440, 460, 3, 3, "Human", 4, 8))
        happy = happy + int(choice.find("result").find("happy").text)
        oent = entities
        robot = robot + int(choice.find("result").find("robot").text)
        entities = human + robot
        if entities > oent:
            for i in range(oent+1,entities + 1):
                if i == 1:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Robot/RF.png"), 40, 280, efficiency, efficiency, "Robot", 3, 1))
                if i == 2:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Robot/RF.png"), 60, 230, efficiency, efficiency, "Robot", 3, 2))
                if i == 3:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Robot/RF.png"), 220, 50, efficiency, efficiency, "Robot", 3, 3))
                if i == 4:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Robot/RF.png"), 320, 50, efficiency, efficiency, "Robot", 3, 4))
                if i == 5:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Robot/RF.png"), 210, 480, efficiency, efficiency, "Robot", 1, 5))
                if i == 6:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Robot/RF.png"), 590, 290, efficiency, efficiency, "Robot", 4, 6))
                if i == 7:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Robot/RF.png"), 440, 290, efficiency, efficiency, "Robot", 4, 7))
                if i == 8:
                    entqueue.append(Entity(pygame.image.load("Assets/Sprites/Robot/RF.png"), 440, 460, efficiency, efficiency, "Robot", 4, 8))
        cash = cash + int(choice.find("result").find("cash").text)
        oef = efficiency
        efficiency = efficiency + int(choice.find("result").find("efficiency").text)
        if oef != efficiency:
            updateRobots(efficiency)
        if choice.find("result").find("dialogue") != None and choice.find("result").find("dialogue").text not in dqueue:
            dqueue.append(choice.find("result").find("dialogue").text)
        if(choice.find("result").find("event") != None and choice.find("result").find("event") not in equeue):
            equeue.append(choice.find("result").find("event").text)
        newevent = False
        current = None

#Start: (40 280), dir 3
def a1(e):
    if (e.x > 275):
        if(not e.placed and e.y < 305):
            e.odir = e.dir
            e.dir = 3
        elif not e.placed:
            e.placed = True
            cqueue.append(Chip(pygame.image.load("Assets/Sprites/Chip/Chip.png"), 280, 355, 5, 5))
            e.odir = e.dir
            e.dir = 1
        elif e.y < 280:
            e.odir = e.dir
            e.dir = 4
    elif e.x < 45:
        e.odir = e.dir
        e.dir = 2
        e.placed = False
    return e

#Start: (60,230), dir 3
def a2(e):
    if(e.y > 240 and not e.placed):
        if e.x < 275 and not e.placed:
            e.odir = e.dir
            e.dir = 2
        elif e.y < 305 and not e.placed:
            e.odir = e.dir
            e.dir = 3
        elif not e.placed:
            e.placed = True
            cqueue.append(Chip(pygame.image.load("Assets/Sprites/Chip/Chip.png"), 280, 355, 5, 5))
            e.odir = e.dir
            e.dir = 1
    else:
        if e.y < 220 and e.x < 65 and e.placed:
            e.odir = e.dir
            e.dir = 3
            e.placed = False
        elif e.x < 65 and e.placed:
            e.odir = e.dir
            e.dir = 1
        elif e.y < 240 and e.placed:
            e.odir = e.dir
            e.dir = 4

    return e

#Start: (220,50), dir 3
def a3(e):
    if(e.y > 340):
        if e.x > 240 and not e.placed:
            e.placed = True
            cqueue.append(Chip(pygame.image.load("Assets/Sprites/Chip/Chip.png"), 280, 355, 5, 5))
            e.odir = e.dir
            e.dir = 4
        elif e.y > 340 and not e.placed:
            e.odir = e.dir
            e.dir = 2
        elif e.x < 220 and e.placed:
            e.odir = e.dir
            e.dir = 1
    elif e.y < 50 and e.placed:
        e.odir = e.dir
        e.dir = 3
        e.placed = False

    return e

#Start: (320,50), dir 3
def a4(e):
    if(e.y > 340):
        if e.x < 310 and not e.placed:
            e.placed = True
            cqueue.append(Chip(pygame.image.load("Assets/Sprites/Chip/Chip.png"), 280, 355, 5, 5))
            e.odir = e.dir
            e.dir = 2
        elif e.y > 340 and not e.placed:
            e.odir = e.dir
            e.dir = 4
        elif e.x > 320 and e.placed:
            e.odir = e.dir
            e.dir = 1
    elif e.y < 50 and e.placed:
        e.odir = e.dir
        e.dir = 3
        e.placed = False

    return e

#Start: (210,480), dir 1
def a5(e):
    if(e.y < 340):
        if e.x > 240 and not e.placed:
            e.placed = True
            cqueue.append(Chip(pygame.image.load("Assets/Sprites/Chip/Chip.png"), 280, 355, 5, 5))
            e.odir = e.dir
            e.dir = 4
        elif e.y < 340 and not e.placed:
            e.odir = e.dir
            e.dir = 2
        elif e.x < 210 and e.placed:
            e.odir = e.dir
            e.dir = 3
    elif e.y > 480 and e.placed:
        e.odir = e.dir
        e.dir = 1
        e.placed = False

    return e

#Start: (590, 290), dir 4
def a6(e):
    if(e.x < 280 and not e.placed):
        if(e.y > 310 and not e.placed):
            e.placed = True
            cqueue.append(Chip(pygame.image.load("Assets/Sprites/Chip/Chip.png"), 280, 355, 5, 5))
            e.odir = e.dir
            e.dir = 1
        if(e.x < 280 and not e.placed):
            e.odir = e.dir
            e.dir = 3
    else:
        if(e.y < 290 and e.placed):
            e.odir = e.dir
            e.dir = 4
            e.placed = False
        elif(e.x > 590 and e.placed):
            e.odir = e.dir
            e.dir = 1
        elif(e.y < 300 and e.placed):
            e.odir = e.dir
            e.dir = 2
    return e

#Start: (440, 290), dir 4
def a7(e):
    if(e.x < 280 and not e.placed):
        if(e.y > 310 and not e.placed):
            e.placed = True
            cqueue.append(Chip(pygame.image.load("Assets/Sprites/Chip/Chip.png"), 280, 355, 5, 5))
            e.odir = e.dir
            e.dir = 1
        if(e.x < 280 and not e.placed):
            e.odir = e.dir
            e.dir = 3
    else:
        if(e.y < 290 and e.placed):
            e.odir = e.dir
            e.dir = 4
            e.placed = False
        elif(e.x > 440 and e.placed):
            e.odir = e.dir
            e.dir = 1
        elif(e.y < 300 and e.placed):
            e.odir = e.dir
            e.dir = 2
    return e

#Start: (440, 460), dir 4
def a8(e):
    if (e.x < 360 and not e.placed):
        if e.x < 310 and not e.placed:
            e.placed = True
            cqueue.append(Chip(pygame.image.load("Assets/Sprites/Chip/Chip.png"), 280, 355, 5, 5))
            e.odir = e.dir
            e.dir = 2
        if e.y < 340 and not e.placed:
            e.odir = e.dir
            e.dir = 4
        elif e.x < 340 and not e.placed:
            e.odir = e.dir
            e.dir = 1
    else:
        if e.x > 440 and e.placed:
            if e.y < 460:
                e.placed = False
                e.odir = e.dir
                e.dir = 4
            else:
                e.odir = e.dir
                e.dir = 1
        elif e.y > 480 and e.placed:
            e.odir = e.dir
            e.dir = 2
        elif e.x > 340 and e.placed:
            e.odir = e.dir
            e.dir = 3

    return e

def main():
    # Initialization stuff
    pygame.init()
    logo = pygame.image.load("Assets/UI/Logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Factory Game")
    global screen
    screen = pygame.display.set_mode((1280, 700))
    running = True
    pygame.font.init()
    #Main Game
    while running:
        updatePos()
        drawUI()
        drawEvents()
        drawDialogue()
        drawFactory()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                getChoice(event.pos)
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        updateEvent()
        pygame.display.flip()

genFaces()
main()