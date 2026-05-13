import re
import time

from config import LOG_PATH

class LogReader:

    def __init__(self, overlay):

        self.overlay = overlay
        self.players = set()
        self.player_pattern = re.compile(
            r"Name:\s*([ -~]+?),"
        )
        self.last_player_time = None
        self.players_printed = False
        self.PLAYER_TIMEOUT = 2
        self.file = open(
            LOG_PATH,
            "r",
            encoding="utf-8",
            errors="ignore"
        )

        self.file.seek(0, 2)

    def update_overlay(self):
        where = self.file.tell()
        line = self.file.readline()
  
        if not line:
            if (
                self.players
                and not self.players_printed
                and self.last_player_time
                and time.time() - self.last_player_time > self.PLAYER_TIMEOUT
            ):
                print("\n=== JUGADORES DETECTADOS ===")
                for player in self.players:
                    print("-", player)
                # actualizar overlay
                self.overlay.update_players(
                    list(self.players)
                )
                self.players_printed = True
            self.file.seek(where)
            return

        if "BMPGame::setGameState -- state [0]" in line:
            print("\n=== NUEVA PARTIDA ===")
            self.players.clear()
            self.last_player_time = None
            self.players_printed = False
            return

        match = self.player_pattern.search(line)

        if match:
            player = match.group(1)
            self.players.add(player)
            self.last_player_time = time.time()
            self.players_printed = False