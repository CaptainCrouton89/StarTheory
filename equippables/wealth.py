class Scrap(object):

    def __init__(self):
        self.name = "Scrap"
        self.price = 1000
        self.levelDependent = True
        self.rewardQuantity = 10


class Wires(Scrap):

    def __init__(self):
        super().__init__()
        self.name = "Wires"


class ScrapMetal(Scrap):

    def __init__(self):
        super().__init__()
        self.name = "Scrap Metal"


class Circuits(Scrap):

    def __init__(self):
        super().__init__()
        self.name = "Circuits"

class Credits(object):

    def __init__(self):
        pass

