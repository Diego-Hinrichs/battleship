from clases.utils import get_game, get_player
from clases.Game import Game
from clases.Player import Player
from clases.Server import Server
import readline, threading

class Console():

    def __init__(self, server: Server):
        self.server = server 

    def start(self):
        console_thread = threading.Thread(target=self.interactive_console, daemon=True)
        console_thread.start()

    def interactive_console(self):
        game: Game | None
        while True:
            command = input("").lower()
            if command:
                readline.add_history(command)
            if command == 'estado':
                player: Player
                stats = f"\nJugadores en línea: {len(self.server.online_players)}"
                stats += f"\nJuegos activos: {len(self.server.active_games)}"
                if len(self.server.active_games) > 0:
                    for game in self.server.active_games:
                        stats += f"\nid del juego: {game.game_id}"
                else:
                    stats += f"\nNo hay juegos activos"
                print(stats)

            elif command.startswith('juego '):
                game_id = command.split(' ')[1]
                game = get_game(self.server.active_games, game_id)
                print(game)

            elif command == 'juegos':
                stats = ""
                if len(self.server.active_games) > 0:
                    for game in self.server.active_games:
                        stats += f"\nJuego {game.game_id} - "
                        stats += f"Tipo de juego: {game.game_type} "
                    print(stats)
                else:
                    print(f"No hay juegos activos")

            elif command.startswith('jugador '):
                player_id = command.split(' ')[1].split(':')
                player_id = (player_id[0], player_id[1])
                player, _ = get_player(self.server.online_players, player_id)
                print(player)

            elif command == 'jugadores':
                if len(self.server.online_players) > 0:
                    for player in self.server.online_players:
                        print(f"Jugador {player.player_id}")
                else:
                    print(f"No hay jugadores en línea")

            elif command.startswith('barcos '):
                game_id = command.split(' ')[1]
                game = get_game(self.server.active_games, game_id)
                if game != None:
                    print(f"---- Barcos jugador 1, vidas: {game.player_1.remaining_lives} ----")
                    for ship in game.player_1.ships:
                        for coord in ship.list_coordinates:
                            print(f"{coord}")

                    print(f"---- Barcos jugador 2, vidas: {game.player_2.remaining_lives} ----")
                    for ship in game.player_2.ships:
                        for coord in ship.list_coordinates:
                            print(f"{coord}")
                else:
                    print(f"Partida no encontrada")

            else:
                print("Comando no reconocido. Intente nuevamente.")
