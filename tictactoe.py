import random
import sys
import globalVals

class TicTacToe:

    def __init__(self):
      self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
      self.playerJustMoved = globalVals.maxPlayers

    def Clone(self):
        clone = TicTacToe()
        clone.board = self.board[:]
        clone.playerJustMoved = self.playerJustMoved
        return clone

    def DoMove(self, move):
        self.playerJustMoved = (self.playerJustMoved % globalVals.maxPlayers) + 1
        self.board[move] = self.playerJustMoved

    def GetMoves(self):
        moves = []
        for i in range(9):
            if self.board[i] == 0:
                moves.append(i)
        return moves

    def DoRandomMove(self):
        self.playerJustMoved = (self.playerJustMoved % globalVals.maxPlayers) + 1
        self.board[random.choice(self.GetMoves())] = self.playerJustMoved
        

    def DoHumanMove(self):
        if self.playerJustMoved == 1:
            typeMove = 'O'
        else:
            typeMove = 'X'

        moveDone = False
        while moveDone != True:
            moveDone = True
            move = raw_input('Enter a position number for an ' + typeMove + ': ')
            try:
                intMove = int(move)
            except:
                move = raw_input('That was not a number, please try again: ')
                moveDone = False
            if intMove not in range(9):
                move = raw_input('That move is not a valid position, please try again: ')
                moveDone = False
            if self.board[intMove] != 0:
                move = raw_input('That move is taken, please try again: ')
                moveDone = False

        return intMove


    def __repr__(self):
        s = ''
        i = 0;
        for spot in self.board:
            s += '_XO'[spot]
            if i % 3 is 2:
                s += '\n'
            i += 1
        s += '\n\n'
        return s


    def CheckFullBoard(self):
        for spot in self.board:
            if spot == 0:
                return False;
        return True


    def CheckEndingConditions(self, playerJustMoved):

        for (x,y,z) in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
            if self.board[x] == self.board[y] == self.board[z] and self.board[x] != 0:
                if self.board[x] == playerJustMoved:
                    return 1.0
                else:
                    return 0.0
        if self.GetMoves() == []:
            return 0.5 # draw
        return -1

