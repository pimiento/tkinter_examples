import configurations as conf
from piece import create_piece


class Model(dict):

    captured_pieces = {'white': [], 'black': []}
    player_turn = None
    halfmove_clock = 0
    fullmove_number = 1
    history = []

    def get_piece_at(self, position):
        return self.get(position)

    def reset_game_data(self):
        captured_pieces = {'white': [], 'black': []}
        player_turn = None
        halfmove_clock = 0
        fullmove_number = 1
        history = []

    def reset_to_initial_locations(self):
        self.clear()
        for position, value in conf.START_PIECES_POSITION.items():
            self[position] = create_piece(value)
            self[position].keep_reference(self)
        self.player_turn = 'white'
