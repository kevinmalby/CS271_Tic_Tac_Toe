from Risk import Risk
from montecarlotree import MonteCarloMethod
import globalVals
import time


# Time and see how many times the computer AI beats
# the randomly playing comp players
def main():
    f = open('testingAgainresults01.txt','w')
    f.write("%-20s%-20s%-20s%-20s\n"%("NumSims","Depth","Winning Player", "Length of Game"))
    f.close()
    f1 = open('GameTrace01.txt','w');
    f1.write("\n");
    f1.close()
    for sims in range(600,800,20):
        for depth in range(40,80,5):
            total = 0
            for cnt in range(4):
                riskState = Risk('countries.txt','territory_cards.txt', 4)
            # riskState = Risk('test_map.txt','territory_cards.txt', 4)
                mcts = MonteCarloMethod()
                numHum = 0
                numComp = 4
                riskState.randomizeInitialState(numHum, numComp)
                riskState.playersMove = 0
                initPlayer = riskState.players[riskState.playersMove]
                riskState.setContinentControl()
                numA = initPlayer.GetNewArmies(riskState)
                initPlayer.numArmiesPlacing = numA
                t1 = time.time()
                f1 = open('GameTrace01.txt','a')
                f1.write('Game Number %d %d sims %d depth\n'%(cnt,sims,depth))
                while riskState.GameOver() == -1:
                    curPlayer = riskState.players[riskState.playersMove]
                    if curPlayer.playerNum == 0:
                        move = curPlayer.MakeMove(riskState,sims,depth)
                        f1.write("Player %d: Game Phase %d %s\n"%(curPlayer.playerNum, riskState.gamePhase,move));
                        riskState.DoMove(move,curPlayer)
                        print move
                    else:
                        phase = riskState.gamePhase
                        move =  riskState.DoRandomMove(curPlayer)
                        f1.write("Player %d: Game Phase %d %s\n"%(curPlayer.playerNum, phase,move));
                print 'uuuhhh'
                f1.close()
                t2 = time.time()
                total += t2-t1
            f = open('testingAgainresults01.txt','a')
            f.write('%-20d%-20d%-20d%-20f\n'%(sims,depth,riskState.playersMove,total/4.0))
            f.close()


if __name__ == "__main__":
    main()
