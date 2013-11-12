from tictactoe import TicTacToe
import globals
import sys, pygame
from montecarlotree import MonteCarloMethod

def main():

    pygame.init()
    state = TicTacToe()
    mcts = MonteCarloMethod()
    while (state.GetMoves() != []):
        print str(state)
        if state.playerJustMoved == 2:
            m = mcts.TreeSearch(state, 15, False)
        else:
            if len(sys.argv) > 1:
                m = state.DoHumanMove()
            else:
                m = mcts.TreeSearch(state, 15, False)
        print 'Best Move: ' + str(m)
        state.DoMove(m)

        print 'Player to move: ' + str(state.playerJustMoved) + '\n'
        resultOfMove = state.CheckEndingConditions(state.playerJustMoved)
        if resultOfMove != -1:
            break

    print str(state)

    resultOfMove = state.CheckEndingConditions(state.playerJustMoved)

    if resultOfMove == 1.0:
        print 'Player ' + str(state.playerJustMoved) + ' wins!'
    elif resultOfMove == 0.0:
        print 'Player ' + str((state.playerJustMoved % globals.maxPlayers) + 1) + ' wins!'
    else:
        print "It was a cat's game!"


if __name__ == "__main__":
    main()