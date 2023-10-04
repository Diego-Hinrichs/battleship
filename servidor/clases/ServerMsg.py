from dataclasses import dataclass, field
import json

def msg_json(action: str, status: int, position: list) -> str:
    return json.dumps({"action": action, "status": status, "position": position})

@dataclass
class ServerMessage():
    action: str = "c"
    status: int = 0 # 0: Mal o 1: Bien 
    position: list = field(default_factory=list)
    
    def make_message(self):
        return msg_json(action = self.action, status = self.status, position = self.position)
    
    def __str__(self):
        f"'action': {self.action}\
            'status': {self.status}\
            'position': {self.position}"