class RiskPlayer:

    def __init__(self, pn, pc):
        self.playerNum = pn
        self.playerColor = pc
        self.occupiedCountries = {} # {"country": num_armies} ????
        self.cards = {}
        self.continentsHeld = {}
        self.numArmiesPlacing = 0

    def GetNewArmies(riskState):
        totalNewArmies = 0

        for key, value in self.continentsHeld:
            totalNewArmies += value

        totalNewArmies += len(self.occupiedCountries) / 3

        if len(self.cards) > 5:
            print 'You must turn in at least 3 of your cards this round'
            totalNewArmies += self.UseCards(riskState)
        else:
            print 'Would you like to use any of your cards this round?'

            while True:
                useCards = raw_input('Please enter y or n\n')
                if useCards != 'y' and useCards != 'n':
                    print 'That is not a valid input, please try again.'
                else:
                    break

            if useCards == 'y':
                totalNewArmies += self.UseCards()

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
            cards = raw_input('Please select 3 cards you wish to use according to the \
                values in the brackets.\nPlease enter in comma separated format.\n')

            cards = cards.split(',')
            intCards = []
            for card in cards:
                intCards.append(int(card.strip()))

            if self.CheckCards(intCards) == True:
                break
            else:
                print 'Those were not valid cards.'

        # Increase the number of armies by the current value that 3 cards gets you
        # Probably want to have an array with the army values and then an index
        # that will be incremented everytime someone cashes in cards
        numNewArmies += riskState.tradeInValues[riskState.tradeInPlaceholder]
        riskState.tradeInPlaceholder += 1


        extraArmiesForOwnedCountries = []
        for card in cards:
            for key in card:

                if key in self.occupiedCountries:
                    extraArmiesForOwnedCountries.append([key,2])

                # Remove the card from the players hand because it has been used
                del self.cards[key]



        # Return the final number of armies to place
        return (numNewArmies, extraArmiesForOwnedCountries)




    def CheckCards(self, cards):

        # Check if all cards have the same symbol
        if self.cards[cards[0]] == self.cards[cards[1]] == self.cards[cards[2]]:
            return True 

        # Check if all cards are different (Will handle wild okay because it will see it as different)
        sameSymbol = False
        i = 0
        for card in cards:
            if self.cards[card] == self.cards[(i+1) % 3]:
                sameSymbol == True
            if self.cards[card] == self.cards[(i+2) % 3]:
                sameSymbol == True
            i += 1

        if sameSymbol == False:
            return True
        
        # Check if two cards are same and one is wild
        wildExists = False
        i = 0
        for card in cards:
            if self.cards[card] == 'wild':
                wildExists = True
                wildIndex = i
            i += 1
        
        nextCard = (wildIndex + 1) % 3
        nextNextCard = (wildIndex + 2) % 3
        if (wildExists == True) and (self.cards[cards[nextCard]] == self.cards[cards[nextNextCard]]):
            return True

        # The player chose cards that cannot be combined so return false
        return False
            

    def __repr__(self):
        return "Player %d: %d Countries %d Continents %d Cards\n"%(self.playerNum,len(self.occupiedCountries), len(self.continentsHeld), len(self.cards))
