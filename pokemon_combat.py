import os
import random
from pokeload import get_all_pokemons


def get_player_profile(pokemon_list):
    return {
        "player_name": input("¿Cual es tu nombre?: "),
        "pokemon_inventory": [random.choice(pokemon_list) for a in range(3)],
        "combats": 0,
        "health_potion": 0
    }


def any_player_pokemon_live(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0


def choose_pokemon(player_profile):
    chosen = None

    while not chosen:
        print("Estos son tus pokemones:\n")
        for index in range(len(player_profile["pokemon_inventory"])):
            print("{} - {}".format(index, get_pokemon_info(player_profile["pokemon_inventory"][index])))

        try:
            return player_profile["pokemon_inventory"][int(str.lower(input("¿Cual eliges?: \n")))]
        except (ValueError, IndexError):
            print("No tienes ese pokemon en tu inventario...")


def choose_attack(attacks):
    chosen_attack = None

    while chosen_attack is None:
        for attack in attacks:
            print("*{}".format(get_attack_info(attack)))
        chosen_attack = int(input("\n¿Con que quieres atacar?(0-4): "))
    try:
        return attacks[chosen_attack]
    except (TypeError, IndexError, ValueError):
        print("\nEse ataque no esta disponible para ese pokemon...")


def get_attack_info(pokemon_attack):
    return "{} | type: {} | damage: {}".format(pokemon_attack["name"],
                                               pokemon_attack["type"],
                                               pokemon_attack["damage"])


def get_pokemon_info(pokemon):
    return "{} | type: {} | hp {}/{} ".format("".join(pokemon["name"]),
                                              "/".join(pokemon["type"]),
                                              pokemon["current_health"],
                                              pokemon["base_health"])


def get_player_info(player_profile):
    return "{} | Combates: {} | Pociones de Vida: {}\n\n".format(player_profile["player_name"],
                                                                 player_profile["combats"],
                                                                 player_profile["health_potion"])


def player_attack(enemy_pokemon, player_pokemon, players_attacks):
    chosen_attack = choose_attack(players_attacks)
    enemy_pokemon["current_health"] -= chosen_attack["damage"]
    print("\n{} ataca con {}".format(player_pokemon["name"], chosen_attack["name"]))
    print("{} recibe {} de daño\n".format(enemy_pokemon["name"], chosen_attack["damage"]))


def enemy_attack(enemy_pokemon, player_pokemon):
    attack = random.choice(enemy_pokemon["attacks"])
    player_pokemon["current_health"] -= attack["damage"]
    print("\n{} ataca con {}".format(enemy_pokemon["name"], attack["name"]))
    print("{} recibe {} de daño\n".format(player_pokemon["name"], attack["damage"]))


def generate_life_bars(enemy_pokemon, player_pokemon):
    enemy_bars = int(enemy_pokemon["current_health"] * 10 / enemy_pokemon["base_health"])
    print("{}: [{}{}] [{}/{}]".format("".join(enemy_pokemon["name"]), "#" * enemy_bars,
                                      " " * (10 - enemy_bars), enemy_pokemon["current_health"],
                                      enemy_pokemon["base_health"]))

    player_bars = int(player_pokemon["current_health"] * 10 / player_pokemon["base_health"])
    print("{}: [{}{}] [{}/{}]\n".format("".join(player_pokemon["name"]), "#" * player_bars,
                                        " " * (10 - player_bars), player_pokemon["current_health"],
                                        player_pokemon["base_health"]))


def fight(player_profile, enemy_pokemon):
    player_pokemon = choose_pokemon(player_profile)
    player_choice(player_profile, player_pokemon)
    input("Presiona [ENTER] para continuar...")
    os.system("cls")
    print("\n\n---NUEVO COMBATE---\n\n")
    print(get_player_info(player_profile))
    print("Muy bien {} este es el proximo combate:".format(player_profile["player_name"]))
    print("\n{} VS {}\n".format(str.upper(get_pokemon_info(player_pokemon)),
                                str.upper(get_pokemon_info(enemy_pokemon))))
    input("Presiona [ENTER] para continuar...\n")
    os.system("cls")

    player_attacks = [random.choice(player_pokemon["attacks"]) for a in range(5)]

    while any_player_pokemon_live(player_profile) and enemy_pokemon["current_health"] > 0:

        print("Es turno de {}\n".format(player_profile["player_name"]))
        print(get_player_info(player_profile))
        generate_life_bars(enemy_pokemon, player_pokemon)
        player_attack(enemy_pokemon, player_pokemon, player_attacks)
        input("Presiona[ENTER] para continuar...")
        os.system("cls")

        if enemy_pokemon["current_health"] <= 0:
            enemy_pokemon["current_health"] = 0
            print("\n--HAS GANADO ESTE COMBATE, FELICIDADES--\n")
            input("Presiona [ENTER] para pelear el siguiente combate...")
            break

        print("Es turno del rival\n")
        print(get_player_info(player_profile))
        generate_life_bars(enemy_pokemon, player_pokemon)
        enemy_attack(enemy_pokemon, player_pokemon)
        input("Presiona[ENTER] para continuar...")
        os.system("cls")

        if player_pokemon["current_health"] <= 0:
            player_pokemon["current_health"] = 0
            print("Ha ganado {}".format(enemy_pokemon["name"]))
            player_profile["pokemon_inventory"].remove(player_pokemon)
            print("{} perdió, {} fue removido de tu inventario".format(player_pokemon["name"], player_pokemon["name"]))
            break

    print("\n\n---FIN DEL COMBATE---\n\n")


def player_choice(player_profile, chosen_pokemon):
    choice = None

    while not choice:
        choice = input(
            "Antes de cualquier cosa, deseas ingerir alguna [P]ocion de vida para tu pokemon o deseas iniciar\n"
            "el [C]ombate?: ")

        if choice == "p" or choice == "P":
            if player_profile["health_potion"] <= 0:
                print("No tienes pociones de vida en tu inventario...\n")
            else:
                chosen_pokemon["current_health"] += 300
                player_profile["health_potion"] -= 1
                print("{} ha sido curado, la vida actual de {} es de {}".format("".join(chosen_pokemon["name"]),
                                                                                "".join(chosen_pokemon["name"]),
                                                                                chosen_pokemon["current_health"]))
            break
        elif choice == "c" or choice == "C":
            print("¡Muy bien {} a pelear!".format(player_profile["player_name"]))
            break
        else:
            print("{} tienes que esocoger una opcion para poder continar...\n".format(str.capitalize(
                player_profile["player_name"])))


def raffle(player_profile):
    print("¡Antes de continuar haremos una rifa para ganar una pocion de vida para tu pokemon!\n")
    potion = random.randint(1, 2)
    input("Presiona [ENTER] para continuar...")

    if potion == 1:
        print("{} te has ganado una pocion de vida, FELICIDADES!!!\n".format(player_profile["player_name"]))
        player_profile["health_potion"] += 1
    else:
        print("Lo siento {} lastimosamente no te tocó la pocion de vida, vuelve a intentarlo en la siguiente ronda!\n"
              .format(player_profile["player_name"]))


def main():
    pokemon_list = get_all_pokemons()
    player_profile = get_player_profile(pokemon_list)
    os.system("cls")

    print("\n\n--- MUY BIEN {} BIENVENIDO A ESTE COMBATE DE SUPERVIVENCIA POKEMON---\n\n".format(
        str.upper(player_profile["player_name"])))

    print("\nAntes de iniciar la partida aqui van un par de instrucciones:\n"
          "* Para escoger los pokemones y los taques de los mismos tienes que usar os indices de uno al cero.\n"
          "* Tendras tres pokemones los cuales podras curar despues antes de cada combate.\n"
          "* Si pierdes un combate, el pokemon con el cual estaas luchando será removido de tu inventario.\n"
          "* Una vez el numero de pokemones en tu inventario sea igual a 0 la partida se terminará.\n"
          "* Al final de cada partida tendras la cantidad de combates que ganaste.")

    input("\nSi entendiste todo a la perfecion presiona [ENTER] para continuar...")
    os.system("cls")

    print("\n¡MUY BIEN {} ME ENCANTA ESA ACTITUD!\n".format(str.upper(player_profile["player_name"])))

    print("Estos son tus pokemons:\n")
    for pokemon in player_profile["pokemon_inventory"]:
        print("{}".format(get_pokemon_info(pokemon)))

    input("\nSi estas listo para pelear presiona [ENTER]...\n")
    os.system("cls")
    print("Muy bien {} empezemos...".format(player_profile["player_name"]))

    while any_player_pokemon_live(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)
        raffle(player_profile)

    print("Has perdido, todos tus pokemones han sido derrotados ganaste {} combates".format(player_profile["combats"]))
    resume = input("¿Deseas repetir la partida? [S/N]: ")

    if resume == "s" or resume == "S":
        main()
    elif resume == "n" or resume == "N":
        print("\nLo entiendo, gracias por jugar de cualquier modo :D")
    else:
        print("\nVoy a tomar eso como un no jajaja. Adiós bro")


if __name__ == "__main__":
    main()