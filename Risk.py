import random
import sys

class Risk:

    def __init__(self,country_file,num_players):
        self.countries = {}  # {"North America:([South America,],{player:number_armies})
        self.map = {} # {"North America":["Eastern United States", "Greenland"]}
        self.players = [0 for x in range(num_players)]
        self.makeMap(country_file)

    ###########################
    # Read in the countries
    ############################
    def makeMap(self, country_file):
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
                 
        print self.map
        print "\n\n"
        print self.countries

    def rollDice(self, num_dice):
        temp = [random.randint(1,6) for x in range(num_dice)]
        temp.sort()
        return temp

    def Clone(self):
        
        pass
    
    def DoMove(self, move):
        pass
    
    ###############################################
    # Returns a list of possible moves based on the state passed in
    # Params:  stage   What stage of the move to get moves for
    #                     1 == placing armies, 2 == attacking, 3 == fortifying
    #
    # 
    # Return [{from_country:(to_country, num_armies)},{from_country:(to_country, num_armies)}]
    #          each dictionary is a possible move
    #        
    ###############################################
    def GetMoves(self, player, stage, num_armies=0):
        moves = []
        # Placing Armies
        if stage == 1:
            for c in player.occupiedCountries:
                moves.extend({c:(c,x)} for x in range(1,num_armies + 1 -15,5))  # can put in groups of 5 if num_armies > 15
                moves.extend({c:(c,x)} for x in range(1,16) if x <= num_armies)       # place in groups of 1 if num_armies < 15
                              
        # Attacking 
        elif stage == 2:
            for c in player.occupiedCountries:
                moves.extend({c:(ct,x)} for ct in self.countries[c][0]for x in range(1,4) if x <= self.countries[c][1][player.playerNum]-1)  # can attack from all occupied countries with at least 2 armies on it
        # Fortifying
        else: 
            ### TODO:: Fortify only adjacent countries or countries connected by path too?
            for c in player.occupiedCountries:
                for cto in self.countries[c][0]:
                    if cto in player.occupiedCountries:
                        moves.extend({c:(cto,x)} for x in range(1,self.countries[c][1][player.Num])
        return moves
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
    
