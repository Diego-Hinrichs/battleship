from clases.Bot import Bot
from clases.Server import Server
from clases.MatchBot import MatchBot
from clases.ServerMsg import ServerMessage
from clases.utils import get_player
import json

server = Server()
udp_server_socket = server.start_server()
def send_msg(client_address, action, status, position):
    response = ServerMessage(action=action, status=status, position=position).make_message()
    udp_server_socket.sendto(response.encode(encoding='utf-8', errors='strict'), client_address)
    return 0

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
                # Jugar vs bot
                bot = Bot().build_random_ship()
                print(bot)
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
                # Jugar vs bot
                bot = Bot()
                match = MatchBot(match_id="primera_partida",match_type=0, bot=bot, player_1=player)
            else: 
                send_msg(client_address, action, status=0, position=[])

    else:
        ### Mensaje de accion invalida
        send_msg(client_address, action, status=0, position=[])
    