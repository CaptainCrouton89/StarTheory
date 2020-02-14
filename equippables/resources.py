import math
import copy

# Prices per 1000 lbs

class Resource(object):

    def __init__(self):
        self.name = "Unnamed resource"
        self.solid = False
        self.solidTemp = 0
        self.rarity = 0
        self.adjustedRarity = 0
        self.abundance = 0
        self.usefulness = 0

    def __str__(self):
        return f'{self.name}'

    def causeEffect(self, planet):
        pass

    '''
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result
    '''


class Hydrogen(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Hydrogen"
        self.type = "gas"
        self.solidTemp = -434
        self.rarity = .95
        self.skillScore = .4
        self.usefulness = .9
        self.price = 140

    def causeEffect(self, planet):
        planet.trafficScore += (1 - planet.trafficScore) * \
            (self.abundance ** 2)


class Helium(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Helium"
        self.solidTemp = -458
        self.rarity = .9
        self.skillScore = .4
        self.usefulness = .2
        self.price = 2000


class Oxygen(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Oxygen"
        self.solidTemp = -360
        self.rarity = .3
        self.skillScore = .2
        self.usefulness = .9
        self.price = 250

    def causeEffect(self, planet):
        planet.populationScore += (1 - planet.populationScore) * \
            (self.abundance ** 2)


class Carbon(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Carbon"
        self.solidTemp = 3800
        self.rarity = .7
        self.skillScore = .3
        self.usefulness = .9
        self.price = 2200

    def causeEffect(self, planet):
        planet.populationScore += (1 - planet.populationScore) * \
            (self.abundance ** 3)


class Iron(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Iron"
        self.solidTemp = 2800
        self.rarity = .4
        self.skillScore = .3
        self.usefulness = .8
        self.price = 63


class Neon(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Neon"
        self.solidTemp = -415
        self.rarity = .6
        self.skillScore = .4
        self.usefulness = .3
        self.price = 33000


class Nitrogen(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Nitrogen"
        self.solidTemp = -346
        self.rarity = .7
        self.skillScore = .3
        self.usefulness = .9
        self.price = 430


class Silicon(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Silicon"
        self.solidTemp = 2200
        self.rarity = .6
        self.skillScore = .3
        self.usefulness = .8
        self.price = 290


class Aluminum(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Aluminum"
        self.solidTemp = 933
        self.rarity = .5
        self.skillScore = .3
        self.usefulness = .7
        self.price = 210


class Sulfur(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Sulfur"
        self.solidTemp = 240
        self.rarity = .6
        self.skillScore = .3
        self.usefulness = .6
        self.price = 7


class Sodium(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Sodium"
        self.solidTemp = 208
        self.rarity = .5
        self.skillScore = .3
        self.usefulness = .6
        self.price = 3000


class Phosphorus(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Phosphorus"
        self.solidTemp = 111
        self.rarity = .4
        self.skillScore = .3
        self.usefulness = .6
        self.price = 9


class Chlorine(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Chlorine"
        self.solidTemp = -150
        self.rarity = .4
        self.skillScore = .3
        self.usefulness = .6
        self.price = 6


class Manganese(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Manganese"
        self.solidTemp = 1520
        self.rarity = .6
        self.skillScore = .3
        self.usefulness = .6
        self.price = 185


class Copper(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Copper"
        self.solidTemp = 1358
        self.rarity = .6
        self.skillScore = .3
        self.usefulness = .6
        self.price = 580


class Calcium(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Calcium"
        self.solidTemp = 1548
        self.rarity = .6
        self.skillScore = .3
        self.usefulness = .6
        self.price = 20


class Uranium(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Uranium"
        self.solidTemp = 2070
        self.rarity = .1
        self.skillScore = .6
        self.usefulness = .8
        self.price = 5500


class Cosmium(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Cosmium"
        self.solidTemp = 4676
        self.rarity = .05
        self.skillScore = .7
        self.usefulness = 1
        self.price = 100000

    def causeEffect(self, planet):
        planet.resourceScore += (1 - planet.resourceScore) * \
            math.sqrt(self.abundance)
        planet.wealthScore += (1 - planet.wealthScore) * \
            math.sqrt(self.abundance)


class Valereon(Resource):

    def __init__(self):
        super().__init__()
        self.name = "Valereon"
        self.solidTemp = -390
        self.rarity = .05
        self.skillScore = .7
        self.usefulness = 1
        self.price = 40000

    def causeEffect(self, planet):
        planet.resourceScore += (1 - planet.resourceScore) * \
            math.sqrt(self.abundance)
        planet.wealthScore += (1 - planet.wealthScore) * \
            math.sqrt(self.abundance)


