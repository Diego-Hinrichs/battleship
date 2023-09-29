from clases.Player import Player
from clases.Coordinates import Coordinates
from clases.Server import Server

# https://docs.python.org/3/library/socket.html
# https://pythontic.com/modules/socket/recvfrom

server = Server()
udp_server_socket = server.start_server()

def connect():
    if not server.used_ports.get(client_address[1]):
        response = ("connection accepted").encode(encoding='utf-8', errors='strict') 
        udp_server_socket.sendto(response, client_address)
        server.used_ports.update({client_address[1]: True}) # Agregar el puerto a un dict puerto: bool
        player = Player(client_address[1], [], 6) # Como lo asigna python, no es necesario validar el puerto
        print(f"Nuevo jugador en el puerto (id): {client_address[1]}\n")
        server.online_players.append(player)
    else:
        # TODO. intentos, si supera los 5 lo baneo por weta :)
        # print(f"Jugador ya se encuentra en linea {client_address[1]}\n")
        response = ("El jugador ya se encuentra online").encode(encoding='utf-8', errors='strict') 
        udp_server_socket.sendto(response, client_address)

def actions(recived_action: str, client_address):
    action = recived_action in server.actions
    if(action):
        if recived_action == "connect":
            connect()
        elif recived_action == "disconnect":
            print(f"Conexión terminada con: {client_address[1]}\n")
    else:
        response = ("Accion no valida").encode(encoding='utf-8', errors='strict') 
        udp_server_socket.sendto(response, client_address)
        print(f"Accion incorrecta: {recived_action}\nRecibido desde: {client_address[1]}\nPara ver los comandos disponibles, escribe: help")

while(True):
    msg, client_address = udp_server_socket.recvfrom(1024)
    actions(msg.decode(encoding='utf-8', errors='strict').lower(), client_address)
