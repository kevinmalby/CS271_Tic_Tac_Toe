from Risk import Risk
from montecarlotree import MonteCarloMethod
import globalVals
import time


# Time and see how many times the computer AI beats
# the randomly playing comp players
def main():
    f = open('comparisonsresults.txt','w')
    f.write("%-20s%-20s%-20s%-20s"%("NumSims","Depth","Winning Player", "Length of Game"))
    f.close()
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
            while riskState.GameOver() == -1:
                curPlayer = riskState.players[riskState.playersMove]
                if curPlayer.playerNum == 0:
                    move = curPlayer.MakeMove(riskState,sims,depth)
                    riskState.DoMove(move,curPlayer)
                else:
                    riskState.DoRandomMove(curPlayer)

            t2 = time.time()    
            f = open('comparisonsresults.txt','a')
            f.write('%-20d%-20d%-20d%-20f\n'%(sims,depth,riskState.playersMove,t2-t1))
            f.close()
if __name__ == "__main__":
    main()
