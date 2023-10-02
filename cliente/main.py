from clases.ClientMsg import ClientMessage
from clases.Client import Client

# https://docs.python.org/3/library/socket.html
# https://pythontic.com/modules/socket/recvfrom

server_ip = "127.0.0.1"
server_port = 20002
server_address = (server_ip, server_port)
client = Client()
upd_client_socket = client.start_client()

def send_msg(response, upd_client_socket, server_address):
    upd_client_socket.sendto(response.encode(encoding='utf-8', errors='strict'), server_address)
    return 0

# Se deberia pedir la ip y el puerto para conexion al servidor
while(True):
    action = str(input(f"Escribe una accion para enviar al servidor: "))
    #TODO armar el msj
    msg_to_send = ClientMessage(action=action).make_message()

    ##TODO ENVIAR MSG
    send_msg(msg_to_send, upd_client_socket, server_address)

    ##TODO RECIBIR MSJ DEL SERVIDOR
    recieved_msg, server_address = upd_client_socket.recvfrom(1024)

    print(recieved_msg.decode(encoding='utf-8', errors='strict'))
    
    # if action == "d":
    #     upd_client_socket.sendto(action.encode(encoding='utf-8', errors='strict'), server_address)
    #     print(f"Terminado conexion con el servidor\n")
    #     upd_client_socket.close()
    #     exit()
