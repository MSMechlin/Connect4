
import Server
import Interface
import Menu

#Use these to adjust the board's dimensions
BOARD_WIDTH = 700
BOARD_HEIGHT = 600
BOARD_POSX = 250
BOARD_POSY = 100
#Use these to adjust panel dimensions
PANEL_WIDTH = 200
PANEL_HEIGHT = 700
P1_POSX = 50
P1_POSY = 100
P2_POSX = 950
P2_POSY = 100
#Adjust rewind buttons
REWIND_PANEL_WIDTH = 400
REWIND_PANEL_HEIGHT = 100
REWIND_POSX = 400
REWIND_POSY = 700
#These are meant to bottleneck the parameters for the constructor
pandim = (PANEL_WIDTH,PANEL_HEIGHT,P1_POSX,P1_POSY,P2_POSX,P2_POSY)
dim = (BOARD_WIDTH,BOARD_HEIGHT,BOARD_POSX,BOARD_POSY)
redim = (REWIND_PANEL_WIDTH,REWIND_PANEL_HEIGHT,REWIND_POSX,REWIND_POSY)
#These are just the window dimensions. If you get done with the bare bones essentials, see if you can get the window to fullscreen automatically and make the interface resize to suit all screen dimensions
S_WIDTH = 1200
S_HEIGHT = 800

Interface.init_screen(S_WIDTH,S_HEIGHT)   
class Player:
    def __init__(self,p):
        self.color = p["Color"]
        self.inputType = p["Input"]
        self.name = p["Name"]

""" 
Try to make the player creation screen as independent of the rest of the modules as possible.
It will probably only need one function that returns a dictionary with both players' data like so:

Players =   [
                Player1:
                {
                    name:<str>,
                    inputType:<int>
                },
                Player2:
                {
                    name:<str>,
                    inputType:<int>
                }
            ]
We can also consider letting the players customize their colors and making that part the players objects.
From there, it should only take a little tinkering in main.py to hook the module up with the rest of the app.
"""

PlayerInfo = Menu.Setup()
while True:
    
    remote = True
    if PlayerInfo[0]["Input"] == 1:
        ip = input("enter ip")
        connection = Server.logonPlayer2(ip,5050)
        connection.send(PlayerInfo[1]["Name"].encode("utf-8"))
        PlayerInfo[0]["Name"] = connection.recv(1024).decode("utf-8")
        print("Opponents name"+ PlayerInfo[0]["Name"])
    elif PlayerInfo[1]["Input"] == 1:
        server = Server.Server()
        connection = server.getConnection()
        connection.send(PlayerInfo[0]["Name"].encode("utf-8"))
        PlayerInfo[1]["Name"] = connection.recv(1024).decode("utf-8")
        print("Opponents name"+ PlayerInfo[1]["Name"])
    else:
        remote = False
        connection = 0
    break
players = [Player(PlayerInfo[0]),Player(PlayerInfo[1])]
boardInterface = Interface.BoardInterface(players,connection,remote,dim,pandim,redim)
gameover = False
turn = False

#Very simple main loop, you see.
while gameover == False:
    gameover = boardInterface.inputCommand(int(turn))#Check the conditions for gameover again
    turn = not turn

"""
The gameOver function will encapsulate the rewind features. Simply wait for one of the rewind buttons to be pressed and respond appropriately. If the x button is clicked, close the game.
"""
#boardInterface.gameOver()
boardInterface.gameOver()