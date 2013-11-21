from Risk import Risk

def main():
    riskState = Risk('countries.txt','territory_cards.txt', 4)

    riskState.randomizeInitialState()
    print str(riskState)

    while riskState.GetMoves() != []:
        print str(riskState)
        curPlayer = riskState.players[riskState.playersMove]

        if riskState.playersMove == 0:
            # First execute the placement phase


            # Then execute the attacking phase

            # Finally, execute the fortification phase


            riskState.DoHumanMove()
        elif riskState.playersMove == 1:

        elif riskState.playersMove == 2:

        elif riskState.playersMove == 3:

        elif riskState.playersMove == 4:

        else
            riskState.playersMove == 5:

        riskState.DoMove() # Execute move of form DoMove(phase, ['north america', 'alaska'])

if __name__ == "__main__":
    main()