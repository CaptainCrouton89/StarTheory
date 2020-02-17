#GameManager

import time as tm
import menus
import StarTheory as st
import story
import init
import pickle
import random
import commands

def initialize(quickStart=True):
    global time
    global player
    global storyline
    global galaxy
    global responseManager, interfaceStack, combatManager
    time = 0
    player = st.Player()
    storyline = story.Story()
    galaxy = init.Galaxy().initialize()
    responseManager = ResponseManager()
    interfaceStack = InterfaceStack(menus.FactionMenu(galaxy.factionList))
    combatManager = CombatManager(player)
    # Runs story
    if not quickStart:
        player.name = input("\nPlease type your name: ")
        storyline.firstStart()

def getCommand():
    # Use option IDs to identify what people want to do, eg. if option.ID = 0: do blah. Different menus would have different ID numbers for their options
    entry = responseManager.getResponse()
    return getInterface().getCommand(entry)

def getInterface():
    return interfaceStack.peek()

def setInterface(interface):
    global interfaceStack
    print(f"\nSetting interface to {interface.__class__.__name__} / {interface.name}\n\n")
    interfaceStack.push(interface)

def getPreviousInterface():
    previous = interfaceStack.pop()
    if interfaceStack.peek().__class__ == previous.__class__:
        getPreviousInterface()
    else:
        print(f"Back to {interfaceStack.peek()}")
    
def runCommand(command):
    command.execute()

def runGame():
    getInterface().display()
    command = getCommand()
    print(f"\nCommand: {command.name}\n")
    runCommand(command)

def newCombat():
    combatManager.addEnemies(generateEnemy())
    combatManager.initializeCombat()

def generateEnemy(tier=1, location=None):
    enemy = st.Enemy()
    return enemy

def nextTick():
    global time
    time += 1

def getTime():
    return time

def save():
    print("Saving")
    tm.sleep(3)
    with open('save/save', 'wb') as saveFile:
        pickle.dump(saveFile)
    print("Save successful")


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


class CombatManager(object):

    def __init__(self, gameManager):  # Usually also option.source would be put in as enemy ship
        self.game = gameManager
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
        combatants.append(player)
        return combatants
    
    def addEnemies(self, *enemies):
        print(f"Adding enemies: {enemies}")
        for enemy in enemies:
            self.enemies.append(enemy)

    def endCombat(self):
        player.resetBattleStats()
        for enemy in self.enemies:
            enemy.resetBattleStats()
        self.enemies.clear()

    def runCombat(self):
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

    '''
    def checkEnd(self):
        if player.tempHitpoints <= 0:
            commands.Victory(self.enemies[0]).build(self.game).execute()
        for enemy in self.enemies:
            if enemy.tempHitpoints <= 0:
                commands.Victory(enemy).build(self.game).execute()
    '''

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
        """global logger
        logger.log(f'''
        Turn: {self.turn}
        Player: {player.name}
        Avg DPR: {(500 - player.tempHitpoints)/self.turn}
        Damage Taken: {damage}
        HP: {player.tempHitpoints}
        Evasion: {player.tempEvasion}
        Hull: {player.tempHull}
        Shield: {player.tempShield}
        Was attacked by: {weapon.name}''', console=True)"""
        tm.sleep(.1)

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


time = None
player = None
storyline = None
galaxy = None
responseManager = None
interfaceStack = None
combatManager = None