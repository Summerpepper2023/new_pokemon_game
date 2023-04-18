import pickle
import re
from pprint import pprint

from requests_html import HTMLSession

pokemon_base = {
    "name": "",
    "current_health": 1000,
    "base_health": 1000,
    "type": [],
    "attacks": [],
    "level": 1,
    "current_experience": 0

}
BASE_URL = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_pokemon&pk="


def get_name(name):
    patterns = ["^([A-Za-z]+)"]
    for pattern in patterns:
        try:
            pokemon_name = re.findall(pattern, name)
            return pokemon_name
        except IndexError:
            print("No se ha encotrado nombre...")


def get_pokemon(index):
    url = "{}{}".format(BASE_URL, index)
    session = HTMLSession()
    pokemon_page = session.get(url)

    new_pokemon = pokemon_base.copy()
    name = pokemon_page.html.find(".mini",first=True).text
    pokemon_name = get_name(name)

    new_pokemon["name"] = pokemon_name
    new_pokemon["type"] = []
    new_pokemon["attacks"] = []

    for img in pokemon_page.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("img"):
        new_pokemon["type"].append(img.attrs["alt"])

    for attack_item in pokemon_page.html.find(".pkmain")[-1].find("tr .check3"):
        attack = {
            "name": attack_item.find("td", first=True).find("a", first=True).text,
            "type": attack_item.find("td")[1].find("img", first=True).attrs["alt"],
            "damage": int(attack_item.find("td")[3].text.replace("--", "0").replace("%", "")),
        }
        new_pokemon["attacks"].append(attack)

    return new_pokemon


def get_all_pokemons():
    try:
        print("\nCargando base de datos de pokemons...")
        with open("pokefile.pkl", "rb") as pokefile:
            all_pokemons = pickle.load(pokefile)
        print("Base de datos cargada...")

    except FileNotFoundError:
        print("Base de datos no encontrada...")
        all_pokemons = []
        print("Accediendo a la base de datos...")

        print("[" ,end="")
        for index in range(150):
            all_pokemons.append(get_pokemon(index+1))
            print("#", end="")
        print("]")
        with open("pokefile.pkl", "wb") as pokefile:
            pickle.dump(all_pokemons, pokefile)
        print("Base de datos descargada...")

    return all_pokemons


def main():
    print(get_all_pokemons())


if __name__ == "__main__":
    main()