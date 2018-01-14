import model


class Controller(object):
    def __init__(self):
        self.init_model()

    def init_model(self):
        self.__model = model.Model()

    def get_board_state(self):
        return self.__model.items()

    def reset_game_data(self):
        self.__model.reset_game_data()

    def reset_to_initial_locations(self):
        self.__model.reset_to_initial_locations()

    def get_piece_at(self, position_of_click):
        return self.__model.get_piece_at(position_of_click)

    def player_turn(self):
        return self.__model.player_turn

    def pre_move_validation(self, start_pos, end_pos):
        return self.__model.pre_move_validation(start_pos, end_pos)
