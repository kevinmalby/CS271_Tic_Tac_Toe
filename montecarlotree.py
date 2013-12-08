import random
from math import *
import pygame
import globalVals

class Node:
    def __init__(self, move = None, parent = None, state = None):
        self.move = move
        self.parentNode = parent
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves(state.players[state.playersMove],state.gamePhase)
       # print "UntriedMoves %s\n"%(self.untriedMoves)
       # self.playerJustMoved = state.playerJustMoved
        self.playerJustMoved = state.playersMove
        self.st = state.Clone()

    def SelectChild(self):
        s = sorted(self.childNodes, key = lambda child: child.wins/child.visits + sqrt(2*log(self.visits)/child.visits))
        s = s[-1]
        return s

    def AddChild(self, move, state):
        node = Node(move, self, state)
        self.untriedMoves.remove(move)
        self.childNodes.append(node)
        return node

    def GetNumDescendents(self, node):
        if node == None:
            return
        
        for c in node.childNodes:
            globalVals.numNodes += 1
            self.GetNumDescendents(c)
            


    def Update(self, result):
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "Node: Player: %s Move: %s Wins: %d Visits: %d\n UntriedMoves: %s\n\n "%(self.playerJustMoved, self.move, self.wins, self.visits, self.untriedMoves)

class MonteCarloMethod:
    
    def TreeSearch(self, rootstate, numIterations, drawtree = False, numRandMoves = 10000000):
        rootnode = Node(None, None, rootstate)
        size = width, height = 1640, 1024

      
        for i in range(numIterations):
            print i
            curNode = rootnode
            curState = rootstate.Clone()
            #print "Root: %s\n"%(curNode)
            #print "Root state: %-8s\n"%(curNode.st)

            if (drawtree == True):
                print 'New Screen: ' + str(i)
                screen = pygame.display.set_mode(size)
                self.DrawTree(curNode, 790, 10, screen)
                done = False
                while done != True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            done = True
            
            # Select Step - Selection is based on the 
            # UCB1 Formula ( CurrentNodeWinRatio + Sqrt(2*log(TotalSimulations)/VisitsAtThisNode) )
            while curNode.untriedMoves == [] and curNode.childNodes != []:
                curNode = curNode.SelectChild()
             #   print "Chosen Child: %s\n"%(curNode)
                #curState.DoMove(curNode.move, curState.players[curState.playersMove])
                curState = curNode.st.Clone()
              #  print "New State: %s\n"%(curState)

            # Expand - If there are still moves to try, select one at random and expand the node with that move
            if curNode.untriedMoves != []:
                move = random.choice(curNode.untriedMoves)
               # print "\tMove: %s"%(move)
                curState.DoMove(move,curState.players[curState.playersMove])
                #print "\tNew State"%(curState)
                curNode = curNode.AddChild(move, curState)

            # Rollout - Randomly play games from this point until game finishes
            cnt = 0
            while curState.GameOver(True) == -1 and cnt < numRandMoves:
                curState.DoRandomMove(curState.players[curState.playersMove])
                cnt += 1

#            print "Final State: %s\n\n\n"%(curState)
            # Backpropogate - After the game is over, propogate the result of it (win/loss) through the expanded
            # nodes. Each node is updated with respect to which player won or lost
            while curNode != None:
                curNode.Update(curState.Score(curNode.playerJustMoved))
                curNode = curNode.parentNode
        return sorted(rootnode.childNodes, key = lambda node: node.visits)[-1].move

    # This is a recursive function that will draw the current Monte Carlo tree in memory
    # If this is to work for Risk, multiple lines will need to be changed so as not to be
    # dependent on the knowledge of max states in a Tic Tac Toe game
    def DrawTree(self, node, x, y, screen, depth = -1):

        if node == None:
            return
        else:
            pygame.draw.rect(screen, (100,170,220), (x,y,60,85),0)
            if node.move == None:
                moveStr = 'Root'
            else:
                moveStr = str(node.move)
            childN = node.childNodes
            childNStr = []
            for c in childN:
                childNStr.append(c.move)
            childNStr = str(childNStr)
            parentN = node.parentNode
            if parentN != None:
                if parentN.move == None:
                    parentStr = 'Root'
                else:
                    parentStr = str(parentN.move)
            else:
                parentStr = 'None'
            winsStr = str(node.wins)
            visitsStr = str(node.visits)
            pjmStr = str(node.playerJustMoved)
            font = 'Ariel'

            self.printText(screen, 'Move: ' + moveStr, font, 12, x+5, y+5, (255,255,255))
            self.printText(screen, 'PlayerJM: ' + pjmStr, font, 12, x+5, y+18, (255,255,255))
            self.printText(screen, 'Children: ' + childNStr, font, 12, x+5, y+31, (255,255,255))
            self.printText(screen, 'Parent: ' + parentStr, font, 12, x+5, y+43, (255,255,255))
            self.printText(screen, 'Wins: ' + winsStr, font, 12, x+5, y+56, (255,255,255))
            self.printText(screen, 'Vists: ' + visitsStr, font, 12, x+5, y+69, (255,255,255))
            pygame.display.update()

            y += 155
            depthValSpacing = 120
            depth += 1
            d = 3**depth
            numChildren = len(node.childNodes)
            x = (x+30) - ((numChildren * 60 + ((numChildren - 1) * (depthValSpacing/d))) / 2)
            if depth == 0:
                pastXMiddle = 820
                if numChildren > 1:
                    x = x - ((9-numChildren)*180)/2
            else:
                pastXMiddle = x+((numChildren*60)+((numChildren-1)*(depthValSpacing/d)))/2

            for c in node.childNodes:
                self.DrawTree(c, x, y, screen, depth)
                pygame.draw.lines(screen, (255,255,255), False, [((pastXMiddle), (y-70)), ((x+30),y)], 1)
                pygame.display.update()
                if depth == 0 and numChildren > 1:
                    x += (((9-numChildren)*180)/(numChildren-1)+120) + 60
                else:
                    x += (depthValSpacing/d)+60

    # Prints text to the screen using Pygame library
    def printText(self, screen, txtText, Textfont, Textsize , Textx, Texty, Textcolor):
        # pick a font you have and set its size
        myfont = pygame.font.SysFont(Textfont, Textsize)
        # apply it to text on a label
        label = myfont.render(txtText, 1, Textcolor)
        # put the label object on the screen at point Textx, Texty
        screen.blit(label, (Textx, Texty))
