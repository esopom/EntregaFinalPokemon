import random
from CursoPython.Entrega_final.poke_load import get_all_pokemons


# Función para crear el perfil del jugador
def get_player_profile(pokemon_list):
    return {
        "player_name": input("\nCuál es tu nombre? "),
        "pokemon_inventory": [add_experience_to_pokemon(random.choice(pokemon_list)) for _ in range(3)],
        "combats": 0,
        "pokeballs": 5,
        "health_potion": 2,
    }


# Añade la experiencia inicial a un Pokémon
def add_experience_to_pokemon(pokemon):
    pokemon["current_experience"] = 0
    return pokemon


# Verifica si algún Pokémon del jugador aún tiene vida
def any_player_pokemon_lives(player_profile):
    return any(pokemon["current_health"] > 0 for pokemon in player_profile["pokemon_inventory"])


# Permite al jugador elegir un Pokémon para la batalla
def choose_pokemon(player_profile):
    while True:
        print("Elige con qué pokemon lucharás: ")
        for index, pokemon in enumerate(player_profile["pokemon_inventory"]):
            print(f"{index} - {get_pokemon_info(pokemon)}")
        try:
            choice = int(input("¿Cuál eliges? "))
            if 0 <= choice < len(player_profile["pokemon_inventory"]):
                if player_profile["pokemon_inventory"][choice]["current_health"] > 0:
                    return player_profile["pokemon_inventory"][choice]
                else:
                    print("Este Pokémon no tiene salud. Elige otro.")
            else:
                print("Elección inválida")
        except ValueError:
            print("Por favor, introduce un número válido.")


# Obtiene la información de un ataque
def get_attack_info(pokemon_attack):
    return f"{pokemon_attack['name']} | type: {pokemon_attack['type']} | damage: {pokemon_attack['damage']}"


# Obtiene la información de un Pokémon
def get_pokemon_info(pokemon):
    return f"{pokemon['name']} | lvl {pokemon['level']} | hp {pokemon['current_health']}/{pokemon['base_health']} | exp {pokemon['current_experience']}/20"


# Permite al jugador elegir un ataque
def get_attack(attacks):
    while True:
        for i, attack in enumerate(attacks, 1):
            print(f"{i} - {get_attack_info(attack)}")
        try:
            choose_attack = int(input("Elige un ataque (1-5): "))
            if 1 <= choose_attack <= len(attacks):
                return attacks[choose_attack - 1]
            else:
                print("Elección inválida. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Intenta de nuevo.")


# Crea una representación gráfica de la salud del Pokémon
def get_graphic_health(pokemon):
    health_percentage = pokemon["current_health"] / pokemon["base_health"]
    return "#" * int(20 * health_percentage)


# Maneja el ataque del jugador
def player_attack(player_pokemon, enemy_pokemon, player_attacks):
    print(
        f"Vida de {player_pokemon['name']} = [{get_graphic_health(player_pokemon)}] ({player_pokemon['current_health']}/{player_pokemon['base_health']})")
    print(
        f"Vida de {enemy_pokemon['name']} = [{get_graphic_health(enemy_pokemon)}] ({enemy_pokemon['current_health']}/{enemy_pokemon['base_health']})")

    chosen_attack = get_attack(player_attacks)
    damage = chosen_attack["damage"]
    enemy_pokemon["current_health"] = max(0, enemy_pokemon["current_health"] - damage)

    print(f"\n{player_pokemon['name']} ataca con {chosen_attack['name']}")
    print(f"{enemy_pokemon['name']} recibe {damage} de daño\n")


# Maneja el ataque del enemigo
def enemy_attack(enemy_pokemon, player_pokemon):
    print(
        f"Vida de {player_pokemon['name']} = [{get_graphic_health(player_pokemon)}] ({player_pokemon['current_health']}/{player_pokemon['base_health']})")
    print(
        f"Vida de {enemy_pokemon['name']} = [{get_graphic_health(enemy_pokemon)}] ({enemy_pokemon['current_health']}/{enemy_pokemon['base_health']})")
    input("(Presiona enter para continuar con el combate)")

    attack = random.choice(enemy_pokemon["attacks"])
    damage = attack["damage"]
    player_pokemon["current_health"] = max(0, player_pokemon["current_health"] - damage)

    print(f"\n{enemy_pokemon['name']} ataca con {attack['name']}")
    print(f"{player_pokemon['name']} recibe {damage} de daño\n")

    print(
        f"Vida de {player_pokemon['name']} = [{get_graphic_health(player_pokemon)}] ({player_pokemon['current_health']}/{player_pokemon['base_health']})")
    print(
        f"Vida de {enemy_pokemon['name']} = [{get_graphic_health(enemy_pokemon)}] ({enemy_pokemon['current_health']}/{enemy_pokemon['base_health']})")
    input("(Presiona enter para continuar con el combate)")


# Asigna experiencia a los Pokémon después de la batalla
def assign_experience(attack_history):
    for pokemon in attack_history:
        points = random.randint(1, 5)
        pokemon["current_experience"] += points

        while pokemon["current_experience"] >= 20:
            pokemon["current_experience"] -= 20
            pokemon["level"] += 1
            pokemon["base_health"] += 5
            pokemon["current_health"] = pokemon["base_health"]
            print(f"¡Tu pokemon {pokemon['name']} ha subido al nivel {pokemon['level']}!")


# Cura a un Pokémon usando una poción
def cure_pokemon(pokemon, player_profile):
    if player_profile["health_potion"] > 0:
        pokemon["current_health"] = pokemon["base_health"]
        player_profile["health_potion"] -= 1
        print(f"{pokemon['name']} ha sido curado completamente. Te quedan {player_profile['health_potion']} pociones.")
    else:
        print("No te quedan pociones de curación")


# Intenta capturar al Pokémon enemigo
def capture_pokemon_with_pokeball(enemy_pokemon, player_profile):
    if player_profile["pokeballs"] > 0:
        player_profile["pokeballs"] -= 1
        capture_chance = (1 - (enemy_pokemon["current_health"] / enemy_pokemon["base_health"])) * 0.7
        if random.random() < capture_chance:
            captured_pokemon = add_experience_to_pokemon(enemy_pokemon.copy())
            player_profile["pokemon_inventory"].append(captured_pokemon)
            print(f"¡Has capturado a {enemy_pokemon['name']}!")
            return True
        else:
            print(f"¡Oh no! {enemy_pokemon['name']} ha escapado de la pokeball.")
        print(f"Te quedan {player_profile['pokeballs']} pokeballs.")
    else:
        print("No te quedan pokeballs.")
    return False


# Maneja una batalla completa
def fight(player_profile, enemy_pokemon):
    print("===== NUEVO COMBATE INICIADO =====")
    player_profile["combats"] += 1
    player_pokemon = choose_pokemon(player_profile)
    player_attacks = random.sample(player_pokemon["attacks"], min(5, len(player_pokemon["attacks"])))
    attack_history = []

    print(f"""
    +------------------------------------------------------------+
    |             |{player_pokemon['name']}| ha comenzado una batalla                  |
    |                           VS                               |
    |                        |{enemy_pokemon['name']}|                                |
    |                 (PULSA ENTER PARA CONTINUAR)               |
    +------------------------------------------------------------+""")
    input()

    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0:
        action = input("Qué deseas hacer: [A]tacar [P]okeball Poción de [V]ida [C]ambiar ").upper()
        if action == "A":
            player_attack(player_pokemon, enemy_pokemon, player_attacks)
            attack_history.append(player_pokemon)
            if enemy_pokemon["current_health"] > 0:
                enemy_attack(enemy_pokemon, player_pokemon)
        elif action == "V":
            cure_pokemon(player_pokemon, player_profile)
        elif action == "P":
            if capture_pokemon_with_pokeball(enemy_pokemon, player_profile):
                break
        elif action == "C":
            player_pokemon = choose_pokemon(player_profile)
        else:
            print("Acción inválida. Intenta de nuevo.")

        if player_pokemon["current_health"] == 0 and any_player_pokemon_lives(player_profile):
            print(f"{player_pokemon['name']} se ha debilitado. Elige otro Pokémon.")
            player_pokemon = choose_pokemon(player_profile)

    if enemy_pokemon["current_health"] == 0:
        print("¡Has ganado!")
        assign_experience(attack_history)

    print("===== FIN COMBATE =====")
    input("Presiona ENTER para continuar")


# Otorga un ítem aleatorio al jugador después de la batalla
def item_lottery(player_profile):
    item = random.choice(["pokeball", "health_potion"])
    quantity = random.randint(1, 3)

    if item == "pokeball":
        player_profile["pokeballs"] += quantity
        print(f"¡Has ganado {quantity} pokeball{'s' if quantity > 1 else ''}!")
    else:
        player_profile["health_potion"] += quantity
        print(f"¡Has ganado {quantity} poción{'es' if quantity > 1 else ''} de salud!")


# Función principal que ejecuta el juego
def main():
    pokemon_list = get_all_pokemons()
    print("===== Lista cargada =====")
    player_profile = get_player_profile(pokemon_list)

    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)
        item_lottery(player_profile)

    print(f"Has perdido en el combate número: {player_profile['combats']}")


if __name__ == "__main__":
    main()