from Risk import Risk

def main():
    riskState = Risk('countries.txt','territory_cards.txt', 4)

    riskState.randomizeInitialState()
    riskState.playersMove = 0
    initPlayer = riskState.players[riskState.playersMove]
    initPlayer.LongPrint()
    riskState.setContinentControl()
    numA = initPlayer.GetNewArmies(riskState)
    initPlayer.numArmiesPlacing = numA


    while True:
        curPlayer = riskState.players[riskState.playersMove]

        # Determine the continents that each player possesses
        #riskState.setContinentControl()

        if riskState.playersMove == 1:
            move = riskState.DoHumanMove(curPlayer)
            print move
            riskState.DoMove(move, curPlayer)
        elif riskState.playersMove == 0:
            # move = riskState.DoHumanMove(curPlayer)
            # print move
            # riskState.DoMove(move, curPlayer)
            print '############# The state of the game before the computer moved ####################################'
            curPlayer.LongPrint()
            print 'The whole state is:'
            print riskState
            print '############# End The state of the game before the computer moved ####################################'
            riskState.DoRandomMove(curPlayer)
            print '############# The state of the game after the computer moved ####################################'
            curPlayer.LongPrint()
            print 'The whole state is:'
            print riskState
            print '############# End The state of the game after the computer moved ####################################'
        else:
            pass

if __name__ == "__main__":
    main()