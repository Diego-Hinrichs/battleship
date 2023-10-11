from dataclasses import dataclass, field
from clases.utils import msg_json

@dataclass
class ServerMessage():
    action: str = "c"
    status: int = 0
    position: list = field(default_factory=list)
    
    def make_message(self):
        return msg_json(action = self.action, status = self.status, position = self.position)
    
    def __str__(self):
        f"'action': {self.action} 'status': {self.status} 'position': {self.position}"