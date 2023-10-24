from dataclasses import dataclass, field
import socket
import json

@dataclass
class Client:
    status: int = 0 # 0: Desconectado; 1: Conectado; 2: Eligió modo de juego; 3: Puso barcos y esta en partida -> Si pierde pasa a 0: Desconectado
    game_type: int = 0 # PvP o PvB
    remaining_lives: int = 6
    list_of_actions = ["c", "s", "b", "a", "t", "l", "w", "d"]
    socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def update_status(self, recieved_msg, msg_sent):
        recieved_action = recieved_msg["action"]
        msg_sent = json.loads(msg_sent)

        if (recieved_action in self.list_of_actions):
            recieved_status = recieved_msg["status"]
            if (recieved_action == "c"):
                if recieved_status == 1:
                    self.status = 1 # Conectado
                    print(f"Conexión exitosa con servidor!")
                if recieved_status == 0 and self.status == 1:
                    print(f"Ya estas conectado")
                    
            elif (recieved_action == "s") and recieved_status == 1:
                self.status = 2 # Eligio modo de juego
                self.game_type = msg_sent["bot"]
                print(f"{'Player vs Bot' if self.game_type else 'Player vs Player'}")
            
            elif (recieved_action == "b") and recieved_status == 1:
                self.status = 4
                print(f"Barcos correctos, consulta tu turno (t)")

            elif (recieved_action == "a"):
                if recieved_status == 1:
                    print(f"Acertaste tu último ataque: {recieved_msg['position']}")
                    print(f"pregunta tu turno (t), si ya ganaste (w) o te rindes (l)")
                elif recieved_status == 0:
                    print(f"No acertaste")
                    print(f"pregunta tu turno (t), si ya ganaste (w) o te rindes (l)")
                else:
                    print(f"Algo ha malido sal, intenta de nuevo")

            elif (recieved_action == "t"):
                your_turn = 'Tu turno' if recieved_status == 1 else 'Aún no puedes jugar'
                print(your_turn)

            elif (recieved_action == "w"):
                win = 'Ganaste' if recieved_status == 1 else 'Aún no ganas'
                if win == 'Ganaste':
                    print(f"Ganaste\nPasas a estado conectado, puedes conectarte nuevamente con (c):")
                    self.__init__(status=1, game_type=0, remaining_lives=6) # Reset
                else:
                    print(win)
            
            elif (recieved_action == "l") and recieved_status == 1:
                print(f'Perdiste\nPasas a estado conectado, puedes selecionar partida (s):')
                self.__init__(status=1, game_type=0, remaining_lives=6) # Reset                

            elif (recieved_action == "d") and recieved_status:
                self.status = 0 # Desconectado
                print(f"Te has desconectado, bye bye!")
                self.socket.close()
                exit()

            else:
                print(f"Algo ha salido mal, intenta de nuevo")
                return False
        else:
            return False
    
    def __str__(self) -> str:
        return f"status: {self.status},\ngame_type: {self.game_type}"

client = Client()