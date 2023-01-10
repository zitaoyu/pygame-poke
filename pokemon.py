import json
import random
from data_downloader import POKEDEX_DATA_PATH, MOVES_DATA_PATH


class Pokedex:
    def __init__(self):
        with open(POKEDEX_DATA_PATH, 'r') as pokedex_data:
            self._pokedex = json.load(pokedex_data)["pokedex"]

    def get(self, id):
        return self._pokedex[id - 1]

class MovesBank:
    def __init__(self):
        with open(MOVES_DATA_PATH, 'r') as moves_data:
            self._moves_data = json.load(moves_data)["moves"]

    def get(self, id):
        return self._moves_data[id - 1]

POKEDEX = Pokedex()
MOVES = MovesBank()


class Move:
    def __init__(self, id):
        data = MOVES.get(id)

        self.id = data["id"]
        self.accuracy = data["accuracy"]
        self.damage_class = data["damage_class"]
        self.effect_chance = data["effect_chance"]
        self.effect = data["effect_entries"]["effect"]
        self.short_effect = data["effect_entries"]["short_effect"]
        self.name = data["name"]
        self.power = data["power"]
        self.pp = data["pp"]
        self.priority = data["priority"]
        self.target = data["target"]
        self.type = data["type"]
        
        self.stat_change = []
        for change in data["stat_changes"]:
            self.stat_change.append({
                "change": change["change"],
                "stat": change["stat"]["name"]
            })

class MoveSet:
    def __init__(self, moves=None):
        self.move_set = [None] * 4

        for i in range(len(moves)):
            self.move_set[i] = moves[i]
    
    def __str__(self) -> str:
        string = ""
        for move in self.move_set:
            string += "\n\nName: " + move.name + "\nPower: " + str(move.power) + "\nAccuracy:" + str(move.accuracy) + "\nType: "+ move.type + "\nPP: " + str(move.pp) +"\nEffect: " + move.short_effect
        return string

class MovePool:
    def __init__(self, moves_data):
        self.level_up_moves = []
        self.machine_moves = []
        self.egg_moves = []
        self.tutor_moves = []

        for move in moves_data:
            method = move["move_learn_method"]
            if method == "level-up":
                self.level_up_moves.append(move)
            elif method == "machine":
                self.machine_moves.append(move)
            elif method == "egg":
                self.egg_moves.append(move)
            elif method == "tutor":
                self.tutor_moves.append(move)

    def get_default_moveset(self, level=1):
        available_moves = []
        for move in self.level_up_moves:
            if level >= move["level_learned_at"]:
                available_moves.append(move)
        size = len(available_moves)

        default_moves = []
        if size <= 4:
            for move in available_moves:
                id = move["id"]
                default_moves.append(Move(id))
        else:
            for num in random.sample(range(size), 4):
                id = self.level_up_moves[num]["id"]
                default_moves.append(Move(id))

        return MoveSet(default_moves)


class BaseStats:
    def __init__(self, stats):
        for stat in stats:
            if stat["name"] == "hp":
                self.hp = stat["base_stat"]

            elif stat["name"] == "attack":
                self.attack = stat["base_stat"]

            elif stat["name"] == "defense":
                self.defense = stat["base_stat"]

            elif stat["name"] == "special-attack":
                self.special_attack= stat["base_stat"]

            elif stat["name"] == "special-defense":
                self.special_defense = stat["base_stat"]

            elif stat["name"] == "speed":
                self.speed = stat["base_stat"]

    def get_base_stats(self):
        return {
            "hp" : self.hp,
            "attack" : self.attack,
            "defense" : self.defense,
            "special-attack" : self.special_attack,
            "special-defense" : self.special_defense,
            "speed" : self.speed
        }

class Pokemon:
    def __init__(self, id, level=1):
        self.id = id
        self.level = level

        # retrieve pokemon data
        data = POKEDEX.get(id)
        self.name = data["name"]
        self.type = data["types"]
        self.base_stats = BaseStats(data["stats"])

        # moves
        self.move_pool = MovePool(data["moves"])
        self.move_set = self.move_pool.get_default_moveset(self.level)

        # IVs and EVs initialization
        self._generate_ivs()
        self.hp_ev = 0
        self.attack_ev = 0
        self.defense_ev = 0
        self.special_attack_ev = 0
        self.special_defense_ev = 0
        self.speed_ev = 0

        # calculate stats
        self._update_stats()


    def _generate_ivs(self):
        ivs = random.sample(range(32), 6)
        self.hp_iv = ivs[0]
        self.attack_iv = ivs[1]
        self.defense_iv = ivs[2]  
        self.special_attack_iv = ivs[3]
        self.special_defense_iv = ivs[4]
        self.speed_iv = ivs[5]

    def _update_stats(self):
        # formula source: https://bulbapedia.bulbagarden.net/wiki/Stat
        # calculator: https://pycosites.com/pkmn/stat.php
        # 
        #       | (2 * Base + IV + [EV / 4]) * Level | 
        # HP =  |____________________________________| + Level + 10
        #       |                100                 |
        calculate_hp = lambda base, iv, ev, level: int(((2 * base + iv + (ev / 4)) * level / 100) + level + 10)
        calculate_stat = lambda base, iv, ev, level, nature=1: int((((2 * base + iv + (ev / 4)) * level / 100) + 5) * nature)
        self.hp = calculate_hp(self.base_stats.hp, self.hp_iv, self.hp_ev, self.level)
        self.attack = calculate_stat(self.base_stats.attack, self.attack_iv, self.attack_ev, self.level)
        self.defense = calculate_stat(self.base_stats.defense, self.defense_iv, self.defense_ev, self.level)
        self.special_attack = calculate_stat(self.base_stats.special_attack, self.special_attack_iv, self.special_attack_ev, self.level)
        self.special_defense = calculate_stat(self.base_stats.special_defense, self.special_defense_iv, self.special_defense_ev, self.level)
        self.speed = calculate_stat(self.base_stats.speed, self.speed_iv, self.speed_ev, self.level)

    def __str__(self) -> str:
        string = "Pokemon: " + self.name
        string += "\nBase stats: " + str(self.base_stats.get_base_stats())
        string += "\nMove set:"
        string += self.move_set.__str__()
        string += "\n\nStats:"
        string += "\nHP: " + str(self.hp) + "\t\t\tIV: " + str(self.hp_iv) + "\tEV: " + str(self.hp_ev)
        string += "\nAttack: "  + str(self.attack) + "\t\tIV: " + str(self.attack_iv) + "\tEV: " + str(self.attack_ev)
        string += "\nDefense: "  + str(self.defense) + "\t\tIV: " + str(self.defense_iv) + "\tEV: " + str(self.defense_ev)
        string += "\nSpecial attack: "  + str(self.special_attack) + "\tIV: " + str(self.special_attack_iv) + "\tEV: " + str(self.special_attack_ev)
        string += "\nSpecial defense: "  + str(self.special_defense) + "\tIV: " + str(self.special_defense_iv) + "\tEV: " + str(self.special_defense_ev)
        string += "\nSpeed: "  + str(self.speed) + "\t\tIV: " + str(self.speed_iv) + "\tEV: " + str(self.speed_ev)

        return string

class PokemonParty:
    def __init__(self, pokemons):
        self.pokemon_party = [None] * 6

        for i in range(len(pokemons)):
            self.pokemon_party[i] = pokemons[i]

    def get_leading_pokemon(self):
        return self.pokemon_party[0]