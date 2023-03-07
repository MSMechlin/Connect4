import pygame
import Board 
import Database

screen = pygame.display.set_mode((100, 100))
my_font = 0

def init_screen(w,h):
    pygame.init()
    global screen
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption("CSE350 prototype")  
    global my_font 
    my_font = pygame.font.SysFont("monospace", 20)                         
"""
def gameoverScreen():
    pygame.draw.rect(screen,(255,255,255),(0,0,700,600))
    text = my_font.render("Game over", True, (0, 0, 0)) 
    textRect = text.get_rect()
    textRect.center = (350, 50) 
    screen.blit(text,textRect)
    pygame.display.update()
"""
class BoardInterface:
    def __init__(self,players,connection,remote,dim,pandim,redim):
        self.log = Database.Database()
        self.board = Board.Board()
        #SETUP BOARD SURFACE
        self.boardWidth = dim[0]
        self.boardHeight = dim[1]
        self.boardSurface = pygame.Surface((self.boardWidth,self.boardWidth))
        self.xPosition = dim[2]
        self.yPosition = dim[3]
        self.screen = screen
        if(dim[0]/7 < dim[1]/6):
            self.checkerRadius = dim[0]*.8/14
        else:
            self.checkerRadius = dim[1]*.8/12
        self.columnWidth = dim[0]/7
        self.rowHeight = dim[1]/6
        self.drawBoard()
        #SETUP PLAYER PANELS
        self.players = players
        self.panelWidth = pandim[0]
        self.panelHeight = pandim[1]
        self.p1pos = (pandim[2],pandim[3])
        self.p2pos = (pandim[4],pandim[5])
        self.panels = [pygame.Surface((self.panelWidth,self.panelHeight)),pygame.Surface((self.panelWidth,self.panelHeight))]
        self.drawPanels(0)
        #SETUP REWIND PANEL
        self.rewindWidth = redim[0]
        self.rewindHeight = redim[1]
        self.rewindXPos = redim[2]
        self.rewindYPos = redim[3]
        self.rewindPanel = pygame.Surface((self.rewindWidth,self.rewindHeight))
        self.drawRewind()
        #SETUP CLICK-SENSITIVE COLUMNS
        self.columns = [pygame.Rect(0,0,0,0)]*7
        for i in range(7):
            self.columns[i] = pygame.Rect(self.columnWidth*i+self.xPosition,self.yPosition,self.columnWidth,self.boardHeight)
        self.remote = remote
        self.connection = connection
        #self.drawPanels(players[0].name,players[1].name)
        #self.drawRewind()
######################################################################################################################

######################################################################################################################
    def drawRewind(self):
        print(self.rewindXPos)
        print(self.rewindYPos)
        self.rewindButtons = [pygame.Rect(0,0,0,0)]*4
        self.rewindSurfaces = [pygame.Surface((0,0))]*4
        for i in range(4):
            self.rewindButtons[i] = pygame.Rect(self.rewindXPos+i*self.rewindWidth/4,self.rewindYPos,self.rewindWidth/4,self.rewindHeight)
            self.rewindSurfaces[i] = pygame.Surface((self.rewindWidth/4,self.rewindHeight))
        pygame.draw.polygon(self.rewindSurfaces[0],(255,255,255),[(10,50),(40,90),(40,10)])
        pygame.draw.polygon(self.rewindSurfaces[0],(255,255,255),[(60,50),(90,90),(90,10)])
        pygame.draw.polygon(self.rewindSurfaces[1],(255,255,255),[(25,50),(75,90),(75,10)])
        pygame.draw.polygon(self.rewindSurfaces[2],(255,255,255),[(75,50),(25,90),(25,10)])
        pygame.draw.polygon(self.rewindSurfaces[3],(255,255,255),[(40,50),(10,90),(10,10)])
        pygame.draw.polygon(self.rewindSurfaces[3],(255,255,255),[(90,50),(60,90),(60,10)])
        self.rewindPanel.fill((100,100,100))
        screen.blit(self.rewindPanel,(self.rewindXPos,self.rewindYPos))
        for i in range(4):
            screen.blit(self.rewindSurfaces[i],self.rewindButtons[i])
        pygame.display.update()
######################################################################################################################

######################################################################################################################
    def drawPanels(self,turn):
        self.panels[0].fill((100,100,100))
        self.panels[1].fill((100,100,100))
        pygame.draw.rect(self.panels[turn],self.players[turn].color,(0,0,self.panelWidth,self.panelHeight),8)
        screen.blit(self.panels[0],(self.p1pos[0],self.p1pos[1]))
        screen.blit(self.panels[1],(self.p2pos[0],self.p2pos[1]))
        text = my_font.render(self.players[0].name, True, (0, 0, 0)) 
        textRect = text.get_rect()
        textRect.center = (self.p1pos[0]+self.panelWidth/2,self.p1pos[1]+self.panelHeight/2) 
        screen.blit(text,textRect)
        text = my_font.render(self.players[1].name, True, (0, 0, 0)) 
        textRect = text.get_rect()
        textRect.center = (self.p2pos[0]+self.panelWidth/2,self.p2pos[1]+self.panelHeight/2) 
        screen.blit(text,textRect)
        pygame.display.update()
######################################################################################################################

######################################################################################################################
    def inputCommand(self,turn):
        print(f"Player {turn} turn.")
        if self.players[turn].inputType == 0:
            print("(Human)")
            pos = self.humanInput()
        elif self.players[turn].inputType == 1:
            print("(Remote)")
            pos = self.remoteInput()
        if pos != 7:
            self.board.placeChecker(pos)
        self.drawBoard()
        self.drawRewind()
        self.drawPanels((turn+1)%2)
        self.log.logMove(self.board.checkers)
        if self.remote and self.players[turn].inputType != 1:
            self.connection.send(str(pos).encode('utf-8'))
            if pos == 7:
                print("Goodbye")
                exit()
        return self.board.over
######################################################################################################################

######################################################################################################################
    def humanInput(self):
        waiting = True
        j = 0
        pygame.event.clear()
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 7
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(7):
                        if self.columns[i].collidepoint(pygame.mouse.get_pos()):
                            if(self.board.verify(i)):
                                return i
                            else:
                                break
            pygame.display.update()
######################################################################################################################

######################################################################################################################
    def remoteInput(self):
        waiting = True
        print("Client is awaiting opponent's command")
        while waiting:
            move = self.connection.recv(64).decode('utf-8')
            if not move:
                pass
            elif int(move) >= 0 and int(move) < 7:
                print("Valid move")
                return int(move)
            elif int(move) == 7:
                print("Bye, bye")
                pygame.QUIT()
                exit()
            else:
                print("invalid move")
            pygame.display.update()
######################################################################################################################

######################################################################################################################
    def drawBoard(self):
        print("column width:" + str(self.boardWidth))
        print("height:" + str(self.boardHeight))
        print(self.checkerRadius)
        pygame.draw.rect(self.boardSurface,(0,0,255),(0,0,self.boardWidth,self.boardHeight))
        for i in range(6):
            for j in range(7):
                if self.board.checkers[i][j] == 0:
                    color = (0,0,0)
                else:
                    color = self.players[self.board.checkers[i][j]-1].color
                pygame.draw.circle(self.boardSurface,color, #the color parameter here is the only thing that changed
                (int(self.columnWidth/2 + j*self.columnWidth),int(self.boardHeight-(self.rowHeight/2 + i*self.rowHeight))),
                self.checkerRadius)
        self.screen.blit(self.boardSurface,(self.xPosition,self.yPosition))
        pygame.display.update()
######################################################################################################################

######################################################################################################################
    def rewind(self,input):
        match(input):
            case 0:
                print("To the beginning")
                reload = self.log.beginning()
            case 1:
                print("One step back")
                reload = self.log.back()
            case 2:
                print("One step forward")
                reload = self.log.forward()
            case 3:
                print("To the end")
                reload = self.log.end()    
        self.board.reload(reload)
        print(self.board.checkers)
        self.drawBoard()
        self.drawRewind()
######################################################################################################################

######################################################################################################################
    def gameOver(self):
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(4):
                        if self.rewindButtons[i].collidepoint(pygame.mouse.get_pos()):
                            self.rewind(i)