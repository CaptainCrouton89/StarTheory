#Commands package may be already in use
import menus
import time
import random
import init
import itemManipulation
import gamemanager as gm

class Command(object):

    def __init__(self):
        #print(f"Issuing {self} command")
        self.name = self.__class__.__name__
        self.combatChance = 0

    def execute(self):
        print("Empty command executed")

    def showMap(self):
        #show map
        pass

    def potentialCombat(self):
        c = random.random()
        print("c:", c)
        if c < self.combatChance:
            return True
        return False


class AddWeapon(Command):

    def __init__(self, weapon):
        super().__init__()
        self.weapon = weapon

    def execute(self):
        if self.weapon.ticks < self.weapon.cooldown:
            print("The weapon is not yet online!")
            time.sleep(.1)
            gm.setInterface(menus.WeaponInfoMenu(self.weapon))
        elif self.weapon.energyCost > gm.player.tempEnergy:
            print("You need more energy!")
            time.sleep(.1)
            gm.setInterface(menus.WeaponInfoMenu(self.weapon))
        else:
            gm.combatManager.addToQueue(self.weapon, gm.player)
            print("Weapon added")
            gm.setInterface(menus.FightMenu(gm.player))


class Back(Command):

    def __init__(self):
        super().__init__()

    def execute(self):
        gm.getPreviousInterface()


class Claim(Command):

    def __init__(self, planet):
        super().__init__()
        self.planet = planet

    def execute(self):
        gm.setInterface(menus.ClaimMenu(self.planet))


class ExamineItem(Command):
    def __init__(self, shop, item):
        super().__init__()
        self.shop = shop
        self.item = item

    def execute(self):
        gm.setInterface(menus.ExamineItemMenu(self.shop, self.item))


class Faction(Command):

    def __init__(self, factionList):
        super().__init__()
        self.factionList = factionList

    def execute(self):
        gm.setInterface(menus.FactionMenu(self.factionList))


class Fight(Command):

    def __init__(self):
        super().__init__()

    def execute(self):
        gm.newCombat()
        gm.setInterface(menus.FightMenu(gm.player))


class Fire(Command):

    def __init__(self):
        super().__init__()

    def execute(self):
        gm.combatManager.AIBuildQueue()
        gm.combatManager.runCombat()
        gm.setInterface(menus.FightMenu(gm.player))


class Help(Command):

    def __init__(self):
        super().__init__()

    def execute(self):
        gm.setInterface(menus.HelpMenu())


class Inventory(Command):

    def __init__(self):
        super().__init__()

    def execute(self):
        gm.setInterface(menus.InventoryMenu(gm.player))


class Map(Command):

    def __init__(self):
        super().__init__()

    def execute(self):
        self.showMap()
        gm.setInterface(menus.MapMenu())


class Nothing(Command):

    def __init__(self):
        super().__init__()

    def execute(self):
        print("Please enter a command")


class Planet(Command):

    def __init__(self, planet, combatChance=.1):
        super().__init__()
        self.planet = planet
        self.combatChance = combatChance

    def execute(self):
        if self.potentialCombat():
            gm.runCommand(RandomEncounter())
        gm.setInterface(menus.PlanetMenu(self.planet))


class PlanetPicker(Command):

    def __init__(self, system):
        super().__init__()
        self.system = system

    def execute(self):
        gm.setInterface(menus.PlanetPickerMenu(self.system))


class Quest(Command):

    def __init__(self, planet):
        super().__init__()
        self.planet = planet

    def execute(self):
        gm.setInterface(menus.QuestMenu(self.planet))


class QuitGame(Command):

    def __init__(self):
        super().__init__()
        
    def execute(self):
        quit()


class RandomEncounter(Fight):

    def __init__(self):
        super().__init__()

    def execute(self):
        gm.newCombat()
        gm.setInterface(menus.FightMenu(gm.player, random=True))


class Save(Command):

    def __init__(self):
        super().__init__()

    def execute(self):
        gm.save()


class ShipPicker(Command):

    def __init__(self, system):
        super().__init__()
        self.system = system

    def execute(self):
        gm.setInterface(menus.ShipPickerMenu(self.system))


class ShipStats(Command):

    def __init__(self, source):
        super().__init__()
        self.source = source

    def execute(self):
        gm.setInterface(menus.StatsMenu(self.source))


class System(Command):

    def __init__(self, system, combatChance=.15):
        super().__init__()
        self.system = system
        self.combatChance = combatChance

    def execute(self):
        if self.potentialCombat():
            gm.runCommand(RandomEncounter())
        gm.nextTick()
        gm.setInterface(menus.SystemMenu(self.system))


class SystemPicker(Command):

    def __init__(self, system):
        super().__init__()
        self.system = system

    def execute(self):
        gm.setInterface(menus.SystemPickerMenu(self.system))


class Trade(Command):

    def __init__(self, market):
        super().__init__()
        self.market = market

    def execute(self):
        if isinstance(self.market, init.PlanetEntity):
            for container in self.market.inventory.getAll():
                container.update()
        self.shop = itemManipulation.Shop(self.market, gm.player)
        gm.setInterface(menus.TradeMenu(self.shop))


class TradeCategory(Command):

    def __init__(self, shop, category):
        super().__init__()
        self.shop = shop
        self.category = category

    def execute(self):
        gm.setInterface(menus.TradeCategoryMenu(self.shop, self.category))


class TransactItem(Command):

    def __init__(self, transaction, shop, item):
        super().__init__()
        self.transaction = transaction
        self.shop = shop
        self.item = item

    def execute(self):
        print("Enter 0 to go back")
        while True:
            try:
                quantity = int(input(f"How many would you like to {self.transaction}?\n"))
            except:
                print("Please enter an integer\n")
            if self.transaction == "buy":
                buyer = self.shop.consumer
                seller = self.shop.market
            elif self.transaction == "sell":
                buyer = self.shop.market
                seller = self.shop.consumer
            if self.shop.check(quantity, buyer, seller, self.item):
                self.shop.transact(buyer, seller, quantity, self.item)
                break

        gm.setInterface(menus.TradeCategoryMenu(self.shop, self.item.type))
        

class UpdateShop(Command):

    def __init__(self, planet, turns):
        super().__init__()
        self.planet = planet
        self.turns = turns

    def execute(self):
        self.planet.timeDifference = self.turns
        for container in self.planet.inventory.getAll():
            container.update()
        gm.setInterface(menus.StatsMenu(self.planet))


class WeaponInfo(Command):

    def __init__(self, weapon):
        super().__init__()
        self.weapon = weapon

    def execute(self):
        gm.setInterface(menus.WeaponInfoMenu(self.weapon))

    #changes
    #singleton!