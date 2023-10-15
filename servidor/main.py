from clases.Player import Player
from clases.Bot import Bot
from clases.Server import Server
from clases.Game import Game
from clases.ServerMsg import ServerMessage
from clases.Coordinates import Coordinates
from clases.utils import get_player, get_game
from console import Console
import json, threading

server = Server()
udp_server_socket = server.start_server()
Console(server).start()

def send_msg(client_address, action, status, position):
    response = ServerMessage(action=action, status=status, position=position).make_message()
    udp_server_socket.sendto(response.encode(encoding='utf-8', errors='strict'), client_address)

def start_new_game_pvb(player: Player):
    if player.status == 3:
        bot = Bot()
        bot.build_random_ship()
        game = Game(game_id=player_id, player_1=player, player_2=bot, current_turn=player.player_id)
        server.active_games.append(game)
        player.update_status(4)

def start_new_game_pvp(player: Player):
    if not player.has_created_ships():
        print(f"El jugador {player_id} debe crear sus barcos antes de iniciar una partida.")
        return

    for player_2 in server.online_players:
        if player_2.game_type == 0 and player_2 != player and player_2.has_created_ships():
            player.update_status(4)
            player_2.update_status(4)
            game = Game(game_id=f"{player_id}_{player_2.player_id}", game_type=0, player_1=player, player_2=player_2, current_turn=player.player_id)
            server.active_games.append(game)
            print(f"Se ha creado una partida:\nPlayer 1: {player.player_id}\nPlayer 2: {player_2.player_id}")
            return

while True:
    received_msg, client_address = udp_server_socket.recvfrom(1024)
    msg = json.loads(received_msg.decode(encoding='utf-8', errors='strict'))
    is_valid_action, action = server.validate_action(msg)

    if is_valid_action:
        if action == "c":
            status = 1 if server.connect_player(client_address) else 0
            send_msg(client_address, action, status=status, position=[])

        elif action == "s":
            status = 1 if server.select_game(client_address, msg) else 0
            send_msg(client_address, action, status=status, position=[])

        elif action == "b":
            status = 1 if server.build_ships(client_address, msg) else 0
            send_msg(client_address, action, status=status, position=[])
            if status == 1:
                player_id = f"{client_address[0]}:{str(client_address[1])}"
                player, _ = get_player(server.online_players, client_address)
                if player.game_type == 1:
                    start_new_game_pvb(player)
                elif player.game_type == 0:
                    start_new_game_pvp(player)

        elif action == "a":
            """
            Si el jugador ataca pero ya gano devolver mensaje de victoria
            """
            game: Game
            coor_in = msg['position'] if len(msg['position']) == 2 else []
            if coor_in == []:
                send_msg(client_address, action, status=0, position=coor_in)
            else:
                player, index = get_player(server.online_players, client_address)
                coor = Coordinates(coor_in[0], coor_in[1])
                for game in server.active_games:
                    game_id = game.game_id.split("_")
                    
                    # Juego contra bot
                    if player.player_id == game.game_id and game.game_type == 1 and player.game_type == 1:
                        # Si gano el jugador con el ataque anterior
                        valid = server.user_attack(game=game, coor=coor)

                        if game.player_1.remaining_lives == 0:
                            server.active_games.remove(game) # Se elimina la partida
                            server.online_players.remove(player) # Se elimina el usuario
                            send_msg(client_address, "l", status=1, position=coor_in)
                        
                        if game.player_2.remaining_lives == 0:
                            server.active_games.remove(game)
                            server.online_players.remove(player)
                            send_msg(client_address, "w", status=1, position=coor_in)
                        
                        else:
                            send_msg(client_address, action, status=1 if valid else 0, position=coor_in)
                            server.bot_attack(game=game, coor=None)
                    
                    ##TODO. Arreglar esta condicion
                    elif player.player_id in game_id and game.game_type == 0:
                        if game.current_turn == player.player_id:
                            valid = server.user_attack(game=game, coor=coor)
                            send_msg(client_address, action, status=1 if valid else 0, position=coor_in)
                        else:
                            #TODO. Mensaje de que no es el turno del jugador
                            send_msg(client_address, "t", 0, position=coor_in)
                            
        elif action == "t":
            player, index = get_player(server.online_players, client_address)
            game: Game
            for game in server.active_games:
                if game.game_type == 1: # Si juega contra bot
                    send_msg(client_address, action, 1, [])
                elif game.game_type == 0:
                    your_turn = 1 if game.current_turn == player.player_id else 0
                    send_msg(client_address, action, your_turn, [])
                else:
                    send_msg(client_address, action, 0, [])

        elif action == "l":
            if (len(server.active_games) == 0):
                send_msg(client_address, action, 0, [])

            player, index = get_player(server.online_players, client_address)
            game: Game
            for game in server.active_games:
                if game.game_type == 1:
                    server.active_games.remove(game)
                    print(f"Ha ganado el bot")
                    send_msg(client_address, action, 1, [])

        elif action == "w":
            player, index = get_player(server.online_players, client_address)
            game: Game
            for game in server.active_games:
                if game.game_type == 1: 
                    remaining_lives = game.player_2.remaining_lives
                    win = 1 if remaining_lives == 0 else 0
                    send_msg(client_address, action, win, [])

        elif action == "d":
            status = 1 if server.disconnect_player(client_address) else 0
            send_msg(client_address, action, status=status, position=[])

    else:
        send_msg(client_address, action, status=0, position=[])
