import time
import random
from customFormat import *
import StarTheory

class Shop(object):

    def __init__(self, market, consumer):
        self.market = market
        self.consumer = consumer
        self.refresh()   

    def refresh(self):
        self.shop = {}
        # Quantity is set to none. Also, how do you transact upgrades, since player can't trade them back
        for container in self.consumer.inventory.getAll():
            print(container)
            print(container.quantity)
            self.add(container.item, container.quantity, self.consumer)
            self.setPrice(container.item, (container.item.price * 1.5))
        for container in self.market.inventory.getAll():
            print(container.item)
            if not container.item.quantity:
                self.add(container.item, container.quantity, self.market)
                self.setPrice(container.item, container.item.getPrice(self.consumer))
            elif container.quantity > 0:
                self.add(container.item, container.quantity, self.market)
                self.setPrice(container.item, container.item.getPrice(self.consumer))
            elif self.consumer.inventory.get(container.item):
                self.setPrice(container.item, container.currentPrice)

    def priceMod(self, item):
        mod = 1
        if item.legal == False:
            mod += .5
        return mod

    def add(self, item, quantity, holder=False):
        if item.type not in self.shop.keys():
            self.shop[item.type] = {}
        if item.name not in self.shop[item.type].keys():
            self.shop[item.type][item.name] = {"price": 0, self.consumer.name: 0, self.market.name: 0, "item": item}
            if not quantity:
                self.shop[item.type][item.name][self.consumer.name] = ""
                self.shop[item.type][item.name][self.market.name] = ""
        if quantity:
            self.shop[item.type][item.name][holder.name] = quantity
        self.shop[item.type][item.name]["item"] = item

    def setPrice(self, item, price):
        price *= self.priceMod(item)
        self.shop[item.type][item.name]["price"] = int(price)

    def getCategory(self, category):
        try:
            return self.shop[category]
        except:
            return False

    def getItem(self, item):
        return self.shop[item.type][item.name]

    def printAvailability(self, item):
        printHeader3("Availability")
        itemDict = self.getItem(item)
        printBalanced(["Item", "Price", "Your Inventory", "Market"])
        printBalanced([item.name, u"\u0199 " + str(itemDict["price"]),
                       itemDict[self.consumer.name], itemDict[self.market.name]])
        print()

    def check(self, quantity, buyer, seller, item):
        itemDict = self.getItem(item)
        if item.quantity:
            if quantity > itemDict[seller.name]:
                print(f"{seller.name} does not have that many available")
                time.sleep(.5)
                return False
        if buyer.credits:
            if quantity * itemDict["price"] > buyer.credits:
                print(f"{buyer.name} does not have enough credits")
                time.sleep(.5)
                return False
        if buyer.space:
            if quantity * itemDict["item"].space > buyer.space:
                print(f"{buyer.name} does not have enough space")
                time.sleep(.5)
                return False
        return True

    def transact(self, buyer, seller, quantity, item):
        if quantity != 0:
            if buyer.credits:
                buyer.credits -= self.getItem(item)["price"] * quantity
            if seller.credits:
                seller.credits += self.getItem(item)["price"] * quantity
            if item.quantity:
                buyer.add(item, quantity)
                seller.remove(item, quantity)
            else:
                item.upgradeEffect(buyer)
        self.refresh()


class ItemContainer(object):

    def __str__(self):
        return self.item.name

    def __init__(self, item, owner, quantity=0):
        self.item = item
        if self.item.quantity:
            self.quantity = quantity
            self.active = True
        else:
            self.active = False
            self.quantity = None
            self.baseQuantity = None
            self.basePrice = item.price
            self.currentPrice = item.price
        self.owner = owner

    def initializeValues(self):
        self.shortage = False
        self.demandCount = 0  # random.uniform(0, 20)

        # Prices
        self.basePrice = None
        self.currentPrice = None

        # Quantity
        self.baseQuantity = None

        self.setBaseValues()

        self.quantity = self.baseQuantity
        self.currentPrice = self.basePrice

    def setBaseValues(self):
        resourceMod = self.resourceModifier()
        proximityMod = self.proximityModifier()

        self.basePrice = int(self.item.price * (.5 + self.owner.wealthScore)
                             * resourceMod * proximityMod)

        bQ = int(self.item.quantity * (.5 + self.owner.wealthScore)
            * resourceMod * (.2 + 2 * self.owner.populationScore) * (1/proximityMod))

        self.baseQuantity = max(bQ, 1)

    def resourceModifier(self):
        # percentage of that item necessary for this item.
        mod = 1
        for resource in self.item.resourceInputs.keys():
            multiplier = self.item.resourceCost(resource)
            if self.owner.getResource(resource).abundance > 0:
                mod -= multiplier * self.owner.getResource(resource).abundance
            else:
                mod += multiplier
        return mod

    def proximityModifier(self):
        mod = 1
        for planet in self.owner.system.planetList:
            if planet.inventory.get(self.item):
                mod *= .9
            else:
                mod *= 1.1
        return mod

    # quantity varies, sometimes falling to zero
    def update(self):
        if self.active:
            if self.shortage:
                print("shortage:", self.shortage)
                priceDecreaseChance = 0
                quantityIncreaseChance = 0
                self.shortage -= self.owner.timeRandom() * 10
                if self.shortage < 0:
                    self.shortage = False
                    print(f"{self.item} shortage over!")
                    self.demandCount = 0
            else:
                if self.quantity < self.baseQuantity:
                    self.demandCount += self.owner.timeRandom() * 10
                    print(f"Demand count: {self.demandCount} increased.")
                if (self.demandCount / 20) > random.random():
                    self.shortage = 1
                    print(f"{self.item} entering Shortage")
                priceDecreaseChance = self.quantity / \
                    (2 * self.baseQuantity)
                quantityIncreaseChance = self.currentPrice / (2 * self.basePrice)

            priceChange = max(
                int(self.owner.timeRandom(lower=.02) * self.basePrice), 1)
            quantityChange = max(
                int(self.owner.timeRandom(lower=.02) * self.baseQuantity), 1)

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
                self.quantity += int(quantityChange * qMod)
                if self.quantity > (self.baseQuantity * 3):
                    self.quantity = self.baseQuantity * 3
            else:
                self.quantity -= quantityChange
                if self.quantity < 0:
                    self.quantity = 0

    def add(self, quantity):
        self.quantity += quantity

    def remove(self, quantity):
        self.quantity -= quantity
        if self.quantity == 0:
            return False
        elif self.quantity < 0:
            raise Exception("Cannot have negative inventory")
        else:
            return True


class InventoryManager(object):

    '''
    Manages a dictionary of dictionaries of container objects. Containers hold meta-data on their items
    '''

    def __init__(self, owner):
        self.owner = owner
        self.inventories = {}
        
    def add(self, item, quantity=1):
        if item.type in self.inventories.keys():
            if item.name in self.inventories[item.type].keys():
                self.inventories[item.type][item.name].add(quantity)
            else:
                self.inventories[item.type][item.name] = ItemContainer(item, self.owner, quantity=quantity)
        else:
            self.inventories[item.type] = {}
            self.inventories[item.type][item.name] = ItemContainer(item, self.owner, quantity=quantity)
        return self.inventories[item.type][item.name]

    def remove(self, item, quantity=1):
        # Remove FillSpaceEffect not occurring
        if isinstance(self.owner, StarTheory.GenericPlayer):
            for i in range(quantity):
                item.removeEffect(self.owner)
        try:
            if self.inventories[item.type][item.name].remove(quantity):
                del(self.inventories[item.type][item.name])
        except:
            input("\n\nThat item is not in inventory and cannot be removed")

    # Returns Container object
    def get(self, item):
        try:
            return self.inventories[item.type][item.name]
        except:
            return False

    # Returns list of containers
    def getContainersOfType(self, itemType):
        items = [item for item in self.inventories[itemType].values()]
        #print("Container list:", items)
        return items

    # Returns list of containers
    def getAll(self):
        allItems = []
        for inventory in self.inventories.values():
            for item in inventory.values():
                allItems.append(item)
        return allItems


class ActiveInventoryManager(object):

    '''
    Manages inventories that have to have effects applied and removed to them. This includes weapons, modules, crew?, and stuff. Not cargo, and not stuff
    from planets.
    '''

    def __init__(self, owner):
        self.owner = owner
        self.inventories = {}
        # {"module":[Bridge(), Bridge(), Engine()], "weapon":[lightLaser(), HeavyLaser()]}

    def add(self, item):
        if item.active == True:
            item.addEffect(self.owner)
            if item.type in self.inventories.keys():
                self.inventories[item.type].add(item)
            else:
                # Adds item to a set that contains all items of that type
                self.inventories[item.type] = set()
                self.inventories[item.type].add(item)

    def remove(self, item):
        if item.active == True:
            for proxy in self.getItemsOfType(item.type):
                if proxy.__class__.__name__ == item.__class__.__name__:
                    self.inventories[item.type].remove(proxy)
                    break

    def getItemsOfType(self, itemType):
        items = [item for item in self.inventories[itemType]]
        #print("item List:", items)
        return items

    # calls reset effect for every item in inventory
    def reset(self):
        for inventory in self.inventories.values():
            for item in inventory:
                item.resetEffect()

    def autoEffect(self):
        for inventory in self.inventories.values():
            for item in inventory:
                item.autoEffect(self.owner)

