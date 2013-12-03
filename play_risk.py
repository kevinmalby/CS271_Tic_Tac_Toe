from Risk import Risk
import random

def main():
    riskState = Risk('countries.txt','territory_cards.txt', 4)

    riskState.randomizeInitialState()
    riskState.playersMove = 0
    initPlayer = riskState.players[riskState.playersMove]
    initPlayer.LongPrint()
    riskState.setContinentControl()
    

    for i in range(0,7):
        name = random.choice(riskState.territoryCards.keys())
        val = riskState.territoryCards[name]
        new_card = [name, val]
        riskState.territoryCards.pop(new_card[0])
        initPlayer.cards[new_card[0]] = new_card[1]

    numA = initPlayer.GetNewArmies(riskState)
    initPlayer.numArmiesPlacing = numA

    while True:
        curPlayer = riskState.players[riskState.playersMove]

        print riskState
        # Determine the continents that each player possesses
        #riskState.setContinentControl()

        if riskState.playersMove == 1:
            move = riskState.DoHumanMove(curPlayer)
            print move
            if move != 'ignore':
                riskState.DoMove(move, curPlayer)
        elif riskState.playersMove == 0:
            # move = riskState.DoHumanMove(curPlayer)
            # print move
            # riskState.DoMove(move, curPlayer)
            riskState.DoRandomMove(curPlayer)
        else:
            pass

if __name__ == "__main__":
    main()