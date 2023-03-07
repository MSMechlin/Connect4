import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())

names = ["",""]
lastMove = ["*","*"]
volley = 0

def handle_client(con,playerNum):
    global volley
    print("Player " + str(playerNum+1) + " has logged on.")
    names[playerNum] = con[0].recv(1024).decode('utf-8')
    print("Player " + str(playerNum+1) + " has entered their name to the server")
    while names[(playerNum+1)%2] == "":
        pass
    con[0].send(names[(playerNum+1)%2].encode('utf-8'))
    while True:
        if volley%2 == playerNum:
            pos = con[0].recv(64).decode('utf-8') #Player's server awaits command
            print(f"Player {playerNum+1}'s move: {pos}")
            lastMove[playerNum] = pos #Update player's move so opponent can leave their waiting loop and update their board.
            volley += 1
        if volley%2 != playerNum:
            print(f"Player {playerNum+1} is Waiting for player {(playerNum+1)%2+1}'s move")
            while lastMove[(playerNum+1)%2] == "*":
                pass
            con[0].send(lastMove[(playerNum+1)%2].encode('utf-8'))
            lastMove[(playerNum+1)%2] = "*" #Last move of opponent has been registered; replace so player can wait again
class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print(SERVER)
        self.sock.bind((SERVER,PORT))
        self.sock.listen()
    def getConnection(self):
        print('Waiting for player 2')
        con = self.sock.accept()
        thread = threading.Thread(target = handle_client, args = (con,1))
        thread.start()

        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print('Logging on player 1')
        client.connect((SERVER,PORT))
        con = self.sock.accept()
        thread = threading.Thread(target = handle_client, args = (con,0))
        thread.start()
        return client
def logonPlayer2(ip,port):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((ip,port))
    return client