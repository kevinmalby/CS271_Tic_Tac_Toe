def DoHumanMove(self, player, phase):

    finalMove = []

    # Remember to add something where we update the player that just went

    # If we are in the placement phase do the following
    if phase == 1:
        newArmiesResult = player.GetNewArmies(self)

        if len(newArmiesResult) > 1:
            numNewArmies = newArmiesResult[0]

            for entry in newArmiesResult[1]:
                finalMove.append(entry)

        else:
            numNewArmies = newArmiesResult[0]
    
        # Place the new armies
        while numNewArmies > 0:
            placingResult = self.HumanPlaceArmies(numNewArmies)
            numNewArmies = placingResult[0]
            finalMove.append[placingResult[1]]

        return finalMove

    # If we are in the attacking phase do the following
    if phase == 2:

        numCountriesPrior = len(player.occupiedCountries)

        # Executing the attack phase
        self.HumanAttackOpponents(player)

        if len(player.occupiedCountries) > numCountriesPrior:
            self.GetCard(player) # Still needs to be implemented

    # If we are in the fortifying phase do the following
    if phase == 3:
        # Fill in fortification code

def HumanPlaceArmies(self, numNewArmies, player):
    
    print 'You currently have the shown number of armies in the corresponding countries:\n'
    for key, value in player.occupiedCountries:
        print key + ': ' + str(value)

    moveDone = False
    while moveDone != True:

        moveDone = True

        # Select which country in which to add armies
        countrySelect = raw_input('Please type the name of the country in which you wish to place armies: ')
        matchFound = False
        for key in player.occupiedCountries:
            if key == countrySelect:
                matchFound = True
                break;
        if matchFound != True:
            moveDone = False
            print 'That was not the name of an actual country or you do not occupy that territory.\n'
            continue

        # Select the number of armies to place in that country
        armiesToPlace = raw_input('Please type the number of armies you wish to place in ' + countrySelect)
        try:
            armiesToPlaceNum = int(armiesToPlace)
        except:
            moveDone = False
            print 'That was not a number.\n'
        if armiesToPlaceNum < 1 or armiesToPlace > numNewArmies:
            moveDone = False
            print 'You must place at least 1 army in the country and no more than the number of armies you have left.'

    # Setup the tuple to be returned as the result
    # The first half contains the updated number of armies, and the second half contains the army movement dictionary
    updatedArmies = numNewArmies - armiesToPlaceNum
    return (updatedArmies, [countrySelect,armiesToPlaceNum])


def HumanAttackOpponents(self, player):
    
    moveDone = False
    while moveDone != True:
        moveDone = True

        # Select which country to attack from
        attacker = raw_input('Please type the name of the country you want to attack from: ')
        matchFound = False
        
        # Make sure that it is a valid country
        for key in self.countries:
            if key == attacker:
                matchFound = True
                break;
        if matchFound != True:
            moveDone = False
            print 'That was not the name of an actual country.\n'
            continue
        
        # Select which country to attack 
        victim = raw_input('Please type the name of the country you want to attack: ')
        matchFound = False
       
        # Make sure that it is a valid country
        for key in self.countries:
            if key == victim:
                matchFound = True
                break;
        if matchFound != True:
            moveDone = False
                matchFound = True
                break;
        if matchFound != True:
            moveDone = False
            print 'That was not the name of an actual country.\n'
            continue

        # Make sure that they aren't trying to attack their own country
        ownCountry = False
        for key in player.occupiedCountries:
            if key == victim:
                ownCountry = True
                break;
        if ownCountry == True:
            moveDone = False
            print 'You cannot attack your own country.\n'
            continue

    return [attacker, victim]
        # attackedPlayer = self.countries[victim][1][0]

        # # Roll the Dice
        # numDice = raw_input('You have %d armies. How many dice do you want to roll? '%(player.occupiedCountries[attacker]))
        # if numDice > player.occupiedCountries[attacker]-1 or numDice < 1 or numDice > 3:
        #     moveDone = False
        #     print 'You cannot roll more dice than armies and one army must stay behind.'
        #     continue
        # else:
        #     numDefDice = raw_input( 'Victim country has %d armies. How many dice does player %d  want to roll? '%(self.countries[victim][1][attackedPlayer], attackedPlayer))
        #     if numDefDice > self.countries[victim][1].values()[0] or numDefDice < 1 or numDefDice > 2:
        #         moveDone = False
        #         print "Invalid number of dice."
        #         continue
        
        # # Count up losses
        # attackerRoll = self.rollDice(numDice)
        # defenderRoll = self.rollDice(numDefDice)
        # print "Attacker rolled: %d"%(attackerRoll)
        # print "Defender rolled: %d"%(defenderRoll)
        
        # for res in [x[0]-x[1] for x in zip(attackerRoll, defenderRoll)]:
        #     # Attacker Loses Armies
        #     if res == 0:
        #         self.countries[attacker][1][player] -= 1
        #         player.occupiedCountries[attacker] -= 1
        #         print "Player %d loses 1 army"%(player.playerNum)
        #     elif res < 0:
        #         self.countries[attacker][1][player] += res
        #         player.occupiedCountries[attacker] += res
        #         print "Player %d loses %d armies"%(player.playerNum, res * -1)
        #     # Victim loses armies
        #     else:
        #         self.countries[victim][1][attackedPlayer] -= res
        #         player.occupiedCountries[victim] -= res
        #         print "Player %d loses %d army"%(attackedPlayer, res)
                                       
        #     # Attack Again?
        # resume = raw_input("Do you want to attack some more? Y/N")
        # if resume == 'Y':
        #     moveDone = False

                
