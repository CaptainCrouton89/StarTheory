import commands
from math import *
import time
from customFormat import *
from StarTheory import *

class Interface(object):

    def __init__(self):
        self.options = []
        self.globalOptions = {
            "q": commands.QuitGame(),
            "i": commands.Inventory(),
            "f": commands.Fight(),
            "m": commands.Map(),
            "h": commands.Help(),
            "s": commands.Save(),
            "b": commands.Back()
        }
        self.content = False
        self.stats = False
        self.optionWidth = 10
        self.clear = True
        self.name = "no-name"
        self.player = None

    def getCommand(self, choice):
        if choice in self.globalOptions.keys():
            return self.globalOptions[choice]
        if self.options:
            try:
                return self.options[int(choice)-1].command
            except:
                print(
                    "Please enter an integer or a global key command. Enter 'h' for more help.")
                time.sleep(.25)
                return commands.Nothing()
        else:
            raise Exception("No options available!")

    def display(self):
        if self.name:
            self.printTitle()
        if self.stats:
            self.printStats()
        self.printContent()
        if self.options:
            self.printOptions()

    def printTitle(self):
        printHeader1(self.name, self.clear)

    def printStats(self):
        print()
        printBalanced(["Health", "Evasion", "Hull",
                       "Energy Shield"])
        printBalanced([
            self.player.tempHitpoints,
            self.player.tempEvasion,
            self.player.tempHull,
            self.player.tempShield])

    def printContent(self):
        print()

    def printOptions(self):
        print()
        if self.options:
            i = 0
            for option in self.options:
                i += 1
                if option.style == "balanced":
                    description = option.description[:]
                    description.insert(0, str(i) + f": {option.name}")
                    printBalanced(description)
                else:
                    print(str(i) + ":", "{0:{2}} {1:<}".format(option.name,
                                                            option.description, self.optionWidth))
                if option.style == "space1":
                    print()


class Option(object):

    def __init__(self, name="", description="", command=None, style=None):
        self.name = name
        self.description = description
        self.command = command
        self.style = style


class BackOption(Option):

    def __init__(self):
        super().__init__()
        self.name = "back"
        self.description = "return to the previous screen"
        self.command = commands.Back()


class InventoryMenu(Interface):

    def __init__(self, player):
        super().__init__()
        self.name = "Inventory"
        self.player = player
        self.content = True
        self.options = [BackOption()]

    def printContent(self):
        super().printContent()
        printHeader2("Crew")
        for container in self.player.inventory.getContainersOfType("officer"):
            print(container, container.quantity)
        printHeader2("\n\nModules")
        for container in self.player.inventory.getContainersOfType("module"):
            print(container, container.quantity)
        printHeader2("\n\nWeapons")
        for container in self.player.inventory.getContainersOfType("weapon"):
            print(container, container.quantity)
        printHeader2("\n\nCargo")
        for container in self.player.inventory.getContainersOfType("cargo"):
            print(container, container.quantity)
        print()


class PlanetMenu(Interface):

    def __init__(self, planet):
        super().__init__()
        self.planet = planet
        self.name = planet.name

        try:
            self.name += f" ({self.planet.system.faction.name})"
        except:
            pass

        self.options = [
            Option("stats", "check stats of planet", commands.ShipStats(planet)),
            Option("trade", "buy or sell items", commands.Trade(planet)),
            Option("claim", "claim this planet for your faction",
                    commands.Claim(planet)),
            Option("quest", "see what jobs are for offer",
                    commands.Quest(planet)),
            Option("star gate", "return to the star gate",
                    commands.System(planet.system)),
            Option("planets", "travel to another planet in this star system", commands.PlanetPicker(planet.system)),
            BackOption()
            ]

    def printContent(self):
        super().printContent()
        print(self.planet.getDescription())


class StatsMenu(Interface):

    def __init__(self, planet):
        super().__init__()
        self.planet = planet
        self.name = planet.name

        self.options = [
            Option("update1", "Update store as if 1 turn had passed", commands.UpdateShop(self.planet, 1)),
            Option("update2", "Update store as if 10 turns had passed", commands.UpdateShop(self.planet, 10)),
            Option("update3", "Update store as if 100 turns had passed", commands.UpdateShop(self.planet, 100)),
            BackOption()
        ]

    def printContent(self):
        super().printContent()
        print("Temperature:", self.planet.temperature)
        printBalanced([
            "Resources: {0}".format(self.planet.resourceScore),
            "Traffic: {0}".format(self.planet.trafficScore),
            "Population: {0}".format(self.planet.populationScore),
            "Wealth: {0}".format(self.planet.wealthScore),
            "Skill: {0}".format(self.planet.skillScore)])
        for resource in self.planet.resourceList:
            print(resource.name, "abundance:", resource.abundance,
                  "score boost:", min(log10(resource.price) / 5, 1) * resource.abundance)
        for container in self.planet.inventory.getAll():
            printBalanced([container.item.name, 
                f"cQuantity: {container.quantity}",
                f"bQuantity: {container.baseQuantity}",
                f"cPrice: {container.currentPrice}",
                f"bPrice: {container.basePrice}"])


class SystemMenu(Interface):

    def __init__(self, system):
        super().__init__()
        self.name = system.name

        try:
            self.name += " system star-gate ({})".format(
                self.source.faction.name)
        except:
            pass
        self.options = [Option("land", "land on a planet", commands.PlanetPicker(system)),
                        Option("jump", "hyperjump to a nearby star-system",
                               commands.SystemPicker(system)),
                        Option("ships", "browse other ships in the system", commands.ShipPicker(system))]


class SystemPickerMenu(Interface):

    def __init__(self, system):
        super().__init__()
        self.system = system

        self.options = []
        for system in system.getFactionNeighbors():
            self.options.append(
                Option(system.name, system.description, commands.System(system)))


class ShipPickerMenu(Interface):

    def __init__(self, system):
        super().__init__()
        self.system = system

        self.options = []
        for ship in system.getShips():
            self.options.append(
                Option(ship.name, ship.description, commands.ShipPicker(system)))


class ShipMenu(Interface):

    def __init__(self, ship):
        super().__init__()
        self.name = ship.name
        self.options = [Option("attack", "attack the ship", commands.Fight()),
                        #Option(
                        #    "contact", "communicate with the captain of the ship", commands.Communicate()),
                        Option("back", "go back", commands.Back())
                        ]


class PlanetPickerMenu(Interface):

    def __init__(self, system):
        super().__init__()
        self.name = system.name

        self.options = []
        for planet in system.planetList:
            self.options.append(
                Option(planet.name, planet.description, commands.Planet(planet)))


class TradeMenu(Interface):

    def __init__(self, shop):
        super().__init__()
        self.shop = shop
        self.name = shop.market.name + " Trade"
        self.options = [
            Option("upgrade", "upgrade your ship", commands.TradeCategory(self.shop, "upgrade")),
            Option("weapon", "buy or sell weapons", commands.TradeCategory(self.shop, "weapon")),
            Option("module", "buy or sell modules", commands.TradeCategory(self.shop, "module")),
            Option("cargo", "buy or sell cargo", commands.TradeCategory(self.shop, "cargo")),
            Option("back", "back to previous menu", commands.Planet(shop.market))
        ]

        self.content = True

    def printCategory(self, category):
        printHeader2(f"\n{category.upper()}S ")
        if category not in self.shop.shop.keys():
            print("None available")
        else:
            for key, value in self.shop.getCategory(category).items():
                printBalanced([key, u"\u0199 " + str(value["price"]),
                            value[self.shop.consumer.name], value[self.shop.market.name]])
        print()

    def printContent(self):
        super().printContent()
        print("Credits:", self.shop.consumer.credits)
        print("Space:", self.shop.consumer.space, "\n")

        printBalanced(["Item", "Price", "Your Inventory", "Market"])
        self.printCategory("upgrade")
        self.printCategory("weapon")
        self.printCategory("module")
        self.printCategory("cargo")
        
        
class TradeCategoryMenu(Interface):

    def __init__(self, shop, category):
        super().__init__()
        self.name = category
        self.shop = shop
        if not shop.getCategory(category):
            print("Nothing available")
        else:
            for key, value in shop.getCategory(category).items():
                self.options.append(Option(key, [u"\u0199 " + str(
                    value["price"]), value[shop.consumer.name], value[shop.market.name]], commands.ExamineItem(shop, value["item"]), style="balanced"))
        self.options.append(Option("back", "back to trade menu", commands.Trade(shop.market)))

    def printContent(self):
        super().printContent()
        print("Credits:", self.shop.consumer.credits)
        print("Space:", self.shop.consumer.space, "\n")
        printBalanced(["Item", "Price", "Your Inventory", "Market"])


class ExamineItemMenu(Interface):

    def __init__(self, shop, item):
        super().__init__()
        self.name = item.name
        self.shop = shop
        self.item = item
        self.options = [
            Option("buy", "buy this item", commands.TransactItem("buy", shop, item)),
            Option("sell", "sell this item", commands.TransactItem("sell", shop, item)),
            Option("back", "back to trade menu", commands.TradeCategory(shop, item.type), style="space1")
        ]

    def printContent(self):
        super().printContent()
        print("Credits:", self.shop.consumer.credits)
        print("Space:", self.shop.consumer.space, "\n")
        try:
            self.item.printStats()
        except:
            pass

        self.shop.printAvailability(self.item)
        
        #print(item.getStats())


class ExploreMenu(Interface):

    def __init__(self, planet):
        super().__init__()
        self.planet = planet
        self.name = planet.name
        self.options = [BackOption()]


class ClaimMenu(Interface):

    def __init__(self, planet):
        super().__init__()
        self.planet = planet
        self.name = planet.name
        self.options = [BackOption()]


class QuestMenu(Interface):

    def __init__(self, planet):
        super().__init__()
        self.planet = planet
        self.name = planet.name
        self.options = [BackOption()]


class FactionMenu(Interface):

    def __init__(self, factionList):
        super().__init__()
        self.name = "Choose your faction"
        self.clear = False

        self.options = []
        for faction in factionList:
            self.options.append(
                Option(faction.name, faction.description, commands.Planet(faction.base.planetList[0])))
        self.content = "You can always type 'q' to exit the game"


class ContactMenu(Interface):

    def __init__(self, planet=False, ship=False):
        super().__init__()
        self.source = planet
        self.name = planet.name
        self.options = [BackOption()]


class FightMenu(Interface):

    def __init__(self, player, random=False):  # player, enemy
        super().__init__()
        self.random = random
        self.name = "combat"
        self.stats = True
        self.player = player
        self.optionWidth = 20
        self.options.append(
            Option("fire", "fires all weapons in queue",
                   commands.Fire(), style="space1")
        )
        for weapon in self.player.getItemsOfType("weapon"):
            self.options.append(
                Option(weapon.name, weapon.description, commands.WeaponInfo(weapon)))

    def printStats(self):
        super().printStats()
        print()
        printBalanced([
            "Energy: {}".format(self.player.tempEnergy),
            "Ticks/Turn: {}".format(self.player.tickCount)])

    def printContent(self):
        if self.random:
            print(f"\nYou are under attack by enemy pirates! Defend your ship!")


class VictoryMenu(Interface):

    def __init__(self, enemy, loot):
        super().__init__()
        self.name = "Victory!"
        
        self.content = "You have destroyed their ship! You have gained {0} scrap, {1} circuits, and {2} wires.".format(
            self.scrapMetal,
            self.wires,
            self.circuits)
        self.options = [
            Option("next", "return to previous menu",
                   str(self.source.__name__), self.source)
        ]


class WeaponInfoMenu(Interface):

    def __init__(self, weapon):
        super().__init__()
        self.name = weapon.name
        self.weapon = weapon
        self.options = [
            Option("add", "Adds weapon to firing queue. All weapons in queue can be fired in main combat menu", commands.AddWeapon(weapon)),
            BackOption()
        ]

    def printContent(self):
        super().printContent()
        printHeader3("Description")
        self.weapon.printStats()


class ShipDestructionMenu(Interface):

    def __init__(self, player, enemyShip, previousMenu):
        super().__init__(player)
        self.name = "Victory"
        self.source = enemyShip
        self.previousMenu = previousMenu
        self.scrapMetal = enemyShip.generateResource(ScrapMetal())
        self.wires = enemyShip.generateResource(Wires())
        self.circuits = enemyShip.generateResource(Circuits())
        self.content = "You have destroyed their ship! You have gained {0} scrap, {1} circuits, and {2} wires.".format(
            self.scrapMetal,
            self.wires,
            self.circuits)
        self.options = [
            Option("next", "return to previous menu",
                   str(self.source.__name__), self.source)
        ]


class HelpMenu(Interface):

    def __init__(self):
        super().__init__()
        self.options = [BackOption()]


class MapMenu(Interface):

    def __init__(self):
        super().__init__()
        self.options = [BackOption()]
