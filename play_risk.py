from Risk import Risk

def main():
    riskState = Risk('countries.txt','territory_cards.txt', 4)

    riskState.randomizeInitialState()
    riskState.playersMove = 0
    initPlayer = riskState.players[riskState.playersMove]
    riskState.setContinentControl()
    numA = initPlayer.GetNewArmies(riskState)
    print numA
    initPlayer.numArmiesPlacing = numA
    print str(riskState)

    while True:
        print str(riskState)
        curPlayer = riskState.players[riskState.playersMove]

        # Determine the continents that each player possesses
        #riskState.setContinentControl()

        if riskState.playersMove == 0:
            move = riskState.DoHumanMove(curPlayer)
            print move
            riskState.DoMove(move, curPlayer)
        elif riskState.playersMove == 1:
            move = riskState.DoHumanMove(curPlayer)
            print move
            riskState.DoMove(move, curPlayer)
        else:
            pass

if __name__ == "__main__":
    main()