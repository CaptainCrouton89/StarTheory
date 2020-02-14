import myFunctions
import log

effectsLogger = log.Log("effects")

class Effect(object):

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __init__(self, item):
        self.item = item

    def __getattr__(self, attr):
        return getattr(self.item, attr)

    def __str__(self):
        return self.__class__.__name__

    def announce(self, effect):
        effectsLogger.log(f"'{effect}' effect called for {self} on {self.item}!")

    def addEffect(self, player):
        self.announce("add")

    def removeEffect(self, player):
        self.announce("remove")

    def actionEffect(self, player):
        self.announce("action")

    def autoEffect(self, player):
        self.announce("auto")

    def resetEffect(self):
        self.announce("reset")

    def upgradeEffect(self):
        self.announce("upgradeApplied")


class UpgradeSpaceEffect(Effect):

    def __init__(self, upgrade):
        super().__init__(upgrade)
        self.upgrade = upgrade

    def upgradeEffect(self, player):
        player.stats.space += self.upgrade.potency


class UpgradeDefenseEffect(Effect):

    def __init__(self, upgrade, defense):
        super().__init__(upgrade)
        self.upgrade = upgrade
        self.defense = defense

    def upgradeEffect(self, player):
        #getattr(player, self.defense) += self.upgrade.potency
        pass


class FillSpaceEffect(Effect):

    def __init__(self, item):
        super().__init__(item)

    def addEffect(self, player):
        super().addEffect(player)
        player.stats.space -= self.item.space

    def removalEffect(self, player):
        super().removeEffect(player)
        player.stats.space += self.item.space


class CoolDownEffect(Effect):

    def __init__(self, item):
        super().__init__(item)

    def resetEffect(self):
        super().resetEffect()
        self.item.ticks = self.item.cooldown


class TweakItemEffect(Effect):

    def __init__(self, item):
        super().__init__(item)

    def modEffect(self, subject):
        subject.cooldown += self.item.cooldownBonus
        subject.energyCost += self.item.energyCostBonus
        subject.speedBonus += self.item.speedBonus
        subject.penetration += self.item.penetration

    def unModEffect(self, subject):
        subject.cooldown -= self.item.cooldownBonus
        subject.energyCost -= self.item.energyCostBonus
        subject.speedBonus -= self.item.speedBonus
        subject.penetration -= self.item.penetration


class WeaponEffect(Effect):

    def __init__(self, item):
        super().__init__(item)

    def actionEffect(self, player):
        super().actionEffect(player)
        self.item.ticks = 0
        player.stats.tempEnergy -= self.energyCost

    def autoEffect(self, player):
        super().autoEffect(player)
        if self.item.ticks < self.item.cooldown:
            self.item.ticks += player.stats.tickCount
        if self.item.ticks > self.item.cooldown:
            self.item.ticks = self.item.cooldown

    def resetEffect(self):
        super().resetEffect()
        self.item.ticks = self.item.cooldown


class BatteryEffect(Effect):

    def __init__(self, item):
        super().__init__(item)

    def addEffect(self, player):
        super().addEffect(player)
        player.stats.energy -= self.item.energyCost

    def removeEffect(self, player):
        super().removeEffect(player)
        player.stats.energy += self.item.energyCost


class ReactorEffect(Effect):

    def __init__(self, item):
        super().__init__(item)

    def autoEffect(self, player):
        super().autoEffect(player)
        player.stats.tempEnergy -= self.item.energyCost
        if player.stats.tempEnergy > player.stats.energy:
            player.stats.tempEnergy = player.stats.energy


class OfficerEffect(Effect):

    def __init__(self, item):
        super().__init__(item)

    def addEffect(self, player):
        super().addEffect(player)
        player.stats.tickCount += self.item.ticks

    def removeEffect(self, player):
        super().removeEffect(player)
        player.stats.tickCount -= self.item.ticks

    def autoEffect(self, player):
        super().autoEffect(player)
        return
        potency = 5 * self.item.level
        if self.item.specialty == "evasion":
            player.stats.tempEvasion += potency
        elif self.item.specialty == "hull":
            player.stats.tempHull += potency
        elif self.item.specialty == "shield":
            player.stats.tempShield += potency
        print("type:", self.item.specialty, "adding:", 5 * self.item.level)
            # need to cap this off.
            # SHould change player defense stats to a dictionary
