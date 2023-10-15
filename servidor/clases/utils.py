from clases.Player import Player
from clases.Game import Game
import json

def get_player(online_players: list[Player], client_address: tuple) -> tuple[Player, int]:
    player_id = f"{client_address[0]}:{str(client_address[1])}"
    player_index = -1
    player_out = Player()
    for index, player in enumerate(online_players):
        if (player.player_id == player_id):
            player_out = player
            player_index = index
    return (player_out, player_index)

def get_game(active_games: list[Game], game_id: str) -> Game | None:
    game: Game
    if len(active_games) > 0:
        for game in active_games:
            if game.game_id == game_id:
                return game
    else:
        return None
        
def msg_json(action: str, status: int, position: list) -> str:
    return json.dumps({"action": action, "status": status, "position": position})