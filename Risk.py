import random
import sys
import copy
import sys, random
import globalVals
from risk_player import RiskPlayer
import pdb

class Risk:

    def __init__(self,country_file,card_file,num_players):
        self.countries = {}  # {"North America:[[South America,],{player:number_armies}]}
        self.map = {} # {"North America":["Eastern United States", "Greenland"]}
        self.players = []
        self.playersMove = -1
        self.territoryCards = {} # {"North America":"Canon"}
        self.tradeInValues = (4,6,8,10,12,15,20,25,30,35,40,45)
        self.tradeInPlaceholder = 0
        self.gamePhase = 1
        if country_file != "":
            self.makeMap(country_file)
        if card_file != "":
            self.makeCards(card_file)
      
    ###########################
    # Read in the countries
    ############################
    def makeMap(self, country_file):
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
        new_board = Risk("","",len(players))
        new_board.countries = copy.deepcopy(self.countries)
        new_board.players = copy.deepcopy(self.players)
        new_board.map = self.map 
        new_board.playersMove = self.playersMove
        new_board.territoryCards = copy.deepcopy(self.territoryCards)
        new_board.tradeInPlaceholder = self.tradeInPlaceholder
        new_board.gamePhase = self.gamePhase
        return new_board
    
    # Updates the game state with the move
    # params: move : {from_country: (to_country, num_armies)}
    #         player: player OBJECT doing the move
    #         phase: which phase of the move (1,2,3)
    #
    def DoMove(self, move, player):
        from_country = move.keys()[0]
        to_country = move[from_country][0]
        num_armies = move[from_country][1]

        c_info = self.countries[from_country][1] # {pl_#: #_armies}
        defendingPlayer = self.countries[to_country][1].keys()[0]

        # Phase 1 - Place armies on country
        if self.gamePhase == 1 and player.numArmiesPlacing > num_armies:
            if c_info.has_key(player.playerNum):
                c_info[player.playerNum] += num_armies
                player.occupiedCountries[to_country] += num_armies
                player.numArmiesPlacing -= num_armies
                if player.numArmiesPlacing == 0:
                    self.gamePhase = 2
            elif c_info.has_key(-1):
                c_info.clear()
                c_info[player.playerNum] = num_armies
                player.numArmiesPlacing -= num_armies
                player.occupiedCountries[to_country] = num_armies
                if player.numArmiesPlacing == 0:
                    self.gamePhase = 2
            else:
                print "Phase One invalid move."
                return -1
            
        # Phase 2 - Attack from country; countries lose armies
        elif self.gamePhase == 2:
            if num_armies == -1:
                #flag to stop attacking
                self.gamePhase = 3
                return
            if num_armies <= (c_info[player.playerNum] - 2):
                attack_dice = self.rollDice(num_armies)

                if self.countries[to_country][1][defendingPlayer] > 1: 
                    defend_dice = self.rollDice(2)
                else:
                    defend_dice = self.rollDice(1)
                 
                for res in [x[0]-x[1] for x in zip(attack_dice, defend_dice)]:
                    # Attacker Loses Armies
                    if res == 0 or res < 0:
                        c_info[player.playerNum] -= 1
                        player.occupiedCountries[from_country] -= 1
                    # Victim loses armies
                    else:
                       # pdb.set_trace()
                        fromc_info = self.countries[to_country][1] 
                        fromc_info[defendingPlayer] -= 1
                        self.players[defendingPlayer].occupiedCountries[to_country] -= 1
                    #country conquered
                        if fromc_info[defendingPlayer] == 0:
                            self.countries[to_country][1].clear()
                            self.countries[to_country][1][player.playerNum] = num_armies # change ownership of country
                            player.occupiedCountries[to_country] = num_armies 
                            player.occupiedCountries[from_country] -= num_armies
                            self.countries[from_country][1][player.playerNum] -= num_armies
                            self.players[defendingPlayer].occupiedCountries.pop(to_country) # def player doesn't have country anymore 
                            new_card = self.territoryCards.popitem()
                            player.cards[new_card[0]] = new_card[1] # get a card
            else:
                print "Phase Two invalid move."
                return -1
            # change game phase if attacker can't attack anymore
            if c_info[player.playerNum] < 2:
                self.gamePhase = 3
        # Phase 3 - Fortify; countries add/lose armies
        elif self.gamePhase == 3:
            #pdb.set_trace()
            if c_info[player.playerNum] -1 > num_armies and to_country in self.countries[from_country][0] and to_country in player.occupiedCountries.keys():
                c_info[player.playerNum] -= num_armies
                player.occupiedCountries[from_country] -= num_armies
                self.countries[to_country][1][player.playerNum] += num_armies
                player.occupiedCountries[to_country] += num_armies
                self.gamePhase = 1
                self.playersMove = (player.playerNum + 1) % globalVals.maxPlayers
            else:
                print "Phase Three invalid move"
                return -1
                # error message
        return

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
                moves.append({c:(c,-1)}) # flag for stopping an attack

        # Fortifying
        else:
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

