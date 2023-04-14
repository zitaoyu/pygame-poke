from pokemon import *


class BattleManager:
    def __init__(self, my_pokemon_party: PokemonParty, opponent_pokemon_party: PokemonParty) -> None:
        self.my_pokemon_party = my_pokemon_party
        self.opponent_pokemon_party = opponent_pokemon_party

        self.my_battling_pokemon = self.my_pokemon_party.get_leading_pokemon()
        self.my_battling_pokemon_attack_stage = 0
        self.my_battling_pokemon_defense_stage = 0
        self.my_battling_pokemon_special_attack_stage = 0
        self.my_battling_pokemon_special_defense_stage = 0
        self.my_battling_pokemon_special_speed_stage = 0
        self.my_battling_pokemon_critical_chance_stage = 0

        self.opponent_battling_pokemon = self.opponent_pokemon_party.get_leading_pokemon()
        self.opponent_battling_pokemon_attack_stage = 0
        self.opponent_battling_pokemon_defense_stage = 0
        self.opponent_battling_pokemon_special_attack_stage = 0
        self.opponent_battling_pokemon_special_defense_stage = 0
        self.opponent_battling_pokemon_special_speed_stage = 0
        self.opponent_battling_pokemon_critical_chance_stage = 0

        self.weather = None
        self.terrain = None

        self.messages = []

    @staticmethod
    def _calculate_damage(level, power, attack, defense, targets, weather, critical, random_val, stab, pk_type,
                          burn) -> int:
        #
        # Damage formula: Gen V onward from https://bulbapedia.bulbagarden.net/wiki/Damage
        #
        # these value will always be 1 since we won't run into these cases
        pb = 1
        other = 1
        z_move = 1
        tera_shield = 1
        damage = int(
            (((2 * level / 5 + 2) * power * attack / defense) / 50 + 2) *
            targets * pb * weather * critical * random_val * stab * pk_type * burn * other * z_move * tera_shield
        )
        return damage

    def pokemon_use_move(self, move_index: int, attacker: Pokemon, defender: Pokemon):
        self.messages.append(
            attacker.nickname + " used " + attacker.move_set.get_move_with_index(move_index).name + "!")
        move = attacker.move_set.get_move_with_index(move_index)
        power = move.power
        if power:
            level = attacker.level
            if move.damage_class == "physical":
                attack = attacker.attack
                defense = defender.defense
            else:
                attack = attacker.special_attack
                defense = defender.special_defense
            targets = 1
            weather = 1

            # calculate type
            pk_type = 1
            if pk_type == 0.5:
                self.messages.append("Not very effective!")
            elif pk_type == 2:
                self.messages.append("Super effective!")

            # calculate critical chance
            critical = 1
            roll = random.random()
            chance = 1 / 24
            if attacker is self.my_battling_pokemon:
                critical_chance_stage = self.my_battling_pokemon_critical_chance_stage
            else:
                critical_chance_stage = self.opponent_battling_pokemon_critical_chance_stage
            if critical_chance_stage == 1:
                chance = 1 / 8
            elif critical_chance_stage == 2:
                chance = 1 / 2
            elif critical_chance_stage >= 3:
                chance = 1
            if chance >= roll:
                critical = 1.5
                self.messages.append("Critical hit!")

            random_val = random.uniform(0.85, 1)
            if move.type in attacker.types:
                stab = 1.5
            else:
                stab = 1
            burn = 1

            damage = self._calculate_damage(level, power, attack, defense, targets, weather, critical, random_val,
                                            stab, pk_type, burn)
            defender.take_damage(damage)
            if defender.fainted:
                self.messages.append(defender.nickname + " has fainted.")

    def battle(self, move_index):
        if self.my_battling_pokemon.speed > self.opponent_battling_pokemon.speed:
            self.pokemon_use_move(move_index, self.my_battling_pokemon, self.opponent_battling_pokemon)
            if self.opponent_battling_pokemon.fainted:
                return
            self.opponent_battling_pokemon_use_move()
        elif self.my_battling_pokemon.speed < self.opponent_battling_pokemon.speed:
            self.opponent_battling_pokemon_use_move()
            if self.my_battling_pokemon.fainted:
                return
            self.pokemon_use_move(move_index, self.my_battling_pokemon, self.opponent_battling_pokemon)
        # speed tie
        elif self.my_battling_pokemon.speed == self.opponent_battling_pokemon.speed:
            random_float = random.random()
            if random_float > 0.50:
                self.pokemon_use_move(move_index, self.my_battling_pokemon, self.opponent_battling_pokemon)
                if self.opponent_battling_pokemon.fainted:
                    return
                self.opponent_battling_pokemon_use_move()
            else:
                self.opponent_battling_pokemon_use_move()
                if self.my_battling_pokemon.fainted:
                    return
                self.pokemon_use_move(move_index, self.my_battling_pokemon, self.opponent_battling_pokemon)

    def my_battling_pokemon_use_move(self, move_index: int):
        self.pokemon_use_move(move_index, self.my_battling_pokemon, self.opponent_battling_pokemon)

    def opponent_battling_pokemon_use_move(self):
        move_index = random.randint(1, self.opponent_battling_pokemon.move_set.get_size()) - 1
        self.pokemon_use_move(move_index, self.opponent_battling_pokemon, self.my_battling_pokemon)

    def get_next_message(self):
        if len(self.messages) == 0:
            return None
        return self.messages.pop(0)
