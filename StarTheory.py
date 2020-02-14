'''
Current problems: When player and enemy add the same weapon, they are both fired at the enemy, whereas if they fire different weapons
they fire as they should. WTF

To Do:
- Convert to Unity
- Distribute clues arround galaxy, have them point you to next place.
    - Determine how you organize/keep track of all of them
- Give rewards for winning in combat. Provide ways of upgrading ship
- Build out story, beginning, middle, and end 
- No consequences for failing exploring planet, but you can't retry for a while. Crew has collective energy, gets depleted when they fail missions. Can't do
    missions when it's at zero. Recharges over time. 

- When you die/ship is destroyed (when you don't surrender) there have to be long lasting consequences with reminders. Interest is higher for your loans, stuff


'''

import log
import os
import sys
import time
import copy
import pickle
import random
from equippables.items.modules import *
from equippables.items.weapons import *
from equippables.items.cargo import *
import itemManipulation
import myFunctions
from customFormat import *
from init import *
import commands
import menus
import story

logger = log.Log("StarTheoryLogs")


class Stats(object):

    def __init__(self, hitpoints=500, evasion=100, hull=100, shield=100):

        # Defenses
        self.hitpoints = hitpoints
        self.evasion = evasion
        self.hull = hull
        self.shield = shield
        self.energy = 0

        self.name = "No-Name"
        self.level = 1
        self.space = 100
        self.tickCount = 0  # this is effected by # of crew
        self.ship = None

        # 1-100 chaos-law: Most heavily effected by most recent activities (weighted average)
        self.alignment = 50
        # 1-100 like your level: Most heavily effected by most recent activities (weighted average)
        self.reputation = 1
        # 1-100 untrusted-trusted: Most heavily effected by most recent activities (weighted average)
        self.honor = 50

        # Wealth
        self.credits = 0
        self.scrapMetal = 0
        self.circuits = 0
        self.wires = 0

        self.reset()

    def reset(self):
        self.tempHitpoints = self.hitpoints
        self.tempEvasion = self.evasion
        self.tempHull = self.hull
        self.tempShield = self.shield
        self.tempEnergy = self.energy

    def getLevel(self):
        return self.level


class GenericPlayer(object):

    def __getstate__(self): 
        return self.__dict__

    def __setstate__(self, d): 
        self.__dict__.update(d)

    def __init__(self):
        # Builds information
        self.stats = Stats()
        #self.inventory = Inventory(self)
        self.inventory = itemManipulation.InventoryManager(self)
        self.activeInventory = itemManipulation.ActiveInventoryManager(self)
        
    # allows calls like 'player.hitpoints' instead of 'player.stats.hitpoints'
    def __getattr__(self, stat):
        return getattr(self.stats, stat)
        raise AttributeError(stat)

    def getItemsOfType(self, itemType):
        return self.activeInventory.getItemsOfType(itemType)

    def getContainersOfType(self, itemType):
        return self.activeInventory.getContainersOfType(itemType)

    def resetBattleStats(self):
        self.activeInventory.reset()
        self.stats.reset()

    def nextRound(self):
        self.activeInventory.autoEffect()

    def addList(self, *items):
        for item in items:
            self.inventory.add(item)
            self.activeInventory.add(item)
        
    def add(self, item, quantity=1):
        self.inventory.add(item, quantity)
        for i in range(quantity):
            self.activeInventory.add(item)

    def removeList(self, *items):
        for item in items:
            self.inventory.remove(item)
            self.activeInventory.remove(item)

    def remove(self, item, quantity=1):
        self.inventory.remove(item, quantity)
        for i in range(quantity):
            self.activeInventory.remove(item)

    # Returns quantity of resource as reward on destruction
    def generateResource(self, item):
        if item.levelDependent == True:
            return item.rewardQuantity * self.level
        else:
            return item.rewardQuantity


class Enemy(GenericPlayer):

    def __init__(self):
        super().__init__()
        self.stats.hull = 200
        self.stats.evasion = 100
        self.addList(
            Bridge(),
            HydroCesBattery(),
            PReactor(),
            LightRailgun(),
            IllicitDrugs(),
            Food(),
            Food(),
            Officer(level=2)
        )
        self.credits = 10000

        # self.type.buildInventory()
        # self.type would be a class, deciding what kind of ship/weapons it has


class Player(GenericPlayer):

    __instance = None
    @staticmethod
    def getInstance():
        if Player.__instance == None:
            Player()
        return Player.__instance

    def __init__(self):
        if Player.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Player.__instance = self

        super().__init__()
        self.name = "You, the player"
        self.addList(
            Bridge(),
            HydroCesBattery(),
            PReactor(),
            LightLaser(),
            LightRailgun(),
            LightMissileTubes(),
            HeavyRailgun(),
            IllicitDrugs(),
            Food(),
            Food(),
            Officer(level=2)
        )
        self.credits = 10000
    

class CombatManager(object):

    def __init__(self, player):  # Usually also option.source would be put in as enemy ship
        #self.game = GameManager
        self.player = Player.getInstance()
        self.queue = []
        self.turn = 0
        self.enemies = []
        
    def initializeCombat(self):
        for combatant in self.getCombatants():
            combatant.resetBattleStats()

    def getCombatants(self):
        combatants = []
        for enemy in self.enemies:
            combatants.append(enemy)
        combatants.append(self.player)
        return combatants
    
    def addEnemies(self, *enemies):
        print(f"Adding enemies: {enemies}")
        for enemy in enemies:
            self.enemies.append(enemy)

    def endCombat(self):
        self.player.resetBattleStats()
        for enemy in self.enemies:
            enemy.resetBattleStats()
        self.enemies.clear()

    def runCombat(self):
        global logger
        logger.log("Running Combat")
        self.turn += 1
        while True:
            if not self.queue:
                break
            weapon, target = self.queue.pop(0)
            self.takeDamage(weapon, target)

        #Check for 0 hp
        for player in self.getCombatants():
            player.nextRound()
        self.queue.clear()
        
        #self.checkEnd()

    def checkEnd(self):
        if self.player.tempHitpoints <= 0:
            commands.Victory(self.enemies[0]).build(self.game).execute()
        for enemy in self.enemies:
            if enemy.tempHitpoints <= 0:
                commands.Victory(enemy).build(self.game).execute()

    def takeDamage(self, weapon, player):
        damage = max(int(weapon.damage - (
            player.tempEvasion * weapon.evasionResistance +
            player.tempHull * weapon.hullResistance +
            player.tempShield * weapon.shieldResistance
        )), 0)
        damage *= weapon.potency
        player.tempHitpoints = max(player.tempHitpoints - damage, 0)
        player.tempEvasion = int(max(player.tempEvasion - max(damage * weapon.evasionDamage, 0), 0))
        player.tempHull = int(max(player.tempHull - max(damage * weapon.hullDamage, 0), 0))
        player.tempShield = int(max(player.tempShield - max(damage * weapon.shieldDamage, 0), 0))
        global logger
        logger.log(f'''
        Turn: {self.turn}
        Player: {player.name}
        Avg DPR: {(500 - player.tempHitpoints)/self.turn}
        Damage Taken: {damage}
        HP: {player.tempHitpoints}
        Evasion: {player.tempEvasion}
        Hull: {player.tempHull}
        Shield: {player.tempShield}
        Was attacked by: {weapon.name}''', console=True)
        time.sleep(.1)

    def addToQueue(self, weapon, source, target=0):
        self.queue.append((weapon, self.getCombatants()[target]))
        weapon.actionEffect(source)

    def AIBuildQueue(self):
        ''' 
        V1: Chooses random weapon to fire each turn, and if it can't fire it, it randomly chooses again.
        V2: Chooses weapon that will reduce player's lowest stat if it is above half, otherwise tries to fire weapon that 
            deals the most damage using that stat
        V3: TBD
        '''
        for enemy in self.enemies:
            counter = 0
            while True:
                counter += 1
                if counter > 100:
                    logger.log("Enemy failed to find weapon")
                    print("AI Failure, please check logs")
                    time.sleep(1)
                    break
                weaponChoice = random.choice(enemy.getItemsOfType("weapon"))
                if weaponChoice.ticks < weaponChoice.cooldown:
                    continue
                elif weaponChoice.energyCost > enemy.energy:
                    continue
                else:
                    self.addToQueue(weaponChoice, enemy, target=-1)
                    break
                

class ResponseManager(object):

    def __init__(self):
        self.keybinds = {}

    def getInput(self):
        userInput = input().lower()
        return userInput

    def bind(self, key, newKey):
        self.keybinds[key] = newKey

    def unbind(self, key):
        self.keybinds.pop(key, None)

    def rebind(self, userInput):
        if userInput in self.keybinds.keys():
            return self.keybinds[userInput]
        return userInput

    def getResponse(self):
        userInput = self.getInput()
        order = self.rebind(userInput)
        return order
     

class InterfaceStack(object):

    def __init__(self, *interfaces):
        self.items = []
        for interface in interfaces:
            self.items.append(interface)

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)
        if len(self.items) > 10:
            self.items = self.items[-100:]

    def pop(self):
        return self.items.pop()


    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)


class GameManager(object):

    def __init__(self):
        pass

    def initialize(self, quickStart=True):
        self.time = 0

        # Creates Singletons
        self.player = Player()
        self.story = story.Story(self)
        self.galaxy = Galaxy(self).initialize()
        self.responseManager = ResponseManager()
        self.interfaceStack = InterfaceStack(
            menus.FactionMenu(self.galaxy.factionList))
        self.combatManager = CombatManager(self.player)

        # Runs story
        if not quickStart:
            self.player.name = input("\nPlease type your name: ")
            self.story.firstStart()

    def getCommand(self):
        # Use option IDs to identify what people want to do, eg. if option.ID = 0: do blah. Different menus would have different ID numbers for their options
        entry = self.responseManager.getResponse()
        return self.getInterface().getCommand(entry)

    def getInterface(self):
        return self.interfaceStack.peek()

    def getPreviousInterface(self):
        previous = self.interfaceStack.pop()
        if self.interfaceStack.peek().__class__ == previous.__class__:
            self.getPreviousInterface()
        else:
            print(f"Back to {self.interfaceStack.peek()}")
        
    def runCommand(self, command):
        command.build(self)
        command.execute()

    def runGame(self):
        self.getInterface().display()
        command = self.getCommand()
        print(f"\nCommand: {command.name}\n")
        self.runCommand(command)

    def newCombat(self):
        self.combatManager.addEnemies(self.generateEnemy())
        self.combatManager.initializeCombat()

    def generateEnemy(self, tier=1, location=None):
        enemy = Enemy()
        return enemy
    
    def nextTick(self):
        self.time += 1

    def getTime(self):
        return self.time

    def save(self):
        print("Saving")
        time.sleep(.3)
        with open('save/save', 'wb') as saveFile:
            pickle.dump(self, saveFile)
        print("Save successful")


class Game(object):

    def __init__(self):
        self.loadScreen()

    def loadScreen(self):
        printHeader0(font("Star Theory", "bold", "blue"))
        print("\n"*4)

    def newGame(self, quickStart=False):
        self.game = GameManager()
        self.game.initialize(quickStart)

    def loadSave(self):
        print("Loading save")
        time.sleep(.3)
        with open('save/save', 'rb') as saveFile:
            self.game = pickle.load(saveFile)
        print("Save loaded")

    def start(self):
        printCentered(font(
            "If this is a new game, press 'n'. To load a past save, press 'l'. To quit at any time, press q.", style="italics"))
        printItalics("")

        k = input()
        if k == "q":
            quit()
        elif k == "n":
            self.newGame()
        elif k == "l":
            self.loadSave()
        else:
            self.newGame(True)


    def runGame(self):
        while True:
            self.game.runGame()


def main():

    game = Game()
    game.start()

    while True:
        game.runGame()

if __name__ == "__main__":
    main()

'''

Ship generation

Many types of ships, with different size/level categories
- Freighters: Carry tons of cargo
- Convoys: Carry passengers
- Commercial Shuttle
- Mining ships
- Pioneer/Explorer ships
- Battle ships
- Yacht
- Aeroshuttle (space to the ground)
- Police
- Science Ship
- Scout
- Spy
- Tanker
- Tug


Each of these are in different sizes, particularly the battleships.
Warships: Designed for both FTL and STL travel
10  - Battleship: Heaviest
9   - Battlecruiser: Less heavy, more powerful
6-10- Fleet Carrier: For planetary assault, Battleship sized
7   - HeavyCruiser: Mid size warship
7   - Light Cruiser: Smaller escort missions
6   - Destroyer: Little glass cannons, protect bigger ships, protect ships from torpedoes
5   - Frigate: More balanced Destroyer, escort cruisers
4   - Corvette: patrol, convoy, secret shit
4   - Landing Ship: Carries landing craft to location. No weapons, will go through systems as well

Support: FTL Travel, but poor in STL
4-10- Cetral Supportive Station (CSS): Provides all the amenities for ship and crew care, like a warehouse/relaxation place
        - Minor and major sizes
2   - Repair ship: fast, maneuverable, no offensive abilities. Repairs ships, even in combat
4-6 - Hydroponic Ships: huge growing stations

Other: FTL and STL
5   - Galleon: Modified Frigate replacing some military modules for cargo. Still fast though - Not produced legally, used by pirates, can be used in
5   - M-Class Frigate: Used as a fleet carrier for mining drones for harvesting belts
5   - C-Class Frigate: Civilian/Company Frigate frame, but outfitted with minimal weaponry, used for transport/exploration/general use for
        major comapnies, especially resource harvesting ones
4   - C-Class Corvette: Good all around ship
3   - C-Class Pioneer: Pioneer/exploration ship. Mostly fuel, outfitted for inter-system, and has capactiy for landing craft. Used to find new resources, claim systems, etc.


Intersystem Transport: FTL only, too unmaneuverable for STL near planets
4-8 - Tankers: Lots of liquid, oil, water, fuel
2-8- Freighter (many different sizes)
5   - Heavy Passenger Liner: Commercial intersystem travel

Interplanetary Transport: STL only, and often times 
4   - Chebec: Modified corvettes for more cargo at the cost of defensive systems. - Privateers, pirates, government
3   - Passenger Liner: Commercial airplane of space - slow, unmaneuverable, cheap, and high capacity
2   - Shuttles: Basic interplanetary travel for small groups, lots of them. 
2-4 - Yacht: Used by the rich as pleasure cruisers


Orbital
2   - Cutters, fast inter-system travel, used by police and agents
2   - Brigantine: shuttle outfitted with light weapons - pirates
1   - M-drone: Mining drone, generally not manned. Small range.


Planetary
1   - Landing Craft: Transport troops and whatever else to ground in hurry.
1   - Orbital Transporter: Caries crew and or cargo to surface. 


You can buy any ship you want if it's sold at a location, not banned from certain ships.
The titles just determine their typical weapon/module/cargo ratios.

space = int((1/2) * x ** 2 + 4* x + 7)

Travel between systems takes you to certain jump point on system, entrance/exit to the warproads, 
which are fairly heavily guarded, usually a station built. 

- From System/Station Menu you can see what INtersystem ships and support/Military ships are there. "other" class ships can use these, 
but won't be found here

- From Planet Menu, you can see all the interplanetary, orbital, support, and military ships present

- If you land, you can access the planetary ships.

Depending where you are, there are various likelihoods that you would see each ship. Every time you jump, a random selection of ships are there, based on different stuff
Likelihood for military:
- Proximity to enemy faction
- Wealth, augmented a lot by danger. Both must be present for huge boost
- If conducting attack on another system

Likelihood for Support
- Same as military, but requires military to be there as well for different levels of support (level 25 military presence pulls with it 10 levels of support)

Intersystem
- Varies with traffic of planets in system, resource scores, and wealth



Ships/Crew have various scores, refecting their galactic standing
- Faction: dictionary of scores for each faction
- Honor: How you are respected - affects what happens on capture, the quests you get, whether you get back stabbed, if the govt trusts you
    etc.
- Reputation: How well known are you. This is like your level, and effects difficulty, and scalign in the game.
- Alignment: Law --> Chaos or Government/Military --> Law Abiding Citizen/Privateer --> Rogue/Pirate
- 


Add sub-factions later


Woken up on foreign asteroid to protect you from those who would wish to harm you. Malfunction in cryo chamber, asteroid was just passing in front of 
        a sun, and the ice covering the electronics just melted.
        
        On screen:
        Date ticks by, rapidly going faster and faster.
        "Sir?"
        "Sir? Wake up, Sir!"

'''
