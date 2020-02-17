'''
Resource, wealth, and skill scores have to vary more than they do

if less than 30% is solid resources, then there is only a station. Big effects on planet:
    1/10 population
    boost to skill
    Can't land, their shops are severely limited:
        Close to no manufacturing
        Source of knowledge, gasses, 

'''

import log
from myFunctions import *
from customFormat import *
from equippables.items.modules import *
from equippables.items.weapons import *
from equippables.items.cargo import *
from equippables.upgrades import *
from equippables.wealth import *
import itemManipulation
import copy
import random
import numpy.lib.scimath as npMath
import numpy as np
import gamemanager as gm

initLog = log.Log("initializationLogs")

class FactionEntity(object):

    def __init__(self, name, description, galaxy):
        self.name = name
        self.description = description
        self.galaxy = galaxy
        self.systemList = []
        self.strength = .01 #percentage of the map they take each time they expand

    def setBase(self, system):
        self.base = system

    def expand(self, tiles):
        addedTiles = 0
        while addedTiles < tiles:
            randTile = random.choice(self.systemList)
            randExpansionTile = random.choice(randTile.neighbors)
            if randExpansionTile.faction == False:
                randExpansionTile.setFaction(self)
                addedTiles +=1

    #newTiles = int(self.galaxy.size * self.strength)


class PlanetEntity(object):

    def __init__(self, system, proximity, name="noname", faction=False, questList=False, cargoList=False, description=False, playerOpinion=50):
        self.name = name
        self.description = "no Name Planet"
        self.inhabited = True
        self.faction = ""
        self.questList = []
        
        self.system = system

        # Scores
        self.resourceScore = 0
        self.wealthScore = 0
        self.populationScore = 0
        self.skillScore = 0
        self.trafficScore = 0

        # Ratings
        self.playerRating = .5

        # Traits
        self.proximity = proximity
        self.resourceList = []
        self.temperature = 0
        self.solidCore = True
        self.habitable = True
        self.station = True

        # Shop
        self.inventory = itemManipulation.InventoryManager(self)
        self.credits = False
        self.space = False
        self.currentTime = 0
        self.lastTime = 0

    def __str__(self):
        return self.name

    def getResource(self, resource, abundant=False):
        for r in self.resourceList:
            if type(r) is type(resource):
                return r
        return r

    def getDescription(self):
        description = []

        # Resources description
        singleResource = False
        mostAbundant = []
        traceAmounts = []

        # Divies elements into different categories
        for resource in self.resourceList:
            if resource.abundance == 1:
                singleResource = resource
                break
            elif resource.abundance > .15:
                mostAbundant.append(resource)
            elif resource.abundance > 0:
                traceAmounts.append(resource)

        # Builds resource description
        if singleResource:
             description.append(
                "Composed entirely of {0}, ".format(singleResource.name))
        elif len(mostAbundant) == 1:
             description.append("Composed primarily of {0}, ".format(mostAbundant[0].name))
        elif len(mostAbundant) == 2:
             description.append("Composed primarily of {0} and {1}, ".format(mostAbundant[0].name, mostAbundant[1].name))
        elif len(mostAbundant) > 2:
            description.append("Composed primarily of ")
            for i in range(len(mostAbundant)-1):
                 description += mostAbundant[i].name + ", "
            description.append("and {0}, ".format(mostAbundant[-1].name))
        else:
            description.append("Composed of ")
            for i in range(len(traceAmounts)-1):
                 description.append(traceAmounts[i].name + ", ")
            description.append("and {0}, ".format(traceAmounts[-1].name))
        if traceAmounts:
            description.append("with trace amounts of ")
            if len(traceAmounts) == 1:
                description.append(traceAmounts[0].name + ", ")
            elif len(traceAmounts) == 2:
                description.append("{0} and {1}, ".format(traceAmounts[0].name, traceAmounts[1].name))
            elif len(traceAmounts) > 2:
                for i in range(len(traceAmounts)-1):
                    description.append(traceAmounts[i].name + ", ")
                description.append("and {0}, ".format(traceAmounts[-1].name))
        description.append(self.name.capitalize() + " is a ")
        
        # Other traits
        if self.temperature > 500:
            if self.solidCore:
                description.append("molten, ")
            else:
                description.append("face-meltingly-hot, ")
        elif self.temperature > 200:
            description.append("super-heated, ")
        elif self.temperature > 100:
            description.append("hot, ")
        elif self.temperature < 400:
            description.append("super-chilled, ")
        elif self.temperature < 100:
            description.append("frozen, ")
        elif self.temperature < 0:
            description.append("chilly, ")
        else:
            description.append("temperate, ")
        if not self.habitable:
            description.append("uninhabitable ")
        elif self.populationScore > .7:
            description.append("richly populated ")
        elif self.populationScore > .3:
            description.append("moderately populated ")
        else:
            description.append("lightly populated ")
        if self.solidCore:
            description.append("planet.")
        else:
            description.append("gas giant.")

        # Stitch together
        description = ''.join(description)
        return description

    def setTemperature(self):
        # Randomizes Temperature
        position, total = self.proximity
        tempRange = (-25*(total + position), 1000 - 162 * position)
        self.temperature = round(random.randint(tempRange[0], tempRange[1]), 5)

        # Melts resources, habitabliltiy ruled out
        totalSolid = 0
        if self.temperature < -300 or self.temperature > 400:
            self.habitable = False
        for resource in self.resourceList:
            if resource.solidTemp >= self.temperature:
                resource.solid = True
                totalSolid += resource.abundance        
        if totalSolid < .3:
            self.solidCore = False
            self.habitable = False
        #print("temp:", self.temperature, "Position:", self.proximity, "solid core:", self.solidCore, "habitable:", self.habitable)

    def generateResources(self, dieSize=4):
        totalAbundance = 0
        numResources = random.randint(0, dieSize) + random.randint(0, dieSize) + 1
        selection = np.random.choice(
            self.resourceList,
            numResources,
            False,
            self.system.galaxy.resourceProbabilities)
        for resource in selection:
            resource.abundance = random.uniform(0.01, (resource.rarity + .3)/1.3)
            totalAbundance += resource.abundance
        for resource in self.resourceList:
            resource.abundance = resource.abundance / totalAbundance  
        #print("break")

    def setResourceScore(self):
        for resource in self.resourceList:
            resourceScore = min(npMath.log10(resource.price) / 5, 1) * resource.abundance
            self.resourceScore += resourceScore
        self.resourceScore = max(round(self.resourceScore, 8), 0.000001)
    
    def setTrafficScore(self):
        neighborProximityScore = npMath.sqrt(len(self.system.getFactionNeighbors()) / 4)
        localNeighborProximityScore = len(self.system.planetList) / (2 * (self.system.maxPlanets))
        baseProximityScore = 1 - ((self.system.distanceFromBase) / self.system.galaxy.diagonal)
        self.trafficScore = (baseProximityScore + neighborProximityScore + localNeighborProximityScore) / 3
        self.trafficScore = max(round(self.trafficScore, 8), 0.000001)

    def setPopulationScore(self):
        self.populationScore = spread((random.random() * 2 + self.trafficScore) / 3)
        if not self.habitable:
            self.populationScore /= 10
        elif self.temperature < 30 or self.temperature > 200:
            self.populationScore /= 3
        self.populationScore = max(round(self.populationScore, 8), 0.000001)
        
    def setWealthScore(self):
        self.wealthScore = spread((self.trafficScore + self.resourceScore + random.random()) / 3)
        self.wealthScore = max(round(self.wealthScore, 8), 0.000001)

    def setSkillScore(self):
        self.skillScore = spread((self.trafficScore + spread(self.wealthScore)) / 2)
        if not self.habitable:
            self.skillScore == npMath.sqrt(self.skillScore)
        self.skillScore = max(round(self.skillScore, 8), 0.000001)

    def applyResourceEffects(self):
        for resource in self.resourceList:
            if resource.abundance > 0:
                resource.causeEffect(self)
            
    def generateShop(self):
        for item in self.system.galaxy.allItems:  # All items needs to be filled
            chances = .9 - 2 * max((item.skillScore - self.skillScore), 0) - \
                2 * max((item.wealthScore - self.wealthScore), 0)
            if item.basic or random.random() <= chances:
                self.inventory.add(item)
                self.inventory.get(item).initializeValues()

                # All basic items are available at some point, but not always available at any given moment
        for upgrade in self.system.galaxy.allUpgrades:
            self.inventory.add(upgrade)

    # In game Methods

    def add(self, item, quantity):
        self.inventory.add(item, quantity)

    def remove(self, item, quantity):
        self.inventory.remove(item, quantity)

    def getTimeDifference(self):
        self.currentTime = gm.getTime()
        d = self.currentTime - self.lastTime
        self.lastTime = self.currentTime
        return d

    def timeRandom(self, upper=1, lower=0):
        randNum = random.uniform(0, .01) * self.getTimeDifference()
        if randNum > upper:
            randNum = upper
        elif randNum < lower:
            randNum = lower
        return randNum


class SystemEntity(object):

    def __init__(self, galaxy, x, y):
        self.x = x
        self.y = y
        self.faction = False
        self.name = "noname"
        self.description = "no Description"
        self.galaxy = galaxy
        self.neighbors = []
        self.planetList = []
        self.shipList = []
        self.distanceFromBase = 10
        self.maxPlanets = 5 # Don't change this, effects temperature calculations
        self.minPlanets = 1

    def generatePlanets(self):
        numPlanets = random.randint(self.minPlanets, self.maxPlanets) + random.randint(self.minPlanets, self.maxPlanets) - self.minPlanets
        # numPlanets = random.randint(self.minPlanets, self.maxPlanets)
        for i in range(numPlanets):
            proximity = (i, numPlanets)
            planet = PlanetEntity(self, proximity)
            self.planetList.append(planet)
            self.galaxy.planetList.append(planet)

    def setFaction(self, faction, base=False):
        self.faction = faction
        faction.systemList.append(self)
        if base:
            faction.setBase(self)
        xDiff = self.x-self.faction.base.x
        yDiff = self.y-self.faction.base.y
        self.distanceFromBase = (
            npMath.sqrt(xDiff ** 2 + yDiff ** 2 + 1))

    def setNeighbors(self):

        if self.y+1 < self.galaxy.height:
            self.neighbors.append(self.galaxy.systemGrid[self.x][self.y+1])
        if self.y-1 >= 0:
            self.neighbors.append(self.galaxy.systemGrid[self.x][self.y-1])
        if self.x+1 < self.galaxy.width:
            self.neighbors.append(self.galaxy.systemGrid[self.x+1][self.y])
        if self.x-1 >= 0:
            self.neighbors.append(self.galaxy.systemGrid[self.x-1][self.y])

    def getFactionNeighbors(self):
        self.factionNeighbors = []
        for system in self.neighbors:
            if system.faction == False:
                continue
            elif system.faction == self.faction:
                self.factionNeighbors.append(system)
        return self.factionNeighbors

        # Make this return something, so that in the getResponse section it can move player or something, or it can quit if player returns quit.


class Galaxy(object):
    def __init__(self, x=5, y=5):
        self.systemGrid = []
        self.width = x
        self.height = y
        self.size = x * y
        self.diagonal = npMath.sqrt(x**2 + y**2)
        self.systemList = []
        self.planetList = []
        self.resourceList = []
        self.allItems = []
        self.allUpgrades = []
        
        for resource in get_all_subclasses(Resource):
            self.resourceList.append(resource())

        for cargo in get_all_subclasses(Cargo):
            self.allItems.append(cargo())

        for module in get_all_subclasses(Module):
            self.allItems.append(module())

        for weapon in get_all_subclasses(Weapon):
            self.allItems.append(weapon())

        for upgrade in get_all_subclasses(Upgrade):
            self.allUpgrades.append(upgrade())
        
        self.resourceProbabilities = []
        self.factionList = [
            FactionEntity("terra", "This is terra", self),
            FactionEntity("kozilex", "This is techy stuff", self),
            FactionEntity("ygnora", "Bio stuff", self)
        ]
        

    def generateSystemGrid(self):
        for column in range(self.width):
            columnList = []
            for row in range(self.height):
                s = SystemEntity(self, column, row)
                columnList.append(s)
                self.systemList.append(s)
            self.systemGrid.append(columnList)

    def buildSystems(self):
        print("Initializing galactic planetary systems...")
        for system in self.systemList:
            system.setNeighbors()
            system.generatePlanets()
        print("Systems initialization complete...")

    def addResources(self):
        totalRarity = 0
        for resource in self.resourceList:
            totalRarity += resource.rarity
        for resource in self.resourceList:
            resource.adjustedRarity = resource.rarity / totalRarity
            self.resourceProbabilities.append(resource.adjustedRarity)
        for planet in self.planetList:
            planet.resourceList = copy.deepcopy(self.resourceList)
            planet.generateResources()

    def setPlanetScores(self):
        for planet in self.planetList:
            planet.setTemperature()
            planet.setResourceScore()
            planet.setTrafficScore()
            planet.setPopulationScore()
            planet.setWealthScore()
            planet.setSkillScore()
            planet.applyResourceEffects()

    def addFactions(self):
        print("Adding factions...")
        for faction in self.factionList:
            counter = 0
            while True:
                counter += 1
                x = random.randint(0, self.width-1)
                y = random.randint(0, self.height-1)
                targetSystem = self.systemGrid[x][y]
                if targetSystem.faction == False:
                    targetSystem.setFaction(faction, base=True)
                    targetSystem.faction.expand(4)
                    break
                if counter > 50:
                    clearScreen()
                    print("\n\n")
                    printCentered("A fatal error has occurred. Press 'enter' to continue.")
                    input("\n")
                    quit()

    def generateShops(self):
        print("Generating shops...")
        for planet in self.planetList:
            planet.generateShop()

    def assignNames(self):
        print("Assigning names...")
        systemNames = open("randGenText/systemNames.txt", "r+")
        systemNamesList = systemNames.read().splitlines()
        planetNames = open("randGenText/planetNames.txt", "r+")
        planetNamesList = planetNames.read().splitlines()
        initLog.log("Number of planets:", len(self.planetList))
        initLog.log("Number of systems:", len(self.systemList))
        for i in range(len(self.systemList)):
            self.systemList[i].name = systemNamesList[i]
        for i in range(len(self.planetList)):
            self.planetList[i].name = planetNamesList[i]
        systemNames.close()
        planetNames.close()
        
    def initialize(self):
        self.generateSystemGrid()
        self.buildSystems()
        self.addResources()
        self.addFactions()
        self.setPlanetScores()
        self.generateShops()
        self.assignNames()
        #self.printPlanetStat("skillScore")
        return self

    def printPlanetStat(self, stat):
        total = 0
        for planet in self.planetList:
            if stat == "resourceScore":
                score = planet.resourceScore
            if stat == "populationScore":
                score = planet.populationScore
            if stat == "wealthScore":
                score = planet.wealthScore
            if stat == "skillScore":
                score = planet.skillScore
            print(score)
            total += score
        avg = total / len(self.planetList)
        print("average:", avg)

    def printSystemStat(self, stat):
        total = 0
        for system in self.systemList:
            if stat == "trafficScore":
                score = system.planetList[0].trafficScore
            print(score, len(system.planetList), system.faction)
            total += score
        avg = total / len(self.systemList)
        print("average:", avg)
                

def get_all_subclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        if not subclass.__subclasses__():
            initLog.log(subclass, "is leaf")
            all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses




'''

Checks if item is above base quantity or not. If it is, it regresses towards means, more likely to happen if is further from the mean. Extremeness 
only determined by how long it's been. Which direction randomly weighted determined by where it's positioned. If the current quantity is below the 
mean, then item.fallCount += 1. Then there is a one in item.fallCount/20 chance that a shortage for the item occurs. If yes, item.shortage = 1. 
While there is a shortage, each time prices are polled (or planet is visited really) then item.shortage -= time.random()*10

'''


