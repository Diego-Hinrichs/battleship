import socket

# https://docs.python.org/3/library/socket.html
# https://pythontic.com/modules/socket/recvfrom

local_ip = "127.0.0.1"
local_port = 20002
bufferSize = 1024

# Crear socket
# Familia de direcciones con las cuales mi socket puede comunicarse (AF_INET -> IPv4)
# También esta (AF_INET6 -> IPv6) (AF_BLUETOOTH, AF_UNIX)
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Vincular socket a la direccion. El socket no debe estar vinculado
UDPServerSocket.bind((local_ip, local_port))

print("Esperando la conexión inicial del cliente...")
init_data, client_address = UDPServerSocket.recvfrom(1024)

def accept_connection(data: bytes):
    if data.decode(encoding='utf-8', errors='strict') == "CONEXION":
        UDPServerSocket.sendto("CONEXION_ACEPTADA".encode(encoding='utf-8', errors='strict'), client_address)
        print(f"Conexión aceptada desde {client_address}")
        return (True, client_address)
    else:
        print("Conexión rechazada. Cerrando el servidor.")
        UDPServerSocket.close()
        return False
    
conn, client_address = accept_connection(data=init_data)

def commands(command: str):
    if command == "chao":
        UDPServerSocket.sendto("Cerrando conexion".encode(encoding='utf-8', errors='strict'), client_address)
        UDPServerSocket.close()
        exit()
    else:
        print(f"Recibido desde {client_address}: {command}")

# Se acepta la conexion del cliente
while(conn):
    msg, client_address = UDPServerSocket.recvfrom(1024)
    commands(msg.decode(encoding='utf-8', errors='strict'))
