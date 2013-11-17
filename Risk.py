import random
import sys
import globalVals

class Risk:

    def __init__(self,country_file,num_players):
        self.countries = {}
        self.map = {}
        self.players = [0 for x in range(num_players)]
        with open(country_file, 'r') as input:
            line = input.readline()
            print "first line: %s"%(line)
            while line != "":
                if line.find(":") != -1:
                    cty = line.partition(":") # name:#_countries
                    self.map[cty[0].strip()] = []
                    for x in range(int(cty[2])):
                        line = input.readline().strip()
                        line = line.split("-")
                        edges = line[1].split(',') # country- border_1, border_2 
                        self.map[cty[0]].append(line[0].strip())
                        self.countries[line[0]] =([x.strip() for x in edges],{-1:0})  # {"America:([S_america,],{player:number_armies})
                line = input.readline()
                   
    
    def rollDice(self, num_dice):
        temp = [random.randint(1,6) for x in range(num_dice)]
        temp.sort()
        return temp

    def Clone(self):
        pass
    
    def DoMove(self, move):
        pass
    
    def GetMoves(self):
        # Pick where to put armies
        # Pick a country to attack from/to
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
    
