import configurations as conf
from piece import Piece


def get_numeric_notation(rowcol):
    row, col = rowcol
    return int(col)-1, conf.X_AXIS_LABELS.index(row)


def get_alphanumeric_position(rowcol):
    if is_on_board(rowcol):
        row, col = rowcol
        return "{}{}".format(
            conf.X_AXIS_LABELS[col], conf.Y_AXIS_LABELS[row]
        )


def get_alternate_color(current_color):
    return conf.BOARD_COLOR_1 if current_color == conf.BOARD_COLOR_2 \
        else conf.BOARD_COLOR_2


def get_x_y_coordinate(row, col):
    return ((col * conf.DIMENSION_OF_EACH_SQUARE),
            ((7 - row) * conf.DIMENSION_OF_EACH_SQUARE))


def is_on_board(rowcol):
    return 0 <= rowcol[0] <= 7 and 0 <= rowcol[1] <= 7


def get_enemy(color):
    return Piece.black if color == Piece.white else Piece.white
