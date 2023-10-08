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

while(True):
    recieved_msg, client_address = udp_server_socket.recvfrom(1024)
    msg = json.loads(recieved_msg.decode(encoding='utf-8', errors='strict'))
    is_valid_action, action = server.validate_action(msg)
    if action == "d":
        if (server.disconnect_player(client_address)):
            send_msg(client_address, action, status=1, position=[])
        else: 
            send_msg(client_address, action, status=0, position=[])

    if(is_valid_action):
        ### Conectamos al usuario
        if action == "c":
            if (server.connect_player(client_address)):
                send_msg(client_address, action, status=1, position=[])
            else: 
                send_msg(client_address, action, status=0, position=[])

        elif action == "s":
            if (server.select_match(client_address, msg)):
                send_msg(client_address, action, status=1, position=[])
            else: 
                send_msg(client_address, action, status=0, position=[])

        elif action == "b":
            if (server.build_ships(client_address, msg)):
                send_msg(client_address, action, status=1, position=[])
                player_id = f"{client_address[0]}:{str(client_address[1])}"
                player, index = get_player(server.online_players, player_id)
                if len(server.online_players) == 1 or player.match_type == 1:
                    bot = Bot()
                    bot.build_random_ship()
                    print(bot)
                    match = Match(match_id=player_id, player_1=player, player_2=bot, current_turn=player)
                    server.active_games.append(match)
                # Si es 1v1 match_id será la ip+port de ambos usuarios...
            else:
                send_msg(client_address, action, status=0, position=[])

        elif action == "a":
            # TODO:Tomar la partida, validar el ataque y ver si ataco, actualizar status
            # Esto es para jugar contra bot....
            coor_in = msg['position']
            player_id = f"{client_address[0]}:{str(client_address[1])}"
            player, index = get_player(server.online_players, player_id)
            coor = Coordinates(coor_in[0], coor_in[1])
            game: Match
            for game in server.active_games: 
                if player_id == game.match_id:
                    # Validar el ataque
                    valid = server.attack(match=game,coor=coor)
                    if valid:
                        # Si el ataque es valido informar con a1[x,y]
                        send_msg(client_address, action, status=1, position=coor_in)
                        success = server.attack(match=game, coor = None) # Ataca el bot
                        if success:
                            send_msg(client_address, action, status=1, position=[])
                    else:
                        # Si el ataque no es valido informar con a0[x,y]
                        send_msg(client_address, action, status=0, position=coor_in)
                        success = server.attack(match=game, coor = None) # Ataca el bot
                        if success:
                            send_msg(client_address, action, status=1, position=[])    
    else:
        ### Mensaje de accion invalida
        send_msg(client_address, action, status=0, position=[])
    