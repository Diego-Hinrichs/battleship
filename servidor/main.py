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

#TODO. esto se va para el server dps, separar partida vs bot de partida vs player
def start_new_game_pvb(player):
    bot = Bot()
    bot.build_random_ship()
    match = Match(match_id=player_id, player_1=player, player_2=bot, current_turn=player)
    server.active_games.append(match)

def start_new_game_pvp(player):
    if not player.has_created_ships():
        print(f"El jugador {player_id} debe crear sus barcos antes de iniciar una partida.")
        return

    #Jugar Player vs Player
    for player_2 in server.online_players:
        if player_2.match_type == 0 and player_2 != player and player_2.has_created_ships():
            player.update_status(4) # Estado = jugando
            player_2.update_status(4) 
            #TODO. El player 1 inicia el juego, ojito
            match = Match(match_id=f"{player_id}_{player_2.player_id}", player_1=player, player_2=player_2, current_turn=player)
            server.active_games.append(match)
            print(f"Se ha creado una partida:\nPlayer 1: {player.player_id}\nPlayer 2: {player_2.player_id}")
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
                player_id = f"{client_address[0]}:{str(client_address[1])}"
                player, _ = get_player(server.online_players, player_id)
                if player.match_type == 1:
                    start_new_game_pvb(player)
                elif player.match_type == 0:
                    start_new_game_pvp(player)

        elif action == "a":
            game: Match
            coor_in = msg['position']
            player_id = f"{client_address[0]}:{str(client_address[1])}"
            player, index = get_player(server.online_players, player_id)
            coor = Coordinates(coor_in[0], coor_in[1])
            for game in server.active_games:
                match_id = game.match_id.split("_")
                # En PvB match_id == player_id
                if player_id == game.match_id and game.match_type == 1 and player.match_type == 1:
                    print(match_id)
                    # Ataque del usuario
                    valid = server.user_attack(match=game, coor=coor)
                    send_msg(client_address, action, status=1 if valid else 0, position=coor_in)
                    # Ataca el bot despues de enviar el msj
                    server.bot_attack(match=game, coor=None)
                if player_id in match_id:
                    valid = server.user_attack(match=game, coor=coor)
                    send_msg(client_address, action, status=1 if valid else 0, position=coor_in)
                    print(player_id)

        elif action == "d":
            status = 1 if server.disconnect_player(client_address) else 0
            send_msg(client_address, action, status=status, position=[])

    else:
        send_msg(client_address, action, status=0, position=[])
    