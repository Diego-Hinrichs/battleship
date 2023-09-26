import socket

# https://docs.python.org/3/library/socket.html
# https://pythontic.com/modules/socket/recvfrom

init_msg = "CONEXION".encode(encoding='utf-8', errors='strict')
server_ip = "127.0.0.1"
server_port = 20002

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Cliente inicia la conexion con el servidor indicando la IP y Puerto
def init_connection(ip: str, port: int):    
    # Establece la conexión inicial con el servidor
    UDPClientSocket.sendto(init_msg, (server_ip, server_port))
    response, server_address = UDPClientSocket.recvfrom(1024)

    if response.decode(encoding='utf-8', errors='strict') == "CONEXION_ACEPTADA":
        print("Conexión inicial exitosa.")
        return (True, server_address)
    else:
        print("El servidor rechazó la conexión. Cerrando el cliente.")
        UDPClientSocket.close()
        return False
    
# Esto deberia ir al servidor?...
# Si, la lista de comandos deberia estar en el servidor
# TODO: pasar comandos al servidor
def commands(command: str):
    list_of_commands = ["chao"]
    command_in = command in list_of_commands
    
    command_e = command.encode(encoding='utf-8', errors='strict')

    if(command_in): 
        if command == "chao":
            UDPClientSocket.sendto(command_e, server_address)
            UDPClientSocket.close()
            exit()
    else:
        print(f"Comando equivocado")


conn, server_address = init_connection(server_ip, server_port)
# Si servidor acepta la conexion
while(conn):
    # Escucha otros mensajes del cliente
    cmd = str(input(f"Escribe un comando para enviar al servidor: "))
    commands(cmd)
    