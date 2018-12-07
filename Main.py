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

def updateEvent():
    global newevent
    global delay
    if not current != None and newevent:
        newevent = True
        delay = False

def genFaces():
    global hfaces
    global rfaces
    hfaces.append(pygame.image.load("Assets/Faces/Male1.png"))
    hfaces.append(pygame.image.load("Assets/Faces/Male2.png"))
    hfaces.append(pygame.image.load("Assets/Faces/Male3.png"))
    hfaces.append(pygame.image.load("Assets/Faces/Male4.png"))
    hfaces.append(pygame.image.load("Assets/Faces/Female1.png"))
    hfaces.append(pygame.image.load("Assets/Faces/Female2.png"))
    hfaces.append(pygame.image.load("Assets/Faces/Female3.png"))
    hfaces.append(pygame.image.load("Assets/Faces/Female4.png"))
    rfaces.append(pygame.image.load("Assets/Faces/Robot1.png"))
    rfaces.append(pygame.image.load("Assets/Faces/Robot2.png"))
    rfaces.append(pygame.image.load("Assets/Faces/Robot3.png"))

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
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
    background = pygame.image.load("Assets/UI/Background.png").convert()
    background = pygame.transform.scale(background, (720, 720))
    chatbox = pygame.image.load("Assets/UI/ChatBox.png").convert()
    chatbox = pygame.transform.scale(chatbox, (720, 180))
    optionbox = pygame.image.load("Assets/UI/OptionBox.png").convert()
    optionbox = pygame.transform.scale(optionbox,(560,360))
    computerscreen = pygame.image.load("Assets/UI/ComputerScreen.png")
    happycounter = pygame.image.load("Assets/UI/HappyCounter.png")
    robcounter = pygame.image.load("Assets/UI/RobotCounter.png")
    humcounter = pygame.image.load("Assets/UI/HumanCounter.png")
    cashcounter = pygame.image.load("Assets/UI/CashCounter.png")
    screen.blit(background, [0, 0])
    screen.blit(chatbox, [0, 720])
    screen.blit(optionbox,[720,540])
    screen.blit(computerscreen,[720,0])
    screen.blit(happycounter, [770,80])
    screen.blit(robcounter, [880, 80])
    screen.blit(humcounter, [990, 80])
    screen.blit(cashcounter, [1100, 80])

def drawOptions(options):
    global screen
    buttonBox = pygame.image.load("Assets/UI/ButtonBox.png")
    buttonBoxHover = pygame.image.load("Assets/UI/ButtonBoxHover.png")
    global pos
    coords = pos
    if(coords[0] in range(780,990) and coords[1] in range(590,720)):
        screen.blit(buttonBoxHover, [780, 590])
    else:
        screen.blit(buttonBox, [780, 590])
    if (coords[0] in range(1010, 1240) and coords[1] in range(590, 720)):
        screen.blit(buttonBoxHover, [1010, 590])
    else:
        screen.blit(buttonBox, [1010, 590])
    if (coords[0] in range(780, 990) and coords[1] in range(730, 860)):
        screen.blit(buttonBoxHover, [780, 730])
    else:
        screen.blit(buttonBox, [780, 730])
    if (coords[0] in range(1010, 1240) and coords[1] in range(730, 860)):
        screen.blit(buttonBoxHover, [1010, 730])
    else:
        screen.blit(buttonBox, [1010, 730])
    font = pygame.font.SysFont('Courier', 18)
    o1RectText = pygame.Rect(790,600,190,85)
    o2RectText = pygame.Rect(1020, 600, 190, 85)
    o3RectText = pygame.Rect(790,740,190,85)
    o4RectText = pygame.Rect(1020,740,190,85)
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
        if time.time() - tm > 4:
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
                if cdia.find("entity").text == "Person":
                    tfaces = hfaces
                else:
                    tfaces = rfaces
                tface = random.randint(1, len(tfaces) - 1)
                while tface == prevface:
                    tface = random.randint(1, len(tfaces) - 1)
                prevface = tface
                face = tfaces[tface]
                oldid = id
                if cdia.find("dialogue").text != None:
                    dqueue.append(cdia.find("dialogue").text)
            diaRectText = pygame.Rect(200, 750, 450, 120)
            if face == None:
                return
            screen.blit(face, [50, 750])
            font = pygame.font.SysFont('Courier', 20)
            drawText(screen, cdia.find("message").text, (255, 255, 255), diaRectText, font)
    else:
        tm = time.time()

def drawFactory():
    global screen
    robot = pygame.image.load("Assets/Sprites/Human/Human.png")
    robot = pygame.transform.scale(robot, (40, 50))
    screen.blit(robot, [400, 400])
    chip = pygame.image.load("Assets/Sprites/Chip/Chip.png")
    screen.blit(chip, [280, 455])

def drawInfo(message):
    global screen
    global human
    global happy
    global robot
    global cash
    compRectText = pygame.Rect(780,120,440,350)
    font = pygame.font.SysFont('Courier', 20)
    uifont = pygame.font.SysFont('Courier', 15)
    happyRectText = pygame.Rect(810, 87, 50,20)
    drawText(screen, str(happy), (0,0,0), happyRectText,uifont)
    robotRectText = pygame.Rect(920, 87, 50,20)
    drawText(screen, str(robot), (0,0,0), robotRectText,uifont)
    humanRectText = pygame.Rect(1030, 87, 50,20)
    drawText(screen, str(human), (0,0,0), humanRectText,uifont)
    cashRectText = pygame.Rect(1140, 87, 80,20)
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
    choice = None
    if current == None:
        return
    if (coords[0] in range(780, 990) and coords[1] in range(590, 720)):
        choice = current.find("options").find("o1")
    if (coords[0] in range(1010, 1240) and coords[1] in range(590, 720)):
        choice = current.find("options").find("o2")
    if (coords[0] in range(780, 990) and coords[1] in range(730, 860)):
        choice = current.find("options").find("o3")
    if (coords[0] in range(1010, 1240) and coords[1] in range(730, 860)):
        choice = current.find("options").find("o4")
    if choice != None and choice.find("message").text != None :
        human = human + int(choice.find("result").find("human").text)
        happy = happy + int(choice.find("result").find("happy").text)
        robot = robot + int(choice.find("result").find("robot").text)
        cash = cash + int(choice.find("result").find("cash").text)
        if choice.find("result").find("dialogue") != None and choice.find("result").find("dialogue").text not in dqueue:
            dqueue.append(choice.find("result").find("dialogue").text)
        if(choice.find("result").find("event") != None and choice.find("result").find("event") not in equeue):
            equeue.append(choice.find("result").find("event").text)
        newevent = False
        current = None
def main():
    # Initialization stuff
    pygame.init()
    logo = pygame.image.load("Assets/UI/Logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Factory Game")
    global screen
    screen = pygame.display.set_mode((1280, 900))
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
        updateEvent()
        pygame.display.flip()

genFaces()
main()