import random
import sys, pygame
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
        self.countryLocations = {}
        self.tradeInValues = (4,6,8,10,12,15,20,25,30,35,40,45)
        self.tradeInPlaceholder = 0
        self.gamePhase = 1
        if country_file != "":
            self.makeMap(country_file)
        if card_file != "":
            self.makeCards(card_file)
        self.makeCountryLocations()
        pygame.init()
      
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

    #####################
    # Read in the cards #
    #####################
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


    #######################################
    # Read in the countries' xy locations #
    #######################################
    def makeCountryLocations(self):
        # Build the territory cards structure
            with open('country_xy_locations.txt', 'r') as input:
                line = input.readline()
                while line != "":
                    countrySymbol = line.split('-')
                    xyLoc = countrySymbol[1].split(' ')
                    self.countryLocations[countrySymbol[0].strip()] = (xyLoc[1].strip(), xyLoc[2].strip())
                    line = input.readline()


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
        new_board = Risk("","",len(self.players))
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

                # Get the number of armies to place for the next player
                player.numArmiesPlacing = player.GetNewArmies(self.Clone())
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
    
    ######################################
    # Function that prints the current   #
    # state of the game, probably better #
    # to use draw map though             #
    ######################################
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

    ################################################
    # Do a move as a human, depends on the         #
    # phase of the game set by DoMove. Returns a   #
    # move in the proper format                    #
    # {countryFrom:(countryTo,numArmies)}          #
    ################################################
    # Do a move as human
    def DoHumanMove(self, player):

        # Remember to add something where we update the player that just went

        # If we are in the placement phase do the following
        if self.gamePhase == 1:

            # Execute the placement phase
            move = self.HumanPlaceArmies(player.numArmiesPlacing, player)

        # If we are in the attacking phase do the following
        if self.gamePhase == 2:

            # Execute the attack phase
           move = self.HumanAttackOpponents(player)

        # If we are in the fortifying phase do the following
        if self.gamePhase == 3:

            # Execute the fortify phase
            move = self.HumanFortify(player)

        return move

    ################################################
    # Do the human placement step, returns the     #
    # result in the proper format of               #
    # {countryFrom:(countryTo,numArmies)}          #
    # relies on DoMove to call the GetNewArmies fn #
    ################################################
    def HumanPlaceArmies(self, numNewArmies, player):
        
        print 'You currently have the shown number of armies in the corresponding countries:\n'
        for key, value in player.occupiedCountries.iteritems():
            print key + ': ' + str(value)
        print ''

        print 'You have %d armies left to place.\n' %(numNewArmies)

        errorVal = -1
        moveDone = False
        while moveDone != True:

            moveDone = True

            # Select which country in which to add armies
            if errorVal == -1 or errorVal == 0:
                countrySelect = raw_input('Please type the name of the country in which you wish to place armies: ')
                if countrySelect not in player.occupiedCountries:
                    print 'That was not the name of an actual country or you do not occupy that territory.\n'
                    moveDone = False
                    errorVal = 0
                    continue
                else:
                    errorVal = -1

            # Select the number of armies to place in that country
            if errorVal == -1 or errorVal == 1:
                armiesToPlace = raw_input('Please type the number of armies you wish to place in %s: ' %(countrySelect))
                print ''
                try:
                    armiesToPlaceNum = int(armiesToPlace)
                except:
                    moveDone = False
                    print 'That was not a number.\n'
                    errorVal = 1
                    continue

                if armiesToPlaceNum not in range(1,numNewArmies+1):
                    moveDone = False
                    errorVal = 1
                    print 'You must place at least 1 army in the country and no more than the number of armies you have left.\n'

        # Setup the dictionary to return
        # The first half contains the updated number of armies, and the second half contains the army movement dictionary
        return {countrySelect:(countrySelect, armiesToPlaceNum)}

    ###################################################
    # Do the human attacking step, returns the        #
    # result in the proper format of                  #
    # {countryFrom:(countryTo,numArmies)}             #
    # *The thing I wonder about here is whether       #
    #  it makes sense to return the number of         #
    #  armies to attack with, it is more like the     #
    #  number of dice to roll, needs further thought* #
    ###################################################
    def HumanAttackOpponents(self, player):

        print 'You currently have the shown number of armies in the corresponding countries:\n'
        for key, value in player.occupiedCountries.iteritems():
            print key + ': ' + str(value)
        print ''
        
        while True:
            endAttack = raw_input('Would you like to stop attacking and move on to fortification? Enter y for yes and n for no. ')
            if endAttack == 'y':
                return {'':('', -1)}
                break
            elif endAttack == 'n':
                break
            else:
                print 'That was not a valid input.\n'

        errorVal = -1
        moveDone = False
        while moveDone != True:
            moveDone = True

            if errorVal == -1 or errorVal == 0:
                # Select which country to attack from
                attacker = raw_input('Please type the name of the country you want to attack from: ')
                
                # Make sure that it is a valid country
                if attacker not in self.countries:
                    print '***That was not the name of an actual country.\n'
                    moveDone = False
                    errorVal = 0
                    continue
                else:
                    errorVal = -1

                if attacker not in player.occupiedCountries:
                    print '***You do not occupy that country.\n'
                    moveDone = False
                    errorVal = 0
                    continue
                else:
                    errorVal = -1

            print '%s currently borders the following countries with the following armies:\n' %(attacker)
            neighborStr = ''
            neighbors = self.countries[attacker][0]
            for country in neighbors:
                neighborStr += '%s: ' %(country)
                neighborArmies = self.countries[country][1]
                for key, value in neighborArmies.items():
                    neighborStr += str(key)
                    neighborStr += ': %s' %(str(value))
                neighborStr += '\n'
            print neighborStr

            
            if errorVal == -1 or errorVal == 1:
                # Select which country to attack 
                victim = raw_input('Please type the name of the country you want to attack: ')
               
                # Make sure that it is a valid country
                if victim not in self.countries:
                    print '***That was not the name of an actual country.\n'
                    moveDone = False
                    errorVal = 1
                    continue
                else:
                    errorVal = -1

                # Make sure they are only attacking an adjacent country
                if victim not in neighbors:
                    print '***You must attack an adjacent country.\n'
                    moveDone = False
                    errorVal = 1
                    continue
                else:
                    errorVal = -1

                # Make sure that they aren't trying to attack their own country
                ownCountry = False
                for key in player.occupiedCountries:
                    if key == victim:
                        ownCountry = True
                        break;
                if ownCountry == True:
                    moveDone = False
                    print '***You cannot attack your own country.\n'
                    errorVal = 1


        opponentArmies = self.countries[victim][1]
        opponentArmies = opponentArmies[opponentArmies.keys()[0]]
        print('\nYou currently have %d armies in your attacking country [%s], the opponent you are attacking has %d armies in their country [%s]' %(player.occupiedCountries[attacker],\
            attacker, opponentArmies, victim))

        moveDone = False
        while moveDone == False:
            moveDone = True
            attackCount = raw_input('How many armies would you like to attack with? ')
            try:
                attackCount = int(attackCount)
            except:
                print '***That was not a number.'
                moveDone = False
                continue

            if attackCount not in range(1, player.occupiedCountries[attacker]):
                print '***That number is outside the range of the number of armies in your country.'
                moveDone = False

        return {attacker:(victim, attackCount)}


    ################################################
    # Do the human fortification step, returns the #
    # result in the proper format of               #
    # {countryFrom:(countryTo,numArmies)}          #
    ################################################
    def HumanFortify(self, player):

        print 'You currently have the shown number of armies in the corresponding countries:\n'
        for key, value in player.occupiedCountries.iteritems():
            print key + ': ' + str(value)
        print ''

        errorVal = -1
        moveDone = False

        while moveDone != True:
            moveDone = True
            
            if errorVal == -1 or errorVal == 0:
                # Select which country to fortify from
                fortifyFrom = raw_input('Please type the name of the country from which you want to fortify armies: ')

                # Make sure that it is a valid country
                if fortifyFrom not in self.countries:
                    print '***That was not the name of an actual country.\n'
                    moveDone = False
                    errorVal = 0
                    continue
                else:
                    errorVal = -1
                
                if fortifyFrom not in player.occupiedCountries:
                    print '***You do not occupy that country.\n'
                    moveDone = False
                    errorVal = 0
                    continue
                else:
                    errorVal = -1

            print '%s currently borders the following countries with the following armies:\n' %(fortifyFrom)
            neighborStr = ''
            neighbors = self.countries[fortifyFrom][0]
            for country in neighbors:
                neighborStr += '%s: ' %(country)
                neighborArmies = self.countries[country][1]
                for key, value in neighborArmies.items():
                    neighborStr += str(key)
                    neighborStr += ': %s' %(str(value))
                neighborStr += '\n'
            print neighborStr


            if errorVal == -1 or errorVal == 1:
                # Select which country to fortify to
                fortifyTo = raw_input('Please type the name of the country to which you want to fortify armies: ')

                # Make sure that it is a valid country
                if fortifyTo not in self.countries:
                    print '***That was not the name of an actual country.\n'
                    moveDone = False
                    errorVal = 1
                    continue
                else:
                    errorVal = -1
                
                if fortifyTo not in player.occupiedCountries:
                    print '***You do not occupy that country.\n'
                    moveDone = False
                    errorVal = 1
                    continue
                else:
                    errorVal = -1
                
            if errorVal == -1 or errorVal == 2:
                # Make sure that the countries are adjacent
                adjacentToFortifyFrom = self.countries[fortifyFrom][0]

                matchFound = False
                for country in adjacentToFortifyFrom:
                    if fortifyTo == country:
                        matchFound = True
                        break;
                if matchFound == False:
                    print '***The chosen countries must be adjacent to each other.'
                    errorVal = 2
                    moveDone = False
                else:
                    errorVal = -1


        moveDone = False
        while moveDone == False:
            moveDone = True
            fortifyCount = raw_input('How many armies would you like to fortify? ' )
            try:
                fortifyCount = int(fortifyCount)
            except:
                print '***That was not a number'
                moveDone = False
                continue

            if fortifyCount not in range(1, player.occupiedCountries[fortifyFrom]):
                print '***That number is outside the range of the number of armies in your country.'
                moveDone = False
                continue

        return {fortifyFrom:(fortifyTo, fortifyCount)}

    ###############################################
    # Checks whether the game is over, and if     #
    # it is, then it will return 1 if the player  #
    # who just moved won, or 0.0 if the player    #
    # who just moved lost. Although I think it    #
    # will always be the case that the player who # 
    # just went is the player who won             #
    ###############################################
    def CheckWinAndScore(self, playerJustMoved):
        
        initialCountry = random.choice(self.countries.values())
        curPlayerNum = initialCountry[1].keys()[0]
        for country, content in self.countries.iteritems():
            occupiedBy = content[1].keys()[0]

            # If the game is not over, return -1
            if occupiedBy != curPlayerNum:
                return -1

            curPlayerNum = occupiedBy
        
        if curPlayerNum == playerJustMoved:
            return 1.0
        else:
            return 0.0


    #######################################
    # Function to determine in a player   #
    # has control of any continents       #
    #######################################
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

    #############################################
    # Initializes the game to random placements #
    # that depend on the number of players      #
    #############################################
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

    ############################################
    # Use the pygame library to make a shitty  #
    # representation of the current game state #
    ############################################
    def DrawMap(self):
        map = pygame.image.load('/home/kevin/Pictures/risk_map.png')
        w = 1227
        h = 628
        screen = pygame.display.set_mode((w,h))
        screen.blit(map,(0,0))

        for country, content in self.countries.iteritems():
            curArmies = content[1]
            if curArmies.keys()[0] > -1:
                color = self.players[curArmies.keys()[0]]
                armyVal = curArmies[curArmies.keys()[0]]
                self.printText(screen, str(armyVal), 'Ariel', 20, int(self.countryLocations[country][0]), int(self.countryLocations[country][1]), color.playerColor)

        pygame.display.update()    

        done = False
        while done != True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

    # Prints text to the screen using Pygame library
    def printText(self, screen, txtText, Textfont, Textsize , Textx, Texty, Textcolor):
        # pick a font you have and set its size
        myfont = pygame.font.SysFont(Textfont, Textsize)
        # apply it to text on a label
        label = myfont.render(txtText, 1, Textcolor)
        # put the label object on the screen at point Textx, Texty
        screen.blit(label, (Textx, Texty))