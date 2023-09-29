from dataclasses import dataclass, field

@dataclass
class ServerMessage():
    action: str = "connect"
    status: int = 0 # 0: Mal o 1: Bien 
    position: tuple = (0,0)
    
    def make_message(self):
        msg = {"action": self.action, 
               "status": self.status, 
               "position": self.position}
        return msg