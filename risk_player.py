class RiskPlayer:

    def __init__(self, pn, pc):
        self.playerNum = pn
        self.playerColor = pc
        self.occupiedCountries = {}
        self.cards = {}
        self.continentsHeld = {}

    def GetNewArmies():
        totalNewArmies = 0

        for key, value in self.continentsHeld:
            totalNewArmies += value

        totalNewArmies += len(self.occupiedCountries) / 3

        if self.cards > 6:
            print 'You must turn in at least 3 of your cards this round'
            totalNewArmies += self.UseCards()
        else:
            print 'Would you like to use any of your cards this round?'

            while True:
                useCards = raw_input('Please enter y or n\n')
                if useCards != 'y' and useCards != 'n':
                    print 'That is not a correct input, please try again.'
                else:
                    break

            if useCards == 'y':
                totalNewArmies += self.UseCards()

        return totalNewArmies

    def UseCards(self):
        print 'You currently have the following cards:'

        for key, value in self.cards:
            

