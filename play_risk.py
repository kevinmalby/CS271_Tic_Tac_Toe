from Risk import Risk

def main():
    riskState = Risk('countries.txt','territory_cards.txt', 4)

    riskState.randomizeInitialState()
    print str(riskState)

    while riskState.GetMoves() != []:
        print str(riskState)
        curPlayer = riskState.players[riskState.playersMove]

        # Determine the continents that each player possesses
        riskState.setContinentControl()


        if riskState.playersMove == 0:
            pass

            # First determine the number of armies that the player can place
            totalArmiesThisTurn = curPlayer.GetNewArmies(riskState)
            curArmies = totalArmiesThisTurn

            # Execute the placement phase
            while curArmies > 0:
                placingResult = riskState.HumanPlaceArmies(curArmies, curPlayer)
                curArmies = placingResult[0]
                riskState.DoMove(placingResult[1])


            # Execute the attacking phase
            

            # Finally, execute the fortification phase


            #riskState.DoHumanMove()

if __name__ == "__main__":
    main()