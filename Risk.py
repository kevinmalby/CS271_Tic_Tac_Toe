import random
import sys

class Risk:

    def __init__(self,country_file,num_players):
        self.countries = {}  # {"North America:([South America,],{player:number_armies})
        self.map = {} # {"North America":["Eastern United States", "Greenland"]}
        self.players = [0 for x in range(num_players)]
        with open(country_file, 'r') as input:
            line = input.readline()
            while line != "":
                if line.find(":") != -1:
                    cty = line.partition(":") # name:#_countries
                    self.map[cty[0].strip()] = []
                    for x in range(int(cty[2])):
                        line = input.readline().strip()
                        line = line.split("-")
                        edges = line[1].split(',') # country- border_1, border_2 
                        self.map[cty[0]].append(line[0].strip())
                        self.countries[line[0]] =([x.strip() for x in edges],{-1:0}) 
                line = input.readline()
                 
       # print self.map
       # print self.countries
    
    def rollDice(self, num_dice):
        temp = [random.randint(1,6) for x in range(num_dice)]
        temp.sort()
        return temp

    def Clone(self):
        pass
    
    def DoMove(self, move):
        pass
    
    def GetMoves(self, player ):
        moves = []
        # Placing Armies
        if stage == 1:
            numArmies = player.getNewArmies()
            for c in player.occupiedCountries:
                moves.append((c,1))
                moves.append((c,2))
                moves.append((c,3))
            pass
        # Attacking 
        elif stage == 2:
            pass
        # Fortifying
        else: 
            pass
    
    def DoRandomMove(self):
       pass

    def DoHumanMove(self):
        pass
    def __repr__(self):
        pass
    def CheckFullBoard(self):
        pass

    def CheckEndingConditions(self, playerJustMoved):
        pass
    
