import numpy

def encode(rows):
    enc = numpy.zeros(6,int)
    for i in range(6):
        for j in range(7):
            enc[i] += rows[i][j] * pow(3,j)
    return enc
def decode(rows):
    #dec = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
    dec = numpy.zeros((6,7),int)
    for i in range(6):
        row = rows[i]
        for j in range(7):
            dec[i][j] = row%3
            row //= 3
    return dec
    
class Movelog:
    def __init__(self):
        self.log = numpy.zeros((42,6),int)
    def access(self,cursor):
        return decode(self.log[cursor])
    def write(self,data,cursor):
        self.log[cursor] = encode(data)

class Database:
    def __init__(self):
        self.moveLog = Movelog()
        self.currentMove = -1
        self.cursor = -1
    def logMove(self,board):
        self.currentMove += 1
        self.cursor += 1
        self.moveLog.write(board,self.cursor)
    def back(self):
        self.cursor -= 1
        if self.cursor == -1:
            self.cursor = 0
        print("Cursor position " + str(self.cursor))
        return self.moveLog.access(self.cursor)
    def forward(self):
        self.cursor += 1
        if self.cursor == (self.currentMove + 1):
            self.cursor = self.currentMove
        print("Cursor position " + str(self.cursor))
        return self.moveLog.access(self.cursor)
    def beginning(self):
        self.cursor = 0
        print("Cursor position " + str(self.cursor))
        return self.moveLog.access(self.cursor)
    def end(self):
        self.cursor = self.currentMove
        print("Cursor position " + str(self.cursor))
        return self.moveLog.access(self.cursor)