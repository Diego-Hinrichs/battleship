from dataclasses import dataclass, field
import socket
import json

@dataclass
class Client:
    status: int = 0 # 0: Desconectado; 1: Conectado; 2: Eligió modo de juego; 3: Puso barcos; 4: Esta jugando -> Si pierde pasa a 0: Desconectado
    match_type: int = 0 # PvP o PvB
    remaining_lives: int = 6
    opponent_lives_remaining: int = 6
    list_of_actions = ["a", "b", "c", "d", "l", "s"]
    socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def connect_whit_server(self) -> bool:
        return True

    def update_status(self, recieved_msg, msg_sent):
        action = recieved_msg["action"]
        msg_sent = json.loads(msg_sent)

        if (action in self.list_of_actions):
            recieved_status = recieved_msg["status"]
            if (action == "c") and recieved_status:
                self.status = 1 # Conectado
                print(f"Conexión exitosa con servidor!")
                return True
            
            elif (action == "s") and recieved_status:
                self.status = 2 # Eligio modo de juego
                self.match_type = msg_sent["bot"]
                print(f"{'Player vs Bot' if self.match_type else 'Player vs Player'}")
                return True
            
            elif (action == "b") and recieved_status:
                self.status = 3 # Barcos buenardos
                return True

            elif (action == "a"):
                print(f"Ultimo ataque: {recieved_msg['position']}")
                if recieved_status == 1:
                    self.opponent_lives_remaining -= 1
                    if self.opponent_lives_remaining == 0:
                        print(f"Ganaste!!")
                        print(f"Selecciona partida para continuar o desconectate [s/d]: ")
                        self.__init__(status=1) # Pasar a estado conectado, reset de status
                elif recieved_status == 0:
                    print("No acertaste")

            elif (action == "d") and recieved_status:
                self.status = 0 # Desconectado
                print(f"Te haz desconectado, bye bye!")
                self.socket.close()
                exit()
            else:
                print(f"Algo ha salido mal, intenta de nuevo")
                return False
        else:
            return False
    
    def __str__(self) -> str:
        return f"status: {self.status},\nmatch_type: {self.match_type}"