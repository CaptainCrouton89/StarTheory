# items.py

'''
Energy builds up each turn. Rate of energy growth can be upgraded as well. Using stuff requires energy.
Most things also have cooldowns, though these can be lowered. Each turn is 10 ticks go by, and each item have cooldowns ranging from 10-100 ticks.
Each item has a cool down listed next to it saying how many ticks it has left before it can be used again. This can also be upgraded. 
Turns are taken simultaneously. Faster speeds mean your attack happens first. You can use all your energy each turn, it regenerates at set speed.
Can get batteries to save up left over. Choose a number of attacks up to amount of energy you have available. 
Tweaks can be installed on modules to lower cool downs, change energy costs, or increase potency (damage/effectiveness).
You have 4 defense stats, health stat, and an energy stat
the 4 defense stats slowly regenerate due to crew repairs, though you can prioritize one over the others (determined by how many crew you have)
When enemies reach 10%(maybe 15%?) hp, the ship surrenders (space ships are expensive, and new ones are even more so). 
You can choose to take all their cargo and ransom crew, or blow it up (in which case you can't take anything from them). Can't take actual credits, in da bank.
However, you may surrender any time you want, in which case they take all your cargo. However, if you drop to 0 HP, your ship blows up. 
You and your crew escape in your escape pod, where you are picked up by the enemy and ransomed back to your faction. You lose honor/reknown, get your ship back,
but go into large debt to your faction. If it gets too high, you are outlawed from landing on that faction's planets.

Crews are TWEAKS!!! Different crew give different bonuses to different modules, and not all were created equal. Some better at repairs,
others better at efficieny, potency, or cooldowns. 


Weapons require certain cool down, also must be manned, and have energy? Too many. Cool down will go down only if manned? You have 10 
energy, max of 15, gain 5 each turn. Lets say that basic weapon uses 7, one turn cooldown, so you could do nothing now and attack with it 
twice next turn? No because has cool down, max rate is once per turn. Idea: Most defenses regenerate quite quickly, so you want to stack 
things in a row to deal more damage? But then you get same sequence of things done over and over—attack with weapons 1, 2, then attack with
weapon 4 and 3 next turn. Then wait one turn for everything to max out, then repeat. Unless different stats regain at different speeds? Maybe
Regenerate not fixed amount, but a percentage, like 20% of it's max, which means targetting high level of one defense is gonna be really hard
so it discourages that. Could also be under user control? like, could direct crew to different stats? WOuld start as automatic, all get auto 
regenerated, with lowest one being priority, but that could be overridden by user if they wanted to. New Idea: Each crew member contributes 
exactly 2% to that defense's regen rate, meaning more crew means more regen? Or instead, each member contributes 20 points of regeneration 
per turn, so that max crews aren't OP. If you start with crew of one, ideally, then you can regenerate 20% of one stat per turn, solid. 


"defenses on board your ship are composed of a multitude of things, including hull armor, insulations, energy shields, and reflection panels. 
You have a variety of different types of defenses that are represeneted. The types of defenses each correspond to a type of damage, 
and are particularly strong against that type of defense. However, these stats can be changed by damage from weapons, often times not of the type 
that they are specifically strong against"


Speed makes it take more turns to fire. Can avert power to defense that needs regen. Lets you sync attacks. Can avert some ene
'''
import random
import time
import inspect
import math
from .effects import *
from customFormat import *
'''
class ItemContainer(object):

    def __init__(self, item, planet):
        self.item = item
        self.planet = planet

        self.shortage = False
        self.demandCount =  0 #random.uniform(0, 20)

        # Prices
        self.basePrice = item.getPrice()
        self.currentPrice = item.getPrice()

        # Quantity
        self.baseQuantity = None
        self.currentQuantity = None

        self.setBaseValues()

        self.currentQuantity = self.baseQuantity
        self.currentPrice = self.basePrice

    def setBaseValues(self):
        resourceMod = self.resourceModifier()
        proximityMod = self.proximityModifier()

        self.baseQuantity = max(int(self.item.quantity * (.5 + self.planet.wealthScore) * resourceMod *
            (.2 + 2 * self.planet.populationScore) * (1/proximityMod)), 1)

        self.basePrice = int(self.item.price * (.5 + self.planet.wealthScore)
            * resourceMod * proximityMod)

    def resourceModifier(self):
        # percentage of that item necessary for this item.
        mod = 1
        for resource in self.item.resourceInputs.keys():
            multiplier = self.item.resourceCost(resource)
            if self.planet.getResource(resource).abundance > 0:
                mod -= multiplier * self.planet.getResource(resource).abundance
            else:
                mod += multiplier
        return mod

    def proximityModifier(self):
        mod = 1
        for planet in self.planet.system.planetList:
            for container in planet.inventoryData:
                if container.item.__class__ == self.item.__class__:
                    mod *= .9
                else:
                    mod *= 1.1
        return mod

    def update(self):
        if self.shortage:
            print("shortage:", self.shortage)
            priceDecreaseChance = 0
            quantityIncreaseChance = 0
            self.shortage -= self.planet.timeRandom() * 10
            if self.shortage < 0:
                self.shortage = False
                print(f"{self.item} shortage over!")
                self.demandCount = 0
        else:
            if self.currentQuantity < self.baseQuantity:
                self.demandCount += self.planet.timeRandom() * 10
                print(f"Demand count: {self.demandCount} increased.")
            if (self.demandCount / 20) > random.random():
                self.shortage = 1
                print(f"{self.item} entering Shortage")
            priceDecreaseChance = self.currentQuantity / (2 * self.baseQuantity)
            quantityIncreaseChance = self.currentPrice / (2 * self.basePrice)

        priceChange = max(int(self.planet.timeRandom(lower=.02) * self.basePrice), 1)
        quantityChange = max(int(self.planet.timeRandom(lower=.02) * self.baseQuantity), 1)

        print(f"{self.item}: priceDecreaseChance = {priceDecreaseChance}, quantityIncreaseChance = {quantityIncreaseChance}, \
              priceChange={priceChange}, quantityChange={quantityChange}, demand={self.demandCount}")

        pMod = 1

        if priceDecreaseChance < random.random():
            self.currentPrice += priceChange
            if self.currentPrice > (self.basePrice * 3):
                self.currentPrice = self.basePrice * 3
        else:
            if priceDecreaseChance > 1:
                pMod = priceDecreaseChance * 1.5
            self.currentPrice -= int(priceChange * pMod)
            if self.currentPrice < (self.basePrice / 3):
                self.currentPrice = int(self.basePrice / 3)

        qMod = 1

        if quantityIncreaseChance > random.random():
            if quantityIncreaseChance > 1:
                qMod = quantityIncreaseChance * 1.5
            self.currentQuantity += int(quantityChange * qMod)
            if self.currentQuantity > (self.baseQuantity * 3):
                self.currentQuantity = self.baseQuantity * 3
        else:
            self.currentQuantity -= quantityChange
            if self.currentQuantity < 0:
                self.currentQuantity = 0
'''

class ItemMeta(type):
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        # Do effects on creation
        instance.setStats()
        return instance


class Item(metaclass=ItemMeta):

    def __init__(self):
        self.name = self.__class__.__name__
        self.description = "Item description"
        self.type = "item"
        self.active = True
        self.effects = []

        # Reward Stats [removable?]
        self.levelDependent = False
        self.rewardQuantity = 1
        self.tier = 1

        # Shop Stats
        self.skillScore = .1
        self.wealthScore = .1
        self.price = 5
        self.quantity = 5

        # more shop stats
        self.legal = True
        self.basic = False
        self.resourceInputs = {}

    def __str__(self):
        return f'{self.name}'

    def getPrice(self, consumer):
        return self.price

    def addEffect(self, player):
        for effect in self.effects:
            effect.addEffect(player)

    def removeEffect(self, player):
        for effect in self.effects:
            effect.removeEffect(player)

    def actionEffect(self, player):
        for effect in self.effects:
            effect.actionEffect(player)

    def autoEffect(self, player):
        for effect in self.effects:
            effect.autoEffect(player)

    def resetEffect(self):
        for effect in self.effects:
            effect.resetEffect()

    def addResourceCost(self, resourceDict):
        for key, value in resourceDict.items():
            if key in self.resourceInputs.keys():
                self.resourceInputs[key] += value
            else:
                self.resourceInputs[key] = value
        self.equalizeInputs()

    def resourceCost(self, resource):
        try:
            return self.resourceInputs[resource]
        except:
            return 0

    def equalizeInputs(self):
        totalInputs = 0
        for key, value in self.resourceInputs.items():
            totalInputs += value
        if totalInputs != 0:
            for key in self.resourceInputs.keys():
                self.resourceInputs[key] = self.resourceInputs[key] / totalInputs

    def setStats(self):
        #self.skillScore = min(self.skillScore * sqrt(self.len(self.resourceInputs.keys())), 1)
        try:
            self.wealthScore = min(max((1 - (2 / math.log10(self.price))), 0), 1)
        except:
            raise Exception(f"{self} must have a price greater than 1.")
        self.equalizeInputs()

# ITEM TYPES —————————————————————————————————————————————————————————————————————————————————————

class Tweak(Item):

    def __init__(self):
        super().__init__()
        self.type = "tweak"
        self.name = ""
        self.description = "Empty tweak description"
        self.effects = [TweakItemEffect(self)]
        self.levelDependent = True
        self.rewardQuantity = 0
        self.cooldownBonus = 0
        self.energyCostBonus = 0
        self.speedBonus = 0
        self.potency = 0
        self.penetration = 0


class Officer(Item):

    def __init__(self, 
                 name="Fred", 
                 description="A good man, following a good cause.",
                 cooldown=1, 
                 potency=0,
                 specialty="random", 
                 level="random"
                 ):
        super().__init__()
        self.type = "officer"
        self.name = name
        self.description = description
        self.effects = [OfficerEffect(self)]
        self.cooldown = cooldown
        self.potency = potency
        if specialty == "random":
            self.specialty = random.choice(["evasion", "hull", "reflectors", "shield"])
        else:
            self.specialty = specialty
        if level == "random":
            self.level = random.randint(1, 3)
        else:
            self.level = level
        self.ticks = 4 + self.level


# MODULES TYPES —————————————————————————————————————————————————————————————————————————————————————



# SHIP TYPES —————————————————————————————————————————————————————————————————————————————————————
'''

class PlayerShip(Ship):

    def __init__(self):
        super().__init__()
        self.name = "Nightingale" # Bluebird? Sparrow? Raven/crow? Nightengale is the name of the game. Father's ship. 
        self.ftl = False
        self.stl = False
        self.atm = True


class MilitaryShip(Ship):

    def __init__(self):
        super().__init__()
        self.name = "Military Ship"
        self.description = "This is a military Ship"
        self.tier = 10
        self.ftl = True
        self.stl = True
        self.atm = False


# SHIPS —————————————————————————————————————————————————————————————————————————————————————

class GalacticBattleShip(MilitaryShip):
   
    def __init__(self):
        super().__init__()
        self.name = "Battle Ship"
        self.description = "No description"
        self.tier = (99, 100)


class BattleShip(MilitaryShip):

    def __init__(self):
        super().__init__()
        self.name = "Battle Ship"
        self.description = "No description"
        self.tier = (85, 99)


class BattleCruiser(MilitaryShip):

    def __init__(self):
        super().__init__()
        self.name = "Battle Cruiser"
        self.description = "No description"
        self.tier = (80, 85)


class FleetCarrier(MilitaryShip):

    def __init__(self):
        super().__init__()
        self.name = "Battle Ship"
        self.description = "No description"
        self.tier = [60, 90]


class SupportShip(Ship):

    def __init__(self):
        super().__init__()
        self.name = "Support Ship"
        self.description = "This is a support ship!"
        self.tier = 5
        self.ftl = True
        self.stl = True
        self.atm = False


class FreightShip(Ship):

    def __init__(self):
        super().__init__()
        self.name = "Support Ship"
        self.description = "This is a support ship!"
        self.tier = 5
        self.ftl = True
        self.stl = True
        self.atm = False


class Corvette(MilitaryShip):

    def __init__(self):
        super().__init__()
        self.name = "Corvette"
        self.description = "A light military ship, generally used for scouting missions"
        self.tier = 2




Relics:
- Notifies you of shortages in items around the galaxy
- Lets you find some items sometimes?
- Cool paint job: changes reputation? Some stat.

'''
