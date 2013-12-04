from risk_player import RiskPlayer
import pdb
import itertools
import montecarlotree as mct

class CompRiskPlayer(RiskPlayer):

    def __init__(self, player_num, player_color):
       RiskPlayer.__init__(self, player_num, player_color)
       self.myTree = mct.MonteCarloMethod()

    def GetNewArmies(self, riskState):
        totalNewArmies = 0
        
        for item in self.continentsHeld.iteritems():
            totalNewArmies += item[1]
            
        if len(self.occupiedCountries) / 3 > 3:
            totalNewArmies += len(self.occupiedCountries) / 3
        else:
            totalNewArmies += 3
        totalNewArmies += self.UseCards(riskState)

        return totalNewArmies


    def UseCards(self, riskState):
        if len(self.cards) < 3:
            return 0

        numNewArmies = 0
        # Choose 3 cards that work for trading in,
        # try and choose ones that have countries the computer
        # 
        # collect all possible working combinations of cards
        iterCombinations = itertools.combinations(self.cards, 3)
        allCombinations = []
        validIndeces = []

        for combination in iterCombinations:
            allCombinations.append(combination)

        for possibility in allCombinations:
            cards = [self.cards[possibility[0]], self.cards[possibility[1]], self.cards[possibility[2]]]
            if self.CheckCards(cards):
                validIndeces.append(possibility)

        if not validIndeces:
            return 0

        maxOwnedCountries = 0
        bestCards = validIndeces[0]
        for option in validIndeces:
            numCountries = 0
            for card in option:
                if card in self.occupiedCountries:
                    numCountries += 1
            if numCountries > maxOwnedCountries:
                bestCards = option
                maxOwnedCountries = numCountries


        # Increase the number of armies by the current value that 3 cards gets you
        # Probably want to have an array with the army values and then an index
        # that will be incremented everytime someone cashes in cards
        numNewArmies += riskState.tradeInValues[riskState.tradeInPlaceholder]
        riskState.tradeInPlaceholder += 1

        for country in bestCards:

            if country in self.occupiedCountries:
                curCountry = riskState.countries[country]
                curCountry[1][self.playerNum] += 2
                self.occupiedCountries[country] += 2

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

    # #################
    # Use the MCST to pick a good move
    #
    #
    ######################
    def MakeMove(self, riskstate):
        #pdb.set_trace()
        move = self.myTree.TreeSearch(riskstate,100,False)
        return move
