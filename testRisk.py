import Risk as r
from risk_player import RiskPlayer
import pdb
from unittest import TestCase as tc
import globalVals
import random

def rollDiceWin(x):
    if x == 3:
        return [6,6,6]
    if x == 2:
        return [1,1]
    if x == 1:
        return [1]

def rollDiceLose(x):
    if x == 2:
        return [6,6]
    if x == 3:
        return [1,1,1]

def rollDiceTie(x):
    if x == 3:
        return [3,3,3]
    if x == 2:
        return [3,3]

class Test:
    def setup(self):
        self.game = r.Risk("countries.txt", "territory_cards.txt", 2)
        self.game.players.extend([RiskPlayer(0,globalVals.blue), RiskPlayer(1,globalVals.red)])
        self.game.players[0].occupiedCountries = {"Argentina": 10, "Brazil":15, "Peru":20,"Venezuela":5}
        self.game.players[1].occupiedCountries = {"Congo":25,"Alaska": 1, "Greenland": 16, "Central America":8, "Eastern United States":2, "North Africa":7}
        for p in self.game.players:
            for c in p.occupiedCountries:
                self.game.countries[c][1].clear()
                self.game.countries[c][1][p.playerNum] = p.occupiedCountries[c]
        

    def test_DoMove(self):
        ## Placement Tests
        print "Phase One DoMove Tests"
        self.setup()
        p_1 = self.game.players[0]
        p_2 = self.game.players[1]
        p_1.numArmiesPlacing = 25
        p_2.numArmiesPlacing = 25
        len_p2_countries = len(p_2.occupiedCountries)
        move = {"Madagascar":("Madagascar",10)}
        self.game.DoMove(move, p_2)
        if len(p_2.occupiedCountries) != len_p2_countries +1:
            'Fail Place Test: Player didnt gain country'
        if not("Madagascar" in p_2.occupiedCountries):
            "Fail Place Test: Country not in player's list"
        if(10 != self.game.players[p_2.playerNum].occupiedCountries["Madagascar"]):
            'Fail Place Test: Country didnt get the right number of armies'
        if 10 != self.game.countries["Madagascar"][1][p_2.playerNum]:
            'Fail Place Test: Country didnt get the right number of armies in game.countries'
        if 2 != self.game.gamePhase:
            'Fail Place test: game phase wrong'
        print "Done Phase 1 DoMove Tests\n"
        ## Attacking Phase Tests
        print "Testing Attacking Phase"
        self.setup()
        self.game.gamePhase = 2
        p_1 = self.game.players[0]
        p_2 = self.game.players[1]
        p_1_num_countries = len(p_1.occupiedCountries)
        p_2_num_countries = len(p_2.occupiedCountries)
        
        # Attacker Wins
        self.game.rollDice = rollDiceWin
        move = {"Venezuela":("Central America", 3)}
        num_armies_Ven = p_1.occupiedCountries["Venezuela"]
        num_armies_CA = p_2.occupiedCountries["Central America"]
        self.game.rollDice = rollDiceWin
        self.game.DoMove(move,p_1)
        if len(p_1.occupiedCountries) != p_1_num_countries:
            print "Failed Attacker Wins, occCount wrong len"
        if p_1.occupiedCountries["Venezuela"] != num_armies_Ven:
            print "Failed Attacker Wins, attacker country army count wrong"
        if p_2.occupiedCountries["Central America"] != num_armies_CA -2:
            print "Failed Attacker Wins, attacker country army count wrong"
        if self.game.countries["Central America"][1][p_2.playerNum] != num_armies_CA -2:
            print "Failed Attacker Wins; game.countries not updated"
        if p_1.occupiedCountries["Venezuela"] != num_armies_Ven:
            print "Failed Attacker Wins; Player 2 modified"

        # Victim Wins
        p_1_num_countries = len(p_1.occupiedCountries)
        p_2_num_countries = len(p_2.occupiedCountries)
        move = {"Brazil":("Congo", 3)}
        num_armies_Brazil = p_1.occupiedCountries["Brazil"]
        num_armies_Congo = p_2.occupiedCountries["Congo"]
        self.game.rollDice = rollDiceLose
        self.game.DoMove(move,p_1)
        if len(p_1.occupiedCountries) != p_1_num_countries:
            print "Failed Victim Wins, occCount wrong len"
        if p_1.occupiedCountries["Brazil"] != num_armies_Brazil - 2:
            print "Failed Victim Wins, attacker country army count wrong"
        if self.game.countries["Brazil"][1][p_1.playerNum] != num_armies_Brazil - 2:
            print "Failed Victim Wins; game.countries not updated"
        if p_2.occupiedCountries["Congo"] != num_armies_Congo:
            print "Failed Victim Wins; Player 2 modified"
            
        # Draw = Victim Wins
        p_1_num_countries = len(p_1.occupiedCountries)
        p_2_num_countries = len(p_2.occupiedCountries)
        num_in_Brazil = p_1.occupiedCountries["Brazil"]
        num_in_Congo = p_2.occupiedCountries["Congo"]
        move = {"Brazil":("Congo", 3)}
        self.game.rollDice = rollDiceTie
        self.game.DoMove(move,p_1)
        if len(p_1.occupiedCountries) != p_1_num_countries:
            print "Failed Draw , occCount wrong len"
        if p_1.occupiedCountries["Brazil"] != num_in_Brazil - 2:
            print "Failed Draw, attacker country army count wrong"
        if self.game.countries["Brazil"][1][p_1.playerNum] != num_in_Brazil - 2:
            print "Failed Draw; game.countries not updated"
        if p_2.occupiedCountries["Congo"] != num_in_Congo:
            print "Failed Draw ; Player 2 modified"

        # Win results in country ownership change
        self.setup()
        self.game.gamePhase = 2
        p_1 = self.game.players[0]
        p_2 = self.game.players[1]
        num_armies_in_Congo = 6
        num_armies_in_Brazil = 1
        self.game.countries["Congo"][1][p_2.playerNum] = num_armies_in_Congo
        self.game.countries["Brazil"][1][p_1.playerNum] = num_armies_in_Brazil
        p_1.occupiedCountries["Brazil"] = num_armies_in_Brazil
        p_2.occupiedCountries["Congo"] = num_armies_in_Congo
       
        p_1_num_countries = len(p_1.occupiedCountries)
        p_2_num_countries = len(p_2.occupiedCountries)
        num_in_Brazil = p_1.occupiedCountries["Brazil"]
        num_in_Congo = p_2.occupiedCountries["Congo"]

        move = {"Congo":("Brazil", 3)}
        self.game.rollDice = rollDiceWin
        self.game.DoMove(move, p_2)

        if (len(p_2.occupiedCountries) -1 ) != p_2_num_countries:
            print "Failed Ownership Change; Attacker didn't gain country"
        if len(p_1.occupiedCountries) != (p_1_num_countries-1):
            print "Failed Ownership Change; Defender didn't lose country"
        if len(p_2.cards) != 1:
            print "Failed Owndership Change; Attacker didn't get a card"
        if "Brazil" in p_1.occupiedCountries:
            print "Failed Ownership Change: Defender still has control of country"
        if not ("Brazil" in p_2.occupiedCountries):
            print "Failed Ownership Change: Attacker didn't gain control of country"
        if not (p_2.playerNum in self.game.countries["Brazil"][1].keys()): 
            print "Failed Ownership Change: game.countries not updated"
        if (p_2.occupiedCountries["Brazil"] != 3) or (self.game.countries["Brazil"][1][p_2.playerNum] != 3): 
            print "Failed Ownership Change: num armies in defender country not updated"
        if (p_2.occupiedCountries["Congo"] != (num_armies_in_Congo -3)) or (self.game.countries["Congo"][1][p_2.playerNum] != (num_armies_in_Congo-3)): 
            print "Failed Ownership Change: num armies in attacking country not updated"
    
        # Errors
            # Countries not adjacent

            # Countries w/ not enough armies

            # Attacking with 3+ dice
        print "Done Attack Phase Tests\n"

        ## Phase Three tests
        print "Phase Three testing"
        self.setup()
        p_1 = self.game.players[0]
        p_2 = self.game.players[1]
        self.game.gamePhase = 3
        p_1.numArmiesPlacing = 2
        num_armies = 2
        num_in_Peru = p_1.occupiedCountries["Peru"]
        num_in_Argentina = p_1.occupiedCountries["Argentina"]

        move = {"Peru":("Argentina",num_armies)}
        self.game.DoMove(move,p_1)

        if self.game.gamePhase != 1:
            print "Fail Fortifying: game phase unchanged"
        if (p_1.occupiedCountries["Peru"] != (num_in_Peru - num_armies)) or (self.game.countries["Peru"][1][p_1.playerNum] != (num_in_Peru - num_armies)):
            print "Fail Fortifying: From country didn't lose armies"
        if (p_1.occupiedCountries["Argentina"] != (num_in_Argentina + num_armies)) or (self.game.countries["Argentina"][1][p_1.playerNum] != (num_in_Argentina + num_armies)):
            print "Fail Fortifying: To country didn't gain armies"
        
            # Error
        self.game.gamePhase = 3
        #pdb.set_trace()
        if self.game.DoMove({"Greenland": ("Alaska", 4)}, p_2) != -1:
            print "Fail Fortifying: Didn't catch non-adjacent countries"
        if self.game.gamePhase != 3:
            print "Fail Fortifying: Game phase changed on error"
        if (p_1.occupiedCountries["Peru"] != (num_in_Peru - num_armies )) or (self.game.countries["Peru"][1][p_1.playerNum] != (num_in_Peru - num_armies)):
            print "Fail Fortifying: From country lost armies on error"
        if (p_1.occupiedCountries["Argentina"] != (num_in_Argentina+num_armies)) or (self.game.countries["Argentina"][1][p_1.playerNum] != (num_in_Argentina + num_armies)):
            print "Fail Fortifying: To country gained armies on error"
        
        print "Done Phase Three Testing"

    ############################################
    # Not even close to a proper set of tests  #
    # Just used it to make sure everything was #
    # working.                                 #
    ############################################
    def TestHumanMove(self):
        self.setup()
        playerOne = self.game.players[0]
        playerTwo = self.game.players[1]


        for i in range(0,6):
            newCard = random.choice(self.game.territoryCards.keys())
            playerOne.cards[newCard] = self.game.territoryCards[newCard]
            self.game.territoryCards.pop(newCard)
            
            newCard = random.choice(self.game.territoryCards.keys())
            playerTwo.cards[newCard] = self.game.territoryCards[newCard]
            self.game.territoryCards.pop(newCard)
            

        print '\n\nPlayer One Cards:'
        print playerOne.cards

        print '\n\nPlayer Two Cards:'
        print playerTwo.cards

        # Test getting the right amount of new armies
        print 'New armies for player one: ' + str(playerOne.GetNewArmies(self.game))

        self.game.DrawMap()

        playerOne.numArmiesPlacing = 25
        playerTwo.numArmiesPlacing = 25
        move = self.game.DoHumanMove(playerOne)
        print move
        print ''
        self.game.DoMove(move, playerOne)
        print self.game
        print playerOne.occupiedCountries
        print playerTwo.occupiedCountries
        self.game.gamePhase = 2
        print self.game.DoHumanMove(playerOne)
        self.game.gamePhase = 3
        print self.game.DoHumanMove(playerOne)
        self.game.DrawMap()

        print self.game.CheckWinAndScore(self.game.playersMove)

        for country, content in self.game.countries.iteritems():
            content[1] = {1:3}

        print self.game.CheckWinAndScore(self.game.playersMove)
        

def main():
    Test().test_DoMove()
    Test().TestHumanMove()


if __name__ == "__main__":
    main()



