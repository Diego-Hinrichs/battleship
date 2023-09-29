import socket


# https://docs.python.org/3/library/socket.html
# https://pythontic.com/modules/socket/recvfrom

server_ip = "127.0.0.1"
server_port = 20002
server_address = (server_ip, server_port)

upd_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
list_of_actions = ["connect", "build", "start", "lose", "attack", "select"]

while(True):
    action = str(input(f"Escribe una accion para enviar al servidor: "))
    if action == "disconnect":
        upd_client_socket.sendto(action.encode(encoding='utf-8', errors='strict'), server_address)
        print(f"Terminado conexion con el servidor\n")
        upd_client_socket.close()
        exit()

    upd_client_socket.sendto(action.encode(encoding='utf-8', errors='strict'), server_address)
    msg, client_address = upd_client_socket.recvfrom(1024)
    print(msg.decode())
