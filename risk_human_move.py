def DoHumanMove(self, player):

    # Remember to add something where we update the player that just went

    # If we are in the placement phase do the following
    if self.gamePhase == 1:

        # Execute the placement phase
        move = self.HumanPlaceArmies(player.numArmiesPlacing, player)

    # If we are in the attacking phase do the following
    if self.gamePhase == 2:

        # Execute the attack phase
       move = self.HumanAttackOpponents(player)

    # If we are in the fortifying phase do the following
    if self.gamePhase == 3:

        # Execute the fortify phase
        move = self.HumanFortify(player)

    return move

def HumanPlaceArmies(self, numNewArmies, player):
    
    print 'You currently have the shown number of armies in the corresponding countries:\n'
    for key, value in player.occupiedCountries:
        print key + ': ' + str(value)

    moveDone = False
    while moveDone != True:

        moveDone = True

        # Select which country in which to add armies
        countrySelect = raw_input('Please type the name of the country in which you wish to place armies: ')
        if countrySelect not in player.occupiedCountries:
            print 'That was not the name of an actual country or you do not occupy that territory.\n'
            moveDone = False
            continue

        # Select the number of armies to place in that country
        armiesToPlace = raw_input('Please type the number of armies you wish to place in ' + countrySelect)
        try:
            armiesToPlaceNum = int(armiesToPlace)
        except:
            moveDone = False
            print 'That was not a number.\n'
            continue
        if armiesToPlaceNum < 1 or armiesToPlace > numNewArmies:
            moveDone = False
            print 'You must place at least 1 army in the country and no more than the number of armies you have left.'

    # Setup the dictionary to return
    # The first half contains the updated number of armies, and the second half contains the army movement dictionary
    return {countrySelect:(countrySelect, armiesToPlaceNum)}


def HumanAttackOpponents(self, player):
    
    moveDone = False
    while moveDone != True:
        moveDone = True

        # Select which country to attack from
        attacker = raw_input('Please type the name of the country you want to attack from: ')
        
        # Make sure that it is a valid country
        if attacker not in self.countries and attacker not in player.occupiedCountries:
            print 'That was not the name of an actual country or it was not your own country.\n'
            moveDone = False
            continue
        
        # Select which country to attack 
        victim = raw_input('Please type the name of the country you want to attack: ')
       
        # Make sure that it is a valid country
        if victim not in self.countries:
            print 'That was not the name of an actual country.\n'
            moveDone = False
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

    opponentArmies = self.countries[victim][1]
    opponentArmies = opponentArmies[opponentArmies.keys()[0]]
    print('\nYou currently have %d armies in your attacking country [%s],\
     the opponent you are attacking has %d armies in their country [%s]' %(player.occupiedCountries[attacker],\
        attacker, opponentArmies, victim))

    moveDone = False
    while moveDone == False:
        moveDone = True
        attackCount = raw_input('How many armies would you like to attack with?')
        try:
            attackCount = int(attackCount)
        except:
            print 'That was not a number'
            moveDone = False
            continue

        if attackCount > player.occupiedCountries[attacker] - 1 or attackCount < 0:
            print 'That number is outside the range of the number of armies in your country'
            moveDone = False

    return {attacker:(victim, attackCount)}

    
def HumanFortify(self, player):

    moveDone = False
    while moveDone != True:
        moveDone = True

        # Select which country to fortify from
        fortifyFrom = raw_input('Please type the name of the country from which you want to fortify armies: ')
        
        # Make sure that it is a valid country
        if fortifyFrom not in self.countries and fortifyFrom not in player.occupiedCountries:
            print 'That was not the name of an actual country or it was not your own country.\n'
            moveDone = False
            continue

        # Select which country to fortify to
        fortifyTo = raw_input('Please type the name of the country to which you want to fortify armies')

        # Make sure that it is a valid country
        if fortifyTo not in self.countries and fortifyTo not in player.occupiedCountries:
            print 'That was not the name of an actual country or it was not your own country.\n'
            moveDone = False
            continue
            
        # Make sure that the countries are adjacent
        adjacentToFortifyFrom = self.countries[fortifyFrom][0]

        matchFound = False
        for country in adjacentToFortifyFrom:
            if fortifyTo == country:
                matchFound = True
                break;
        if matchFound == False:
            print 'The chosen countries must be adjacent to each other'
            moveDone = False


    moveDone = False
    while moveDone == False:
        moveDone = True
        fortifyCount = raw_input('How many armies would you like to fortify?')
        try:
            fortifyCount = int(fortifyCount)
        except:
            print 'That was not a number'
            moveDone = False
            continue

        if fortifyCount > player.occupiedCountries[fortifyFrom] - 1 or fortifyCount < 0:
            print 'That number is outside the range of the number of armies in your country'
            moveDone = False
            continue

    return {fortifyFrom:(fortifyTo, fortifyCount)}

