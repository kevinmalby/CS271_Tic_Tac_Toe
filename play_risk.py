from Risk import Risk

def main():
    riskState = Risk('countries.txt','territory_cards.txt', 4)

    riskState.randomizeInitialState()
    print str(riskState)

    while riskState.GetMoves() != []:
        print str(riskState)
        curPlayer = riskState.players[riskState.playersMove]

        # if riskState.playersMove == 0:
        #     pass
        #     # First execute the placement phase


        #     # Then execute the attacking phase

        #     # Finally, execute the fortification phase


        #     #riskState.DoHumanMove()
        # elif riskState.playersMove == 1:
        #     pass
        # elif riskState.playersMove == 2:
        #     pass
        # elif riskState.playersMove == 3:
        #     pass
        # elif riskState.playersMove == 4:
        #     pass
        # else
        #     pass

        #riskState.DoMove() # Execute move of form DoMove(phase, ['north america', 'alaska'])

if __name__ == "__main__":
    main()