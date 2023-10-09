from clases.Bot import Bot
from clases.Server import Server
from clases.Match import Match
from clases.ServerMsg import ServerMessage
from clases.Coordinates import Coordinates
from clases.utils import get_player
import json

server = Server()
udp_server_socket = server.start_server()

def send_msg(client_address, action, status, position):
    response = ServerMessage(action=action, status=status, position=position).make_message()
    udp_server_socket.sendto(response.encode(encoding='utf-8', errors='strict'), client_address)

def is_match_finish(match: Match):
    pl1 = match.player_1.remaining_lives
    pl2 = match.player_2.remaining_lives
    if pl2 == 0:
        return (True, pl1)
    elif pl1 == 0:
        return (True, pl2)
    else:
        return (False, None)

def start_new_game(client_address):
    player_id = f"{client_address[0]}:{str(client_address[1])}"
    player, _ = get_player(server.online_players, player_id)
    if player.match_type == 1:
        bot = Bot()
        bot.build_random_ship()
        player.update_status(4)
        match = Match(match_id=player_id, player_1=player, player_2=bot, current_turn=player)
        server.active_games.append(match)
        print(bot)

    if player.status == 4:
        print(f"El jugador {player_id} ya está en una partida.")
        return
    
    if not player.has_created_ships():
        print(f"El jugador {player_id} debe crear sus barcos antes de iniciar una partida.")
        return

    for other_player in server.online_players:
        if other_player.match_type == 0 and other_player != player and other_player.has_created_ships():
            # Crear una partida
            player.update_status(4)
            other_player.update_status(4)
            match = Match(match_id=f"{player_id}_{other_player.player_id}", player_1=player, player_2=other_player, current_turn=player)
            server.active_games.append(match)
            player.match_type = 1
            other_player.match_type = 1
            print(f"Se ha creado una partida entre {player_id} y {other_player.player_id}")
            print(match.player_1)
            print(match.player_2)
            return

while(True):
    recieved_msg, client_address = udp_server_socket.recvfrom(1024)
    msg = json.loads(recieved_msg.decode(encoding='utf-8', errors='strict'))
    is_valid_action, action = server.validate_action(msg)

    if(is_valid_action):
        ### Conectamos al usuario
        if action == "c":
            status = 1 if server.connect_player(client_address) else 0
            send_msg(client_address, action, status=status, position=[])

        ### Cambiamos su tipo de partida
        elif action == "s":
            status = 1 if server.select_match(client_address, msg) else 0
            send_msg(client_address, action, status=status, position=[])

        ### Validamos, construimos e iniciamos partida, vs BOT
        elif action == "b":
            status = 1 if server.build_ships(client_address, msg) else 0
            send_msg(client_address, action, status=status, position=[])
            if status == 1:
                start_new_game(client_address)

        elif action == "a":
            game: Match
            coor_in = msg['position']
            player_id = f"{client_address[0]}:{str(client_address[1])}"
            player, index = get_player(server.online_players, player_id)
            coor = Coordinates(coor_in[0], coor_in[1])
            for game in server.active_games: 
                if player_id == game.match_id:
                    valid = server.attack(match=game, coor=coor) # Ataque del usuario
                    send_msg(client_address, action, status=1 if valid else 0, position=coor_in)
                    server.attack(match=game, coor=None) # Ataca el bot despues de enviar el msj
                    finish, _ = is_match_finish(game)

        elif action == "d":
            status = 1 if server.disconnect_player(client_address) else 0
            send_msg(client_address, action, status=status, position=[])

    else:
        ### Mensaje de accion invalida...
        send_msg(client_address, action, status=0, position=[])
    