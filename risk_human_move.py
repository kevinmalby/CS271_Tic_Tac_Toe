def DoHumanMove(self, player):
    self.playerJustMoved = player.playerNum
    numNewArmies = player.GetNewArmies() # Within this will be code to calculate how many countries captured and if any continents captured
    
    # Place the new armies
    while numNewArmies > 0:
        numNewArmies = self.HumanPlaceArmies(numNewArmies)

    # Executing the attack phase
    self.HumanAttackOpponents(player)

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
        currentCountry = self.countries[countrySelect]
        currentCountry[1][0] = armiesToPlaceNum
        player.occupiedCountries[countrySelect] = armiesToPlaceNum

        # Return the updated number of armies available for placing
        return numNewArmies - armiesToPlaceNum

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
        attackedPlayer = self.countries[victim][1].keys()[1]

        # Roll the Dice
        numDice = raw_input('You have %d armies. How many dice do you want to roll? '%(player.occupiedCountries[attacker]))
        if numDice > player.occupiedCountries[attacker]-1 or numDice < 1 or numDice > 3:
            moveDone = False
            print 'You cannot roll more dice than armies and one army must stay behind.'
            continue
        else:
            numDefDice = raw_input( 'Victim country has %d armies. How many dice does player %d  want to roll? '%(self.countries[victim][1][attackedPlayer], attackedPlayer))
            if numDefDice > self.countries[victim][1].values()[0] or numDefDice < 1 or numDefDice > 2:
                moveDone = False
                print "Invalid number of dice."
                continue
        
        # Count up losses
        attackerRoll = self.rollDice(numDice)
        defenderRoll = self.rollDice(numDefDice)
        print "Attacker rolled: %d"%(attackerRoll)
        print "Defender rolled: %d"%(defenderRoll)
        
        for res in [x[0]-x[1] for x in zip(attackerRoll, defenderRoll)]:
            # Attacker Loses Armies
            if res == 0:
                self.countries[attacker][1][player] -= 1
                player.occupiedCountries[attacker] -= 1
                print "Player %d loses 1 army"%(player.playerNum)
            elif res < 0:
                self.countries[attacker][1][player] += res
                player.occupiedCountries[attacker] += res
                print "Player %d loses %d armies"%(player.playerNum, res * -1)
            # Victim loses armies
            else:
                self.countries[victim][1][attackedPlayer] -= res
                player.occupiedCountries[victim] -= res
                print "Player %d loses %d army"%(attackedPlayer, res)
                                       
            # Attack Again?
        resue = raw_input("Do you want to attack some more? Y/N")
        if resume == 'Y':
            moveDone = False

                
