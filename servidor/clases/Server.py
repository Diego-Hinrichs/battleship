from dataclasses import dataclass, field
import socket

@dataclass
class Server:
    """Clase servidor"""
    server_ip: str = "127.0.0.1"
    server_port: int = 20002
    buffersize: int = 1024
    online_players: list = field(default_factory=list)
    used_ports: dict = field(default_factory=dict)
    actions = ["connect", "disconnect", "attack","select", "build", "lose", "help"]

    def start_server(self):
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_server_socket.bind((self.server_ip, self.server_port))
        self.used_ports.update({self.server_port: True})
        return udp_server_socket

    def start_game(self) -> bool:
        return 0

    def end_game(self) -> bool:
        return 0
