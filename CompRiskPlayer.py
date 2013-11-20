class CompRiskPlayer(RiskPlayer):
    def __init__(self, player_num, player_color):
       RiskPlayer.__init__(player_num,player_color)

    def GetNewArmies(self, useCards=False):
        totalNewArmies = 0
        
        for key, value in self.continentsHeld:
            totalNewArmies += value
            
        totalNewArmies += len(self.occupiedCountries) / 3
            
        if self.cards > 6:
            totalNewArmies += self.UseCards()
        elif useCards == True:
            totalNewArmies += self.UseCards()

        return totalNewArmies

    def DoComputerMove(self,player):
        pass

    def PlaceArmies(self):
        pass

    def AttackOpponet(self):
        pass


    def Fortify(self):
        pass
