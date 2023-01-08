
class Stats:
    def __init__(self, pokemon_id, level):
        self.hp = 0
        self.attack = 0
        self.special_attack = 0
        self.defense = 0
        self.special_defense = 0
        self.speed = 0

class Move:
    def __init__(self, id):
        self.id = id
        self.type = None
        self.damage = None
        self.arcuraccy = None
        self.pp = None

class MoveSet:
    def __init__(self, move_list):
        self.move_set = move_list

class Pokemon:
    def __init__(self, pokemon_id=-1, level=1):
        self.level = level
        self.pokemon_id = pokemon_id
        self.stats = Stats(pokemon_id, level)
        self.type = None
        self.set = None
