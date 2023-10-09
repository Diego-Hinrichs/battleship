from clases.ClientMsg import ClientMessage
from clases.Client import Client
import json, sys, signal

# https://docs.python.org/3/library/socket.html
# https://pythontic.com/modules/socket/recvfrom

server_ip = "127.0.0.1"
server_port = 20001
server_address = (server_ip, server_port)
client = Client()
upd_client_socket = client.socket

def send_msg(response, upd_client_socket, server_address):
    upd_client_socket.sendto(response.encode(encoding='utf-8', errors='strict'), server_address)
    return 0

def handle_ctrl_c(sig, frame):
    print("\nCtrl+C presionado. Enviando mensaje de despedida al servidor...")
    msg_to_send = ClientMessage(action="d").make_message(client)
    send_msg(msg_to_send, upd_client_socket, server_address)
    sys.exit(0)

# Registra el manejador de señal para Ctrl+C
signal.signal(signal.SIGINT, handle_ctrl_c)

print(f"Iniciando conexion con {server_ip} en el puerto {server_port}")

while(True):
    action = str(input(f"{server_ip}:{server_port:<6}{'~ $':<4}")).lower()
    msg_to_send = ClientMessage(action=action).make_message(client)
    send_msg(msg_to_send, upd_client_socket, server_address)
    recieved_msg, server_address = upd_client_socket.recvfrom(1024)
    #TODO. Si no me envian confirmacion en x tiempo
    msg = json.loads(recieved_msg.decode(encoding='utf-8', errors='strict'))
    client.update_status(msg, msg_to_send) # Retorna algo al cliente