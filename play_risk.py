from Risk import Risk
from montecarlotree import MonteCarloMethod
import globalVals

def main():
    riskState = Risk('countries.txt','territory_cards.txt', 4)
    mcts = MonteCarloMethod()

    numHum = 2
    numComp = 2
    riskState.randomizeInitialState(numHum, numComp)
    riskState.playersMove = 0
    initPlayer = riskState.players[riskState.playersMove]
    riskState.setContinentControl()
    numA = initPlayer.GetNewArmies(riskState)
    initPlayer.numArmiesPlacing = numA

    while riskState.GameOver() == -1:
        curPlayer = riskState.players[riskState.playersMove]

        if riskState.playersMove == 1:
            move = riskState.DoHumanMove(curPlayer)
        elif riskState.playersMove == 0:
            move = mcts.TreeSearch(riskState, 30, False)
        else:
            pass

        riskState.DoMove(move, curPlayer)

    resultOfGame = riskState.Score(curPlayer, True)

    if resultOfGame == 1.0:
        print 'Player %d wins.' %(riskState.playersMove)
    else:
        print 'Player %d wins.' %((riskState.playersMove % globalVals.maxPlayers) + 1)

if __name__ == "__main__":
    main()
