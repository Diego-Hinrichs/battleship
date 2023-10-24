from clases.Player import Player
from clases.Server import Server
from clases.Game import Game
from clases.Coordinates import Coordinates
from clases.ServerMsg import ServerMessage
from clases.utils import get_player, get_game
from console import Console
import json

server = Server()
udp_server_socket = server.start_server()
Console(server).start() # Podria crear otra clase para buscar la partida

def send_msg(udp_server_socket, client_address, action, status, position):
    response = ServerMessage(action=action, status=status, position=position).make_message()
    udp_server_socket.sendto(response.encode(encoding='utf-8', errors='strict'), client_address)

def update_player(index: int):
    new_player = Player(status = 1, player_id = player.player_id)
    server.online_players[index] = new_player

def player_vs_bot(server, game: Game, player, index, client_address, coor_in):
    valid = server.user_attack(game=game, coor=coor)
    if game.player_1.remaining_lives == 0: # Jugador
        update_player(index)
        server.active_games.remove(game)
        send_msg(udp_server_socket, client_address, "l", status=1, position=coor_in)
    elif game.player_2.remaining_lives == 0: # Bot
        update_player(index)
        server.active_games.remove(game)
        send_msg(udp_server_socket, client_address, "w", status=1, position=coor_in)
    else:
        send_msg(udp_server_socket,client_address, action, status=1 if valid else 0, position=coor_in)
        server.bot_attack(game=game, coor=None)

def player_vs_player(game: Game, player, index, client_address, coor_in):
    # Ver si perdio en el turno anterior
    if game.lose(player.player_id):
        for player_to_remove in game:
            if player.player_id == player_to_remove.player_id and isinstance(player_to_remove, Player):
                update_player(index)
                server.active_games.remove(game)
        send_msg(udp_server_socket,client_address, "l", 1, position=coor_in)

    elif game.current_turn == player.player_id:
        valid = server.user_attack(game=game, coor=coor)
        if game.win(player.player_id) == 1:
            update_player(index)
            send_msg(udp_server_socket, client_address, "w", 1, position=coor_in)
        else:
            send_msg(udp_server_socket, client_address, action, status=1 if valid else 0, position=coor_in)

while True:
    received_msg, client_address = udp_server_socket.recvfrom(1024)
    msg = json.loads(received_msg.decode(encoding='utf-8', errors='strict'))
    #print(msg)
    is_valid_action, action = server.validate_action(msg)

    if is_valid_action:
        game: Game
        player, index = get_player(server.online_players, client_address)
        game = get_game(server.active_games, player) # type: ignore
        if action == "c":
            if len(server.online_players) >= 2 or len(server.active_games) == 1: # Limitar la conexion a 2 jugadores o 1 juego activo
                send_msg(udp_server_socket, client_address, action, status=0, position=[])
            else:
                status = 1 if server.connect_player(client_address) else 0
                send_msg(udp_server_socket, client_address, action, status=status, position=[])

        elif action == "s":
            status = 1 if server.select_game(client_address, msg) else 0
            send_msg(udp_server_socket, client_address, action, status=status, position=[])

        elif action == "b":
            status = 1 if server.build_ships(client_address, msg) else 0
            send_msg(udp_server_socket, client_address, action, status=status, position=[])
            if status == 1:
                if player.game_type == 1:
                    server.start_new_game_pvb(player)
                elif player.game_type == 0:
                    server.start_new_game_pvp(player)

        elif action == "a" and game != None:
            coor_in = msg['position']
            if len(coor_in) == 0:
                send_msg(udp_server_socket, client_address, action, 0, position=coor_in)
            else:
                coor = Coordinates(coor_in[0], coor_in[1])
                if player.player_id == game.game_id and game.game_type == 1: # PvB
                    player_vs_bot(server, game, player, index, client_address, coor_in)
                elif player.player_id in game.game_id.split("_") and game.game_type == 0 and game.current_turn == player.player_id:
                    player_vs_player(game, player, index, client_address, coor_in)
                else:
                    send_msg(udp_server_socket, client_address, "t", 0, position=coor_in)

        elif action == "t" and game != None:
            if len(server.active_games) == 0:
                send_msg(udp_server_socket,client_address, action, 0, [])
            else:
                if game.game_type == 1: # Si juega contra bot
                    send_msg(udp_server_socket, client_address, action, 1, [])
                elif game.game_type == 0: # Player vs Player
                    your_turn = 1 if game.current_turn == player.player_id else 0
                    send_msg(udp_server_socket, client_address, action, your_turn, [])
                else:
                    send_msg(udp_server_socket, client_address, action, 0, [])

        elif action == "l" and game != None:
            if game.game_type == 1: # Bot
                update_player(index)
                server.active_games.remove(game)
                send_msg(udp_server_socket, client_address, action, 1, [])

            elif player.player_id in game.game_id.split("_") and game.game_type == 0: # PvP
                for player_in_game in game:
                    if player_in_game.player_id == player.player_id:
                        player_in_game.remaining_lives = 0
                        if game.current_turn == player.player_id:
                            game.switch_turn()
                            update_player(index)
                        send_msg(udp_server_socket, client_address, action, 1, [])
            else:
                send_msg(udp_server_socket, client_address, action, 0, [])

        elif action == "w" and game != None:
            if game.game_type == 1: # PvB
                win = game.win(player.player_id)
                send_msg(udp_server_socket, client_address, action, win, [])
            elif player.player_id in game.game_id.split("_") and game.game_type == 0: # PvP
                win = game.win(player.player_id)
                if win == 1:
                    send_msg(udp_server_socket, client_address, action, 1, position=[])
                else:
                    send_msg(udp_server_socket, client_address, action, win, position=[])

        elif action == "d":
            if player.status == 4 and player.player_id == game.game_id and game.game_type == 1: # Partida vs Bot
                server.active_games.remove(game)
                print(f"Gano el bot")
                status = 1 if server.disconnect_player(client_address) else 0
                send_msg(udp_server_socket, client_address, action, status, [])

            elif player.status == 4 and player.player_id in game.game_id.split("_") and game.game_type == 0:
                for player_to_disconnect in game and player_to_disconnect.player_id == player.player_id:
                    player_to_disconnect.remaining_lives = 0
                    if game.current_turn == player.player_id:
                        game.switch_turn()
                        status = 1 if server.disconnect_player(client_address) else 0
                        send_msg(udp_server_socket, client_address, action, status, [])
            else:
                status = 1 if server.disconnect_player(client_address) else 0
                send_msg(udp_server_socket, client_address, action, status=status, position=[])

        else:
            send_msg(udp_server_socket, client_address, action, status=0, position=[])
    else:
        send_msg(udp_server_socket, client_address, action, status=0, position=[])
