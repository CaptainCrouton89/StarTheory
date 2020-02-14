from ..itemsClass import *
from ..effects import *
from ..resources import *

class Module(Item):

    def __init__(self):
        super().__init__()
        self.effects = [CoolDownEffect(self), FillSpaceEffect(self)]
        self.type = "module"
        self.description = "Empty module description"

        self.addResourceCost(
            {Iron(): .3, Manganese(): .1, Silicon(): .05, Carbon(): .2, Aluminum(): .15, Copper(): .2})
        self.quanity = 2
        self.space = 10
        self.price = 5000
        self.skillScore = .4

        self.ticks = 0
        self.cooldown = 0
        self.energyCost = 0
        self.potency = 0


class Battery(Module):

    def __init__(self):
        super().__init__()
        self.effects.append(BatteryEffect(self))


class Reactor(Module):

    def __init__(self):
        super().__init__()
        self.effects.append(ReactorEffect(self))


class Engine(Module):

    def __init__(self):
        super().__init__()
        self.action = True


# ACTUAL MODULES ——————————————————————————————————————————————————————————

class Bridge(Module):

    def __init__(self):
        super().__init__()
        self.addResourceCost(
            {Neon(): .2})
        self.name = "Bridge"
        self.price = 1000
        self.speed = 2
        self.cooldown = 13
        self.energyCost = 4


class HydroCesBattery(Battery):

    base = False

    def __init__(self):
        super().__init__()
        self.addResourceCost(
            {Carbon(): .5, Sulfur(): .3, Copper(): .2})
        self.name = "Hydro-Ces Battery"
        self.price = 5500
        self.speed = 1
        self.cooldown = 10
        self.energyCost = -6


class PReactor(Reactor):

    def __init__(self):
        super().__init__()
        self.name = "P-Reactor"
        self.addResourceCost(
            {Uranium(): .4, Manganese(): .3})
        self.price = 9000
        self.speed = 0
        self.cooldown = 10
        self.energyCost = -3
