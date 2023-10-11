from clases.ClientMsg import ClientMessage
from clases.Client import Client
import json, sys, signal
from dotenv import load_dotenv
import os

# https://docs.python.org/3/library/socket.html
# https://pythontic.com/modules/socket/recvfrom

load_dotenv(dotenv_path="../.env")
SERVER_LOCAL = os.getenv("SERVER_LOCAL")
SERVER_UNIVERSIDAD = os.getenv("SERVER_UNIVERSIDAD")
SERVER_PORT = os.getenv("SERVER_PORT")

server_address = (SERVER_LOCAL, int(SERVER_PORT)) # type: ignore
client = Client()
upd_client_socket = client.socket

def send_msg(response, upd_client_socket, server_address):
    upd_client_socket.sendto(response.encode(encoding='utf-8', errors='strict'), server_address)
    return 0

def handle_ctrl_c(sig, frame):
    print("\nCtrl+C presionado. Enviando mensaje de despedida al servidor...")
    msg_to_send = ClientMessage(action="d", bot=0, ships={}, position=[]).make_message(client)
    send_msg(msg_to_send, upd_client_socket, server_address)
    sys.exit(0)

# Registra el manejador de señal para Ctrl+C
signal.signal(signal.SIGINT, handle_ctrl_c)

print(f"Iniciando conexion con {SERVER_LOCAL} en el puerto {SERVER_PORT}")

while(True):
    action = str(input(f"{SERVER_LOCAL}:{SERVER_PORT:<6}{'~ $':<4}")).lower()
    msg_to_send = ClientMessage(action=action).make_message(client)
    send_msg(msg_to_send, upd_client_socket, server_address)
    recieved_msg, server_address = upd_client_socket.recvfrom(1024)
    #TODO. Si no me envian confirmacion en x tiempo
    msg = json.loads(recieved_msg.decode(encoding='utf-8', errors='strict'))
    client.update_status(msg, msg_to_send) # Retorna algo al cliente