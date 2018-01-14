import os
import utils
import exceptions
import configurations as conf


class Piece(object):
    short_name = None
    white = "white"
    black = "black"

    def __init__(self, color):
        self.name = self.__class__.__name__.lower()
        if color == self.black:
            self.name = self.name.lower()
        elif color == self.white:
            self.name = self.name.upper()
        self.color = color
        self.image = None

    def keep_reference(self, model):
        self.model = model

    @property
    def filename(self):
        return os.path.join(
            conf.PIECE_IMAGE_PATH, "pieces_image",
            "{}_{}.png".format(self.name.lower(), self.color)
        )

    def moves_available(self, current_position):
        allowed_moves = []
        start_row, start_column = utils.get_numeric_notation(current_position)
        for x, y in self.directions:
            collision = False
            for step in range(1, self.max_distance + 1):
                if collision:
                    break
                destination = start_row + step * x, start_column + step * y
                possible = self.possible_position(destination)
                if possible not in self.model.all_occupied_positions():
                    allowed_moves.append(destination)
                elif possible in self.model.all_positions_occupied_by_color(
                        self.color
                ):
                    collision = True
                else:
                    allowed_moves.append(destination)
                    collision = True
        allowed_moves = filter(utils.is_on_board, allowed_moves)
        return [utils.get_alphanumeric_position(a) for a in allowed_moves]

    def possible_position(self, destination):
        return utils.get_alphanumeric_position(destination)


class King(Piece):
    directions = conf.ORTHOGONAL_POSITIONS + conf.DIAGONAL_POSITIONS
    max_distance = 1
    short_name = "K"


class Queen(Piece):
    directions = conf.ORTHOGONAL_POSITIONS + conf.DIAGONAL_POSITIONS
    max_distance = 8
    short_name = "Q"


class Rook(Piece):
    directions = conf.ORTHOGONAL_POSITIONS
    max_distance = 8
    short_name = "R"


class Bishop(Piece):
    directions = conf.DIAGONAL_POSITIONS
    max_distance = 8
    short_name = "B"


class Knight(Piece):
    directions = conf.KNIGHT_POSITIONS
    short_name = "N"

    def moves_available(self, current_position):
        start_position = utils.get_numeric_notation(current_position.upper())
        color_occupied = self.model.all_positions_occupied_by_color(self.color)
        allowed_moves = []
        for x, y in self.directions:
            destination = start_position[0] + x, start_position[1] + 1
            pos = utils.get_alphanumeric_position(destination)
            if pos not in color_occupied and utils.is_on_board(destination):
                allowed_moves.append(pos)
        return allowed_moves


class Pawn(Piece):
    short_name = "P"

    def moves_available(self, current_position):
        if self.color == Piece.white:
            initial_position, direction = 1, 1
        else:
            initial_position, direction = 6, -1
        enemy = utils.get_enemy(self.color)
        allowed_moves = []
        # Moving
        prohibited = self.model.all_occupied_positions()
        start_position = utils.get_numeric_notation(current_position.upper())
        forward = start_position[0] + direction, start_position[1]
        f_alphanum_pos = utils.get_alphanumeric_position(forward)
        if f_alphanum_pos not in prohibited and utils.is_on_board(forward):
            allowed_moves.append(f_alphanum_pos)
            if start_position[0] == initial_position:
                # If pawn is in starting position allow double moves
                double_forward = (forward[0] + direction, forward[1])
                df_alphanum_pos = utils.get_alphanumeric_position(double_forward)
                is_on_board = utils.is_on_board(double_forward)
                if df_alphanum_pos not in prohibited and is_on_board:
                    allowed_moves.append(df_alphanum_pos)
        # Attacking
        for a in range(-1, 2, 2):
            attack = start_position[0] + direction, start_position[1] + a
            a_alphanum_pos = utils.get_alphanumeric_position(attack)
            color_occupied = self.model.all_positions_occupied_by_color(enemy)
            if a_alphanum_pos in color_occupied:
                allowed_moves.append(a_alphanum_pos)
        return allowed_moves

pieces = [King, Queen, Rook, Bishop, Knight, Pawn]


def create_piece(piece, color=Piece.white):
    if isinstance(piece, str):
        variants = {cls.short_name: cls for cls in pieces}
        if piece.upper() in variants:
            color = Piece.white if piece.isupper() else Piece.black
            piece = variants[piece.upper()]
            return piece(color)
    raise exceptions.ChessError("invalid piece name: '{}'".format(piece))
