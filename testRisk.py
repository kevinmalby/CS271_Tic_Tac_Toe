import Risk as r
from risk_player import RiskPlayer
import pdb

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
        self.game.players.extend([RiskPlayer(0,"blue"), RiskPlayer(1,"red")])
        self.game.players[0].occupiedCountries = {"Argentina": 10, "Brazil":15, "Peru":20,"Venezuela":5}
        self.game.players[1].occupiedCountries = {"Congo":25,"Alaska": 1, "Greenland": 16, "Central America":8, "Eastern United States":2}
        for p in self.game.players:
            for c in p.occupiedCountries:
                self.game.countries[c][1].clear()
                self.game.countries[c][1][p.playerNum] = p.occupiedCountries[c]
# {"Congo":{2:25},"Argentina": {1:10}, "Brazil":{1:15}, "Peru":{1:20},"Venezuela":{1:5},"Alaska":{2: 1}, "Greenland":{2: 16}, "Quebec":{2:8}, "Eastern United States":{2:2}})
        


    def test_DoMove(self):
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
        print "Done test_DoMove\n"

def main():
    Test().test_DoMove()


if "__name__" == "main":
    main()



