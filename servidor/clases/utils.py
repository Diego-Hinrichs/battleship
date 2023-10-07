from clases.Player import Player

def get_player(online_players: list[Player], player_id: str) -> tuple[Player, int]:
    player_index = -1
    player_out = Player()
    for index, player in enumerate(online_players):
        if (player.player_id == player_id):
            player_out = player
            player_index = index
            break
    return (player_out, player_index)