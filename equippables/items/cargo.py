from ..itemsClass import *
from ..effects import *
from ..resources import *

# price is per 10 lbs

class Cargo(Item):

    def __init__(self):
        super().__init__()
        self.type = "cargo"
        self.space = 1
        self.description = "This item can be sold, and it's prices and quantities are dynamic"
        self.active = False
        self.effects = [FillSpaceEffect(self)]

        # Shop stats
        self.basic = True
        self.skillScore = 0
        self.quantity = 1
        self.stacks = True


class Food(Cargo):

    def __init__(self):
        super().__init__()
        self.name = "Food"
        self.addResourceCost(
            {Carbon(): .65, Hydrogen(): .2, Nitrogen(): .1, Phosphorus(): .05})
        self.price = 16
        self.quantity = 250
        self.basic = True


class ExoticFood(Cargo):

    def __init__(self):
        super().__init__()
        self.name = "Exotic Foods & Spices"
        self.addResourceCost(
            {Carbon(): .55, Hydrogen(): .2, Nitrogen(): .1, Phosphorus(): .15})
        self.price = 250
        self.quantity = 25
        self.basic = True


class Liqour(Cargo):

    def __init__(self):
        super().__init__()
        self.name = "Liquor"
        self.addResourceCost(
            {Carbon(): .55, Hydrogen(): .2, Nitrogen(): .1, Phosphorus(): .15})
        self.price = 40
        self.quantity = 250
        self.basic = True


class LuxuryGoods(Cargo):

    def __init__(self):
        super().__init__()
        self.name = "Luxury Goods"
        self.addResourceCost(
            {Carbon(): .65, Hydrogen(): .2, Oxygen(): .1, Cosmium(): .05})
        self.price = 25000
        self.quantity = 35
        self.basic = True

    
class Textiles(Cargo):

    def __init__(self):
        super().__init__()
        self.name = "Textiles"
        self.addResourceCost(
            {Carbon(): .4, Hydrogen(): .2, Oxygen(): .3})
        self.price = 350
        self.quantity = 300
        self.basic = True


class Medicine(Cargo):

    def __init__(self):
        super().__init__()
        self.name = "Medical Supplies"
        self.addResourceCost(
            {Copper(): .2, Chlorine(): .2, Sodium(): .1, Calcium(): .05, Sulfur(): .05, Aluminum(): .3, Silicon(): .1})
        self.price = 21500
        self.quantity = 90
        self.basic = True


class Slaves(Cargo):

    def __init__(self):
        super().__init__()
        self.name = "Slaves"
        self.price = 200
        self.quantity = 20
        self.legal = False


class IllicitDrugs(Cargo):

    def __init__(self):
        super().__init__()
        self.name = "Illicit Drugs"
        self.addResourceCost(
            {Carbon(): .4, Hydrogen(): .35, Nitrogen(): .05, Oxygen(): .2})
        self.price = 38000
        self.quantity = 40
        self.legal = False
