import random
import sys

class TicTacToe:

    def __init__(self):
      self.board = ['_', '_', '_', '_','_', '_', '_', '_','_']

    def NewBoard(self):
        self.board = ['_', '_', '_', '_','_', '_', '_', '_','_']
        return self.board;

    def PrintBoard(self):
        i = 0;
        for spot in self.board:
            sys.stdout.write(spot)
            if i % 3 is 2:
                print
            i += 1
        print
        print

    def XMove(self):

        moveFound = False

        while (moveFound == False):
            move = random.randint(0,8)
            if self.board[move] == '_':
                self.board[move] = 'X'
                moveFound = True
        return self.board

    def OMove(self):

        moveFound = False

        while (moveFound == False):
            move = random.randint(0,8)
            if self.board[move] == '_':
                self.board[move] = 'O'
                moveFound = True
        return self.board

    def PrintWinningStatement(self, moveResult):
        if moveResult == 'X':
            print 'X won the game!'
        elif moveResult == 'O':
            print 'O won the game!'
        elif moveResult == 'C':
            print "It was a cat's game"
        else:
            return

    def CheckFullBoard(self):
        for spot in self.board:
            if spot == '_':
                return False;
        return True


    def CheckEndingConditions(self):
        topLeftCorner = self.board[0]
        if topLeftCorner != '_':
            if ((topLeftCorner == self.board[1] == self.board[2]) or (topLeftCorner == self.board[3] == self.board[6]) or (topLeftCorner == self.board[4] == self.board[8])):
                return topLeftCorner
        bottomRightCorner = self.board[8]
        if bottomRightCorner != '_':
            if ((bottomRightCorner == self.board[2] == self.board[5]) or (bottomRightCorner == self.board[6] == self.board[7])):
                return bottomRightCorner
        middle = self.board[4]
        if middle != '_':
            if ((middle == self.board[1] == self.board[7]) or (middle == self.board[3] == self.board[5])):
                return middle
        if self.CheckFullBoard() == True:
            return 'C'
        return 0

    def SimulateGame(self):
        self.board = self.NewBoard()

        while (True):
            self.PrintBoard()

            self.board = self.XMove()
            moveResult = self.CheckEndingConditions()
            if ((moveResult == 'X') or (moveResult == 'O') or (moveResult == 'C')):
                break

            self.PrintBoard()

            self.board = self.OMove()
            moveResult = self.CheckEndingConditions()
            if ((moveResult == 'X') or (moveResult == 'O') or (moveResult == 'C')):
                break

        self.PrintBoard()
        self.PrintWinningStatement(moveResult)
        print
        print
