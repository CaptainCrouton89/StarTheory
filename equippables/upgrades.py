from .effects import *

class Upgrade(object):

    def __init__(self, exponent=.05):
        self.type = "upgrade"
        self.description = "This upgrades stuff"
        self.potency = 10
        self.quantity = None
        self.legal = True
        self.space = 0
        self.price = 1000
        self.exponent = exponent
        self.effects = []

    def getPrice(self, player):
        lvl = player.getLevel()
        price = self.price * (1 + self.exponent) ** lvl
        print("upgrade price:", price)
        return price

    def upgradeEffect(self, player):
        for effect in self.effects:
            effect.upgradeEffect(player)

    def __str__(self):
        return self.__class__.__name__


class UpgradeSpace(Upgrade):

    def __init__(self):
        super().__init__()
        self.name = "Upgrade Space"
        self.effects = [UpgradeSpaceEffect(self)]


class HullUpgrade(Upgrade):

    def __init__(self):
        super().__init__()
        self.name = "Stronger Hull"
        self.effects = [UpgradeDefenseEffect(self, "hull")]


class ShieldUpgrade(Upgrade):

    def __init__(self):
        super().__init__()
        self.name = "More powerful reactors"
        self.effects = [UpgradeDefenseEffect(self, "shield")]


class EvasionUpgrade(Upgrade):

    def __init__(self):
        super().__init__()
        self.name = "Better Engines"
        self.effects = [UpgradeDefenseEffect(self, "evasion")]


'''
Reflavor everything as a module! 
Better shield generators, many tiers?
Better engines, more maneuverable, allow FTL
Better... Hull plating?
Should only sometimes take up more space, but ideally they are just flat upgrades?
Should not be available as modules? Def. should be upgrades, don't want to wait on a new hull upgrade till you find sufficient planet with trade. Not Items,
cant be traded or treated like trade items. 
'''
