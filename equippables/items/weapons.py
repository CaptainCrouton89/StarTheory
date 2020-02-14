from ..itemsClass import *
from ..effects import *
from ..resources import *

class Weapon(Item):

    STRONG_RESISTANCE = .9
    MEDIUM_RESISTANCE = .6
    WEAK_RESISTANCE = .1

    STRONG_DAMAGE = .7
    MEDIUM_DAMAGE = .4
    WEAK_DAMAGE = .1

    def __init__(self):
        super().__init__()
        self.type = "weapon"
        self.description = "This weapon has no description yet"
        self.effects = [WeaponEffect(self)]
        self.tier = 1
        self.skillScore = .4
        self.cooldown = 0
        self.energyCost = 0
        self.potency = 1
        self.ticks = 0
        self.mods = []

    def setDamage(self):
        self.damage = self.tier * 200

    def addMod(self, mod):
        if len(self.mods) < (self.tier // 3):
            self.mods.append(mod)
            mod.modEffect(self)

    def removeMod(self, mod):
        self.mods.remove(mod)
        mod.unModEffect(self)

    def printStats(self):
        print(self.description)
        print()
        printHeader3("Effectiveness")
        printBalanced([
            "TYPE",
            "DAMAGE",
            "RESISTANCE"
        ], size=2)
        printBalanced(["Evasion/Engines", self.evasionDamage,
                       self.evasionResistance], size=2)
        printBalanced(["Hull Armor", self.hullDamage,
                       self.hullResistance], size=2)
        printBalanced(["Shield", self.shieldDamage,
                       self.shieldResistance], size=2)
        print("\n")
        printHeader3("Stats")
        printBalanced([
            "Speed: {}".format(self.speed),
            "Damage: {}".format(self.damage),
            "Cooldown: {}/{}".format(self.ticks, self.cooldown),
            "Energy Cost: {}".format(self.energyCost)
        ], size=2)
        print("\n")


#  WEAPON TYPES —————————————————————————————————————————————————————————————————————————————————————

# Implement getter functions so I can apply bonuses to things without permanently changing. E.g. getDamage = damage * potency, not just self.damage
# Should have subclasses of weapons, where they tweak the resistors and damage, or just nerf them with cool other effects as bonuses (.1 more resistances
# but more damage? .2 less of one type of damage in return for a cool effect that all children inherit?)
# Armor piercing rounds? Heat seeking? Cannons vs rays vs tubes etc.

class BallisticWeapon(Weapon):
    # deal targetMod * damage to that mod, and damage to ship = weaponDamage - (shipArmor mod * damage) for each damage type
    # HPdamage = damage - (evasion*score + hull*score + ...)
    # Then, your defense stats go down by HPdamage*score from that damagetype

    def __init__(self):
        super().__init__()
        self.name = "Ballistic Weapon"
        self.damageType = "ballistic"

        self.addResourceCost(
            {Iron(): .5, Manganese(): .1, Silicon(): .1, Carbon(): .2, Aluminum(): .1})

        # Resistors
        self.evasionResistance = Weapon.MEDIUM_RESISTANCE
        self.hullResistance = Weapon.STRONG_RESISTANCE
        self.shieldResistance = Weapon.WEAK_RESISTANCE

        # Damages
        self.evasionDamage = Weapon.MEDIUM_DAMAGE
        self.hullDamage = Weapon.WEAK_DAMAGE
        self.shieldDamage = Weapon.STRONG_DAMAGE


class ExplosiveWeapon(Weapon):

    def __init__(self):
        super().__init__()
        self.name = "Explosive Weapon"
        self.damageType = "explosive"

        self.addResourceCost(
            {Iron(): .1, Manganese(): .1, Silicon(): .1, Carbon(): .2, Aluminum(): .1, Phosphorus(): .2, Oxygen(): .2})

        # Resistors
        self.evasionResistance = Weapon.STRONG_RESISTANCE
        self.hullResistance = Weapon.WEAK_RESISTANCE
        self.shieldResistance = Weapon.MEDIUM_RESISTANCE

        # Damages
        self.evasionDamage = Weapon.WEAK_DAMAGE
        self.hullDamage = Weapon.STRONG_DAMAGE
        self.shieldDamage = Weapon.MEDIUM_DAMAGE


class BeamWeapon(Weapon):

    def __init__(self):
        super().__init__()
        self.name = "Beam Weapon"
        self.damageType = "beam"

        self.addResourceCost(
            {Neon(): .5, Silicon(): .2, Nitrogen(): .2, Carbon(): .1})

        # Resistors
        self.evasionResistance = Weapon.WEAK_RESISTANCE
        self.hullResistance = Weapon.MEDIUM_RESISTANCE
        self.shieldResistance = Weapon.STRONG_RESISTANCE

        # Damages
        self.evasionDamage = Weapon.STRONG_DAMAGE
        self.hullDamage = Weapon.MEDIUM_DAMAGE
        self.shieldDamage = Weapon.WEAK_DAMAGE

'''
class BioWeapon(Weapon):

    # These weapons aren't as effective as most weapons, but they have all sorts of special affects (changing tick speeds, etc)
    def __init__(self):
        super().__init__()
        self.name = "Bio Weapon"
        self.damageType = "bio"

        self.addResourceCost(
            {Carbon(): .5, Hydrogen(): .3, Chlorine(): .2})

        # Resistors
        self.evasionResistance = .5
        self.hullResistance = .9
        self.reflectorsResistance = .9
        self.shieldResistance = .1

        # Damages
        self.evasionDamage = .2
        self.hullDamage = .8
        self.reflectorsDamage = .05
        self.shieldDamage = .05

'''
# BALLISTIC WEAPONS —————————————————————————————————————————————————————————————————————————————————————

class LightRailgun(BallisticWeapon):

    def __init__(self):
        super().__init__()
        self.name = "Light Railgun"
        self.description = "Peewee-shooty-shooter"
        self.price = 1000
        self.space = 1
        self.speed = 2
        self.damage = 200
        self.cooldown = 5
        self.energyCost = 3


class HeavyRailgun(BallisticWeapon):

    def __init__(self):
        super().__init__()
        self.name = "Heavy Railgun"
        self.description = "Could be described as heavier than the typical railgun"
        self.price = 3000
        self.space = 2
        self.speed = 3
        self.damage = 700
        self.cooldown = 7
        self.energyCost = 4


class MoFoLaser(BallisticWeapon):

    def __init__(self):
        super().__init__()
        self.name = "Mo-Fo Laser"
        self.description = "This'll fuck you up dude"
        self.price = 10
        self.space = 1
        self.speed = 1
        self.damage = 50000
        self.cooldown = 1
        self.energyCost = 0


# LASER WEAPONS —————————————————————————————————————————————————————————————————————————————————————

class LightLaser(BeamWeapon):

    def __init__(self):
        super().__init__()
        self.name = "Light Laser"
        self.price = 1000
        self.space = 1
        self.speed = 2
        self.damage = 200
        self.cooldown = 5
        self.energyCost = 3


# EXPLOSIVE WEAPONS —————————————————————————————————————————————————————————————————————————————————————

class LightMissileTubes(ExplosiveWeapon):

    def __init__(self):
        super().__init__()
        self.name = "Light Missile Tubes"
        self.price = 1000
        self.space = 1
        self.speed = 2
        self.damage = 200
        self.cooldown = 5
        self.energyCost = 3
