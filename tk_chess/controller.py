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
