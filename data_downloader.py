import requests
import json
import os
import shutil

POKEMON_DATA_URL = "https://pokeapi.co/api/v2/pokemon/?limit=10000"
MOVES_DATA_URL = "https://pokeapi.co/api/v2/move?limit=100000"

DATA_FOLDER_PATH = './data/'
POKEDEX_DATA_PATH = DATA_FOLDER_PATH + 'pokedex.json'
MOVES_DATA_PATH = DATA_FOLDER_PATH + 'moves.json'
POKEMON_SPRITES_FOLDER_PATH = './assets/pokemon/'


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def info_log(string):
    print("[Info]: " + string)


'''
Load pokedex minimal data in to a JSON file
'''


def download_pokedex_data_to_json():
    if os.path.exists(POKEDEX_DATA_PATH):
        response = input(POKEDEX_DATA_PATH + ' exists, override file? [y/n]: ')
        if response != 'y':
            return

    json_object = {
        "pokedex": []
    }
    pokedex = json_object["pokedex"]
    pokemon_list = requests.get(POKEMON_DATA_URL).json()["results"]

    for i in range(0, len(pokemon_list)):
        pokemon_data = requests.get(pokemon_list[i]["url"]).json()
        moves = []
        for move in pokemon_data["moves"]:
            version_group_details = move["version_group_details"]
            version_group = None
            last_version_group = None
            if len(version_group_details) > 0:
                last_version_group = version_group_details[len(version_group_details) - 1]
                version_group = last_version_group["version_group"]["name"]
            pk_id = int(move["move"]["url"].split('/')[-2])
            moves.append({
                "id": pk_id,
                "name": move["move"]["name"],
                "level_learned_at": last_version_group["level_learned_at"],
                "move_learn_method": last_version_group["move_learn_method"]["name"],
                "version_group": version_group
            })

        stats = []
        for stat in pokemon_data["stats"]:
            stats.append({
                "base_stat": stat["base_stat"],
                "effort": stat["effort"],
                "name": stat["stat"]["name"]
            })

        types = []
        for pk_type in pokemon_data["types"]:
            types.append(pk_type["type"]["name"])
        pk_id = pokemon_data["id"]
        name = pokemon_data["name"]
        pk_data = {
            "id": pk_id,
            "name": name,
            "moves": moves,
            "stats": stats,
            "types": types
        }
        pokedex.append(pk_data)
        info_log("Loaded pekemon #" + str(pk_id) + ", name: " + name)

    json_object = json.dumps(json_object, indent=4)
    with open(POKEDEX_DATA_PATH, "w") as outfile:
        outfile.write(json_object)
    info_log("Wrote pokedex data to " + POKEDEX_DATA_PATH + " successfully!")


'''
Load moves data into a JSON file
'''


def download_moves_data_to_json():
    if os.path.exists(MOVES_DATA_PATH):
        response = input(MOVES_DATA_PATH + ' exists, override file? [y/n]: ')
        if response != 'y':
            return

    json_object = {
        "moves": []
    }
    moves = json_object["moves"]
    move_list = requests.get(MOVES_DATA_URL).json()["results"]

    for i in range(0, len(move_list)):
        move_data = requests.get(move_list[i]["url"]).json()
        effect = None
        short_effect = None
        if len(move_data["effect_entries"]) > 0:
            last_effect_entry = move_data["effect_entries"][len(move_data["effect_entries"]) - 1]
            effect = last_effect_entry["effect"]
            short_effect = last_effect_entry["short_effect"]

        move_simple_data = {
            "accuracy": move_data["accuracy"],
            "damage_class": move_data["damage_class"]["name"],
            "effect_chance": move_data["effect_chance"],
            "effect_entries": {
                "effect": effect,
                "short_effect": short_effect
            },
            "id": move_data["id"],
            "name": move_data["name"],
            "power": move_data["power"],
            "pp": move_data["pp"],
            "priority": move_data["priority"],
            "stat_changes": move_data["stat_changes"],
            "target": move_data["target"]["name"],
            "type": move_data["type"]["name"]
        }
        moves.append(move_simple_data)
        info_log("Loaded move #" + str(i) + ", name: " + move_data["name"])

    json_object = json.dumps(json_object, indent=4)
    with open(MOVES_DATA_PATH, "w") as outfile:
        outfile.write(json_object)
        info_log("Wrote moves data to " + MOVES_DATA_PATH + " successfully!")


def download_pokemon_sprites():
    if os.path.exists(POKEMON_SPRITES_FOLDER_PATH):
        response = input(POKEMON_SPRITES_FOLDER_PATH + ' exists, re-download sprites? [y/n]: ')
        if response != 'y':
            return
    create_folder(POKEMON_SPRITES_FOLDER_PATH)

    # helper function to download image with url
    def download_sprite(url, file_name):
        if os.path.exists(file_name):
            return
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            info_log('image successfully Downloaded: ' + file_name)
        else:
            info_log('image Could not be retrieved')

    pokemon_list = requests.get(POKEMON_DATA_URL).json()["results"]

    for i in range(0, len(pokemon_list)):
        pokemon_data = requests.get(pokemon_list[i]["url"]).json()
        pk_id = pokemon_data["id"]
        sprites = pokemon_data["sprites"]
        front_sprite_url = sprites["front_default"]
        back_sprite_url = sprites["back_default"]
        if front_sprite_url is not None:
            download_sprite(front_sprite_url,
                            POKEMON_SPRITES_FOLDER_PATH + str(pk_id) + '_front.png')
        if back_sprite_url is not None:
            download_sprite(back_sprite_url,
                            POKEMON_SPRITES_FOLDER_PATH + str(pk_id) + '_back.png')


def main():
    create_folder(DATA_FOLDER_PATH)
    download_pokedex_data_to_json()
    download_moves_data_to_json()
    download_pokemon_sprites()


if __name__ == "__main__":
    main()
