import random
import sys
import copy
import sys, random
import globalVals
from risk_player import RiskPlayer

class Risk:

    def __init__(self,country_file,num_players):
        self.countries = {}  # {"North America:[[South America,],{player:number_armies}]}
        self.map = {} # {"North America":["Eastern United States", "Greenland"]}
        self.players = [0 for x in range(num_players)]
        self.makeMap(country_file)
        self.makeCards(card_file)

    ###########################
    # Read in the countries
    ############################
    def makeMap(self, country_file):
        self.territoryCards = {} # {"North America":"Canon"}
        self.tradeInValues = (4,6,8,10,12,15,20,25,30,35,40,45)
        self.tradeInPlaceholder = 0
        self.players = []
        self.playersMove = -1

        # Build the map and countries structures
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
                        self.countries[line[0]] =[[x.strip() for x in edges],{-1:0}] 
                line = input.readline()
        print self.map
        print "\n\n"
        print self.countries

    # Read in the cards
    def makeCards(self, card_file):
        # Build the territory cards structure
        with open(card_file, 'r') as input:
            line = input.readline()
            while line != "":
                countrySymbol = line.split('-')
                countrySymbol[1] = countrySymbol[1].strip()
                self.territoryCards[countrySymbol[0]] = countrySymbol[1]
                line = input.readline()
            self.territoryCards['Wild1'] = 'wild'
            self.territoryCards['Wild2'] = 'wild'

                 
       # print self.map
       # print "\n\n"
       # print self.countries

    ####################################
    # Returns a sorted tuple of numbers between 1 and 6 inclusive
    # Length of tuple is num_dice
    #
    ############################
    def rollDice(self, num_dice):
        temp = [random.randint(1,6) for x in range(num_dice)]
        temp.sort()
        return temp

    #################################
    # Makes a copy of the game state
    #
    # Returns countries_copy
    #
    ###############################
    def Clone(self):
       return copy.deepcopy(self.countries)
    
    # Function to do move, don't currently remember what it's doing
    def DoMove(self, move, player, phase):
        for country, armies in move:
            updatePlayer = armies[0]
            self.countries[country][1][updatePlayer] += armies[1]

            if self.countries[country][1][updatePlayer] == 0:
                removePlayer = self.countries[country][updatePlayer]
                del removePlayer[removePlayer.keys()[1]]
                del player.occupiedCountries[country]


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
                        moves.extend({c:(cto,x)} for x in range(1,self.countries[c][1][player.Num]))
        return moves
    
    # Function to print state
    def __repr__(self):
        gameState = ''
        for continent in self.map:
            gameState += '\n' + continent + '\n'

            for country in self.map[continent]:

                curCountry = self.countries[country]
                playerArmies = curCountry[1]
                gameState += country + ': [ ' + str(playerArmies) + ' ]\n'

        return gameState
        
    def DoRandomMove(self):
       pass

    def DoHumanMove(self):
        pass
            
    def CheckFullBoard(self):
        pass

    def CheckEndingConditions(self, playerJustMoved):
        pass


    def setContinentControl(self):

        for player in self.players:

            # Reset the contents of the continentsHeld dictionary
            player.continentsHeld = {}

            # Check if player controls each of the continents
            continentCount = {'North America':0, 'South America':0, 'Europe':0, 'Australia':0, 'Asia':0, 'Africa':0}

            for country in player.occupiedCountries:
                
                for continent in self.map:
                    if country in continent:
                        continentCount[continent] += 1

            if continentCount['North America'] == 9:
                player.continentsHeld['NA'] = 5

            if continentCount['Europe'] == 7:
                player.continentsHeld['EU'] = 5

            if continentCount['Australia'] == 4:
                player.continentsHeld['AU'] = 2

            if continentCount['South America'] == 4:
                player.continentsHeld['SA'] = 2

            if continentCount['Asia'] == 12:
                player.continentsHeld['AS'] = 7

            if continentCount['Africa'] == 6:
                player.continentsHeld['AF'] = 3

    def randomizeInitialState(self):
        armiesToPlaceEach = 40-((globalVals.maxPlayers-2)*5)

        self.players.append(RiskPlayer(0, 'Red'))
        self.players.append(RiskPlayer(1, 'Blue'))


        numEmptyCountries = len(self.countries)
        while armiesToPlaceEach > 0:

            for i in range(globalVals.maxPlayers):

                if numEmptyCountries > 0:
                    while True:
                        country = random.choice(self.countries.keys())

                        if self.countries[country][1][0] == -1:
                            self.countries[country][1][0] = self.players[i].playerNum
                            self.countries[country][1][1]  = 1
                            self.players[i].occupiedCountries[country] = 1
                            numEmptyCountries -= 1
                            break

                else:
                    country = random.choice(self.players[i].occupiedCountries.keys())
                    self.countries[country][1][1] += 1
                    self.players[i].occupiedCountries[country] += 1

            armiesToPlaceEach -= 1

