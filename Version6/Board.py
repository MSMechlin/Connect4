import numpy

class Board:
    def __init__(self):
        self.checkers = numpy.array([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],numpy.uint8)
        self.columnHeights = numpy.array([0,0,0,0,0,0,0],numpy.uint8)
        self.currentPlayer = 0
        self.over = False
        self.turnNumber = 0
    def placeChecker(self,pos):
        self.checkers[self.columnHeights[pos]][pos] = self.currentPlayer + 1
        self.columnHeights[pos] += 1
        self.lastMove = pos
        #print(self.checkers)
        self.over = self.gameCheck(pos)
        self.currentPlayer = self.currentPlayer+1
        self.currentPlayer = self.currentPlayer%2
        
        self.turnNumber += 1
    def gameCheck(self,lastMove):
        x = lastMove
        y = self.columnHeights[lastMove]-1
        """Check down"""
        count = 1
        cursor = 1
        while(y-cursor > -1 and self.checkers[y-cursor][x] == self.currentPlayer+1):
            cursor += 1
            count +=1
        if count >= 4:
            return True
        """Check Left-Right"""
        count = 1
        cursor = 1
        while(x+cursor < 7 and self.checkers[y][x+cursor] == self.currentPlayer+1):
            cursor += 1
            count +=1
        cursor = 1
        while(x-cursor > -1 and self.checkers[y][x-cursor] == self.currentPlayer+1):
            cursor += 1
            count +=1
        if count >= 4:
            return True
        """Check TopLeft-BottomRight"""
        count = 1
        cursor = 1
        while(y+cursor < 6 and x-cursor > -1 and self.checkers[y+cursor][x-cursor] == self.currentPlayer+1):
            cursor += 1
            count +=1
        cursor = 1
        while(y-cursor > -1 and x+cursor < 7 and self.checkers[y-cursor][x+cursor] == self.currentPlayer+1):
            cursor += 1
            count +=1
        if count >= 4:
            return True    
        """Check TopRight-BottomLeft"""
        count = 1
        cursor = 1
        while(y+cursor < 6 and x+cursor < 7 and self.checkers[y+cursor][x+cursor] == self.currentPlayer+1):
            cursor += 1
            count +=1
        cursor = 1
        while(y-cursor > -1 and x-cursor > -1 and self.checkers[y-cursor][x-cursor] == self.currentPlayer+1):
            cursor += 1
            count +=1
        if count >= 4:
            return True
        else:
            return False
    def verify(self, column):
        return self.columnHeights[column] < 6
    def reload(self,rows):
        self.checkers = rows