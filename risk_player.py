class RiskPlayer:

    def __init__(self, pn, pc):
        self.playerNum = pn
        self.playerColor = pc
        self.occupiedCountries = {} # {"country": num_armies}
        self.cards = {}
        self.continentsHeld = {}
        self.numArmiesPlacing = 0
        self.conqueredTerritory = False
        self.numAttacks = 0
        self.maxArmiesLeft = 200
        self.minCountry = ''
        self.maxCountry = ''
        self.startArmies = 0
        self.startCountries = 0

    def GetNewArmies(self, riskState):
        totalNewArmies = 0

        for key, value in self.continentsHeld.iteritems():
            totalNewArmies += value

        if (len(self.occupiedCountries) / 3) > 3:
            totalNewArmies += len(self.occupiedCountries) / 3
        else:
            totalNewArmies += 3

        if len(self.cards) > 5:
            print 'You must turn in at least 3 of your cards this round'
            totalNewArmies = self.UseCards(riskState)
            return totalNewArmies
        elif len(self.cards) < 3:
            print 'You currently have less than 3 cards, you will not be able to cash them in.'
        else:
            print 'Would you like to use any of your cards this round?'

            while True:
                useCards = raw_input('Please enter y or n\n')
                if useCards != 'y' and useCards != 'n':
                    print 'That is not a valid input, please try again.'
                else:
                    break

            if useCards == 'y':
                totalNewArmies += self.UseCards(riskState)

        return totalNewArmies

    def UseCards(self, riskState):

        numNewArmies = 0

        print 'You currently have the following cards:\n'
        cardStr = ""
        for key in self.cards:
            cardStr += '|  ' + key.ljust(10) + '  |' + '  '
        cardStr += '\n'
        for key, value in self.cards.iteritems():
            cardStr += '|  ' + value.ljust(10) + '  |' + '  '
        cardStr += '\n'
        for i in range(len(self.cards)):
            cardStr += '|  [' + str(i) + ']'.ljust(10) + '|' + '  '
        cardStr += '\n'
        print cardStr


        while True:
            cards = raw_input('Please select 3 cards you wish to use according to the values in the brackets.\nPlease enter in comma separated format.\n')

            cards = cards.split(',')
            intCards = []
            for card in cards:
                intCards.append(int(card.strip()))

            count = 0
            cardChoiceVals = []
            cardChoiceKeys = []
            for country, value in self.cards.iteritems():
                if count in intCards:
                    cardChoiceVals.append(value)
                    cardChoiceKeys.append(country)
                count += 1

            if self.CheckCards(cardChoiceVals) == True:
                break
            else:
                print 'Those were not valid cards.'

        # Increase the number of armies by the current value that 3 cards gets you
        # Probably want to have an array with the army values and then an index
        # that will be incremented everytime someone cashes in cards
        numNewArmies += riskState.tradeInValues[riskState.tradeInPlaceholder]
        riskState.tradeInPlaceholder += 1

        for country in cardChoiceKeys:

            if country in self.occupiedCountries:
                curCountry = riskState.countries[country]
                curCountry[1][self.playerNum] += 2
                self.occupiedCountries[country] += 2
                self.maxArmiesLeft -= 2

            # Remove the card from the players hand because it has been used
            del self.cards[country]

        # Return the final number of armies to place
        return (numNewArmies)


    def CheckCards(self, cards):

        # Check if all cards have the same symbol
        if cards[0] == cards[1] == cards[2]:
            return True 

        # Check if all cards are different (Will handle wild okay because it will see it as different)
        sameSymbol = False
        i = 0
        for card in cards:
            if card == cards[(i+1) % 3]:
                sameSymbol = True
            if card == cards[(i+2) % 3]:
                sameSymbol = True
            i += 1

        if sameSymbol == False:
            return True
        
        # Check if two cards are same and one is wild
        wildExists = False
        i = 0
        for card in cards:
            if card == 'wild':
                wildExists = True
                wildIndex = i
            i += 1
        
        if wildExists == True:
            return True

        # The player chose cards that cannot be combined so return false
        return False

    def maxMinCluster(self, riskState):
        min = 1000000
        minCountry = ''
        max = 0
        maxCountry = ''
        for country, armies in self.occupiedCountries.iteritems():
            tempCount = armies
            for adjacent in riskState.countries[country][0]:
                c = riskState.countries[adjacent][1]
                if self.playerNum in c:
                    tempCount += c[c.keys()[0]]
            if tempCount < min:
                min = tempCount
                minCountry = country
            if tempCount > max:
                max = tempCount
                maxCountry = country

        self.minCountry = minCountry
        self.maxCountry = maxCountry

    def LongPrint(self):
        strRep = "Player %d: %d Countries %d Continents %d Cards\n"%(self.playerNum,len(self.occupiedCountries), len(self.continentsHeld), len(self.cards))
        strRep += '\n'
        for country, val in self.occupiedCountries.iteritems():
            strRep += '%s : %d\n' %(country, val)
        print strRep
            

    def __repr__(self):
        return "Player %d: %d Countries %d Continents %d Cards\n\t%s\n"%(self.playerNum,len(self.occupiedCountries), len(self.continentsHeld), len(self.cards),self.occupiedCountries)
