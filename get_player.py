import time
import re

from config import LOG_PATH

players = set()

player_pattern = re.compile(r"Name:\s*([ -~]+?),")

last_player_time = None
players_printed = False

PLAYER_TIMEOUT = 2  # segundos

with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as file:
    file.seek(0, 2)

    while True:
        where = file.tell()
        line = file.readline()

        if not line:
            # Si ya pasó tiempo sin nuevos jugadores
            if (
                players
                and not players_printed
                and last_player_time
                and time.time() - last_player_time > PLAYER_TIMEOUT
            ):
                print("\n=== JUGADORES DE LA PARTIDA ===")

                for player in players:
                    print(f"- {player}")

                players_printed = True

            time.sleep(0.1)
            file.seek(where)
            continue

        # Nueva partida
        if "BMPGame::setGameState -- state [0]" in line:
            players.clear()
            last_player_time = None
            players_printed = False

            print("\n=== NUEVA PARTIDA ===")

            continue

        # Buscar jugador
        match = player_pattern.search(line)

        if match:
            player = match.group(1)

            if player not in players:
                players.add(player)

            last_player_time = time.time()
            players_printed = False