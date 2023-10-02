from dataclasses import dataclass, field
import socket

@dataclass
class Client:
    status: int = 0
    match_type: int = 0

    def start_client(self):
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        return udp_server_socket

    def connect_whit_server(self) -> bool:
        return True

    def play(self) -> bool:
        return True

    def disconnect(self) -> bool:
        return True