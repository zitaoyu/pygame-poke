import json
import random
from typing import List
from util import *
from data_downloader import POKEDEX_DATA_PATH, MOVES_DATA_PATH


class Pokedex:
    def __init__(self):
        with open(POKEDEX_DATA_PATH, 'r') as pokedex_data:
            self.__pokedex = json.load(pokedex_data)["pokedex"]

    def get(self, id):
        return self.__pokedex[id - 1]


class MovesBank:
    def __init__(self):
        with open(MOVES_DATA_PATH, 'r') as moves_data:
            self.__moves_data = json.load(moves_data)["moves"]

    def get(self, id):
        return self.__moves_data[id - 1]


POKEDEX = Pokedex()
MOVES = MovesBank()


class Type(Enum):
    NORMAL = "normal"
    FIRE = "fire"
    WATER = "water"
    GRASS = "grass"
    ELECTRIC = "electric"
    ICE = "ice"
    FIGHTING = "fighting"
    POISON = "poison"
    GROUND = "ground"
    FLYING = "flying"
    PSYCHIC = "psychic"
    BUG = "bug"
    ROCK = "rock"
    GHOST = "ghost"
    DARK = "dark"
    DRAGON = "dragon"
    STEEL = "steel"
    FAIRY = "fairy"

    def type_chart(self, attack_type, defense_type):
        pass


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
        self.current_pp = self.pp
        self.priority = data["priority"]
        self.target = data["target"]
        self.type = Type(data["type"])

        self.stat_change = []
        for change in data["stat_changes"]:
            self.stat_change.append({
                "change": change["change"],
                "stat": change["stat"]["name"]
            })


class MoveSet:
    def __init__(self, moves: List[Move]):
        self.__moves: List[Move] = [None] * 4

        for i in range(len(moves)):
            self.__moves[i] = moves[i]

    def get_move_with_index(self, index) -> Move:
        return self.__moves[index]

    def replace_move(self, move: Move, index) -> None:
        self.__moves[index] = move

    def get_size(self) -> int:
        size = 0
        for move in self.__moves:
            if move is not None:
                size += 1
        return size

    def get_move_names(self) -> list[str]:
        names = []
        for move in self.__moves:
            if move is not None:
                names.append(move.name)
        return names

    def __str__(self) -> str:
        string = ""
        for move in self.__moves:
            string += "\n\nName: " + move.name + "\nPower: " + str(move.power) + "\nAccuracy:" + str(
                move.accuracy) + "\nType: " + move.type.value + "\nPP: " + str(
                move.pp) + "\nEffect: " + move.short_effect
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

    def get_default_moveset(self, level=1) -> MoveSet:
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
                self.special_attack = stat["base_stat"]

            elif stat["name"] == "special-defense":
                self.special_defense = stat["base_stat"]

            elif stat["name"] == "speed":
                self.speed = stat["base_stat"]

    def get_base_stats(self):
        return {
            "hp": self.hp,
            "attack": self.attack,
            "defense": self.defense,
            "special-attack": self.special_attack,
            "special-defense": self.special_defense,
            "speed": self.speed
        }


class Pokemon:
    def __init__(self, id, level=1):
        self.id: int = id
        self.level: int = level

        # retrieve pokemon data
        data = POKEDEX.get(id)
        self.name: str = data["name"]
        self.nickname: str = self.name.capitalize()
        self.types: List[Type] = []
        for pk_type in data["types"]:
            self.types.append(Type(pk_type))
        self.base_stats: BaseStats = BaseStats(data["stats"])

        # moves
        self.move_pool: MovePool = MovePool(data["moves"])
        self.move_set: MoveSet = self.move_pool.get_default_moveset(self.level)

        # IVs and EVs initialization
        self.__generate_ivs()
        self.hp_ev: int = 0
        self.attack_ev: int = 0
        self.defense_ev: int = 0
        self.special_attack_ev: int = 0
        self.special_defense_ev: int = 0
        self.speed_ev: int = 0

        # calculate stats
        self.__update_stats()
        self.current_hp: int = self.hp
        self.fainted: bool = False

    def __generate_ivs(self):
        ivs = random.sample(range(32), 6)
        self.hp_iv = ivs[0]
        self.attack_iv = ivs[1]
        self.defense_iv = ivs[2]
        self.special_attack_iv = ivs[3]
        self.special_defense_iv = ivs[4]
        self.speed_iv = ivs[5]

    @staticmethod
    def __calculate_hp(base: int, iv: int, ev: int, level: int) -> int:
        return int(((2 * base + iv + (ev / 4)) * level / 100) + level + 10)

    @staticmethod
    def __calculate_stat(base: int, iv: int, ev: int, level: int, nature=1) -> int:
        return int((((2 * base + iv + (ev / 4)) * level / 100) + 5) * nature)

    def __update_stats(self):
        # formula source: https://bulbapedia.bulbagarden.net/wiki/Stat
        # calculator: https://pycosites.com/pkmn/stat.php
        # 
        #       | (2 * Base + IV + [EV / 4]) * Level | 
        # HP =  |____________________________________| + Level + 10
        #       |                100                 |
        self.hp = self.__calculate_hp(self.base_stats.hp, self.hp_iv, self.hp_ev, self.level)
        self.attack = self.__calculate_stat(self.base_stats.attack, self.attack_iv, self.attack_ev, self.level)
        self.defense = self.__calculate_stat(self.base_stats.defense, self.defense_iv, self.defense_ev, self.level)
        self.special_attack = self.__calculate_stat(self.base_stats.special_attack, self.special_attack_iv,
                                                    self.special_attack_ev, self.level)
        self.special_defense = self.__calculate_stat(self.base_stats.special_defense, self.special_defense_iv,
                                                     self.special_defense_ev, self.level)
        self.speed = self.__calculate_stat(self.base_stats.speed, self.speed_iv, self.speed_ev, self.level)

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0
            self.fainted = True

    def fully_heal(self):
        self.current_hp = self.hp
        self.fainted = False

    def __str__(self) -> str:
        string = "Pokemon: " + self.name
        string += "\nBase stats: " + str(self.base_stats.get_base_stats())
        string += "\nMove set:"
        string += self.move_set.__str__()
        string += "\n\nStats:"
        string += "\nHP: " + str(self.hp) + "\t\t\tIV: " + str(self.hp_iv) + "\tEV: " + str(self.hp_ev)
        string += "\nAttack: " + str(self.attack) + "\t\tIV: " + str(self.attack_iv) + "\tEV: " + str(self.attack_ev)
        string += "\nDefense: " + str(self.defense) + "\t\tIV: " + str(self.defense_iv) + "\tEV: " + str(
            self.defense_ev)
        string += "\nSpecial attack: " + str(self.special_attack) + "\tIV: " + str(
            self.special_attack_iv) + "\tEV: " + str(self.special_attack_ev)
        string += "\nSpecial defense: " + str(self.special_defense) + "\tIV: " + str(
            self.special_defense_iv) + "\tEV: " + str(self.special_defense_ev)
        string += "\nSpeed: " + str(self.speed) + "\t\tIV: " + str(self.speed_iv) + "\tEV: " + str(self.speed_ev)

        return string


class PokemonParty:
    def __init__(self, pokemons: List[Pokemon]):
        self.pokemon_party: List[Pokemon] = [None] * 6

        for i in range(len(pokemons)):
            self.pokemon_party[i] = pokemons[i]

    def get_leading_pokemon(self) -> Pokemon:
        return self.pokemon_party[0]

    def add_to_party(self, pokemon: Pokemon):
        is_added = False
        for i in range(len(self.pokemon_party)):
            if self.pokemon_party[i] is None:
                self.pokemon_party[i] = pokemon
                is_added = True
        return is_added
