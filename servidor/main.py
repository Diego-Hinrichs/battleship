from clases.Player import Player
from clases.Coordinates import Coordinates
from clases.Server import Server
from clases.Board import Board
from clases.ServerMsg import ServerMessage

server = Server()
udp_server_socket = server.start_server()
print(f"\nIniciando servidor en:\t{server.server_ip}:{server.server_port}")

def send_msg(response, udp_server_socket, client_address):
    udp_server_socket.sendto(response.encode(encoding='utf-8', errors='strict'), client_address)
    return 0

while(True):
    recieved_msg, client_address = udp_server_socket.recvfrom(1024)
    is_valid_action, action = server.validate_action(recieved_msg.decode(encoding='utf-8', errors='strict'))
    if(is_valid_action):
        ### Conectamos al usuario
        if action == "c":
            if (server.connect_player(client_address)):
                response = ServerMessage(action=action, status=1).make_message()
                send_msg(response, udp_server_socket, client_address)
            else: 
                response = ServerMessage(action=action, status=0).make_message()
                send_msg(response, udp_server_socket, client_address)
        
        ### Selecciona tipo partida
        if action == "s":
            if (server.select_match(client_address)):
                response = ServerMessage(action=action, status=1).make_message()
                send_msg(response, udp_server_socket, client_address)
            else: 
                response = ServerMessage(action=action, status=0).make_message()
                send_msg(response, udp_server_socket, client_address)



        ### Construye sus barcos
        

        ### Juega


        ### Anuncia derrota


        ### Se desconecta
        if action == "d":
            if (server.disconnect_player(client_address)):
                response = ServerMessage(action=action, status=1).make_message()
                send_msg(response, udp_server_socket, client_address)
            else: 
                response = ServerMessage(action=action, status=0).make_message()
                send_msg(response, udp_server_socket, client_address)
    else:
        ### Mensaje de accion invalida
        response = ServerMessage(action=action, status=0).make_message()
        send_msg(response, udp_server_socket, client_address)
        #print(f"Accion incorrecta: {recieved_msg.decode(encoding='utf-8', errors='strict')}\tRecibido desde: {client_address[1]}\n")
    