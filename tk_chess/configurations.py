import os
from configparser import ConfigParser, Error as ConfigParserError

TITLE = " Chess "
NUMBER_OF_ROWS = 8
NUMBER_OF_COLUMNS = 8
DIMENSION_OF_EACH_SQUARE = 64
# colors
BOARD_COLOR_1 = "#DDB88C"
BOARD_COLOR_2 = "#A66D4F"
HIGHLIGHT_COLOR = "#2EF70D"
#
FIGURES_POSITION = ('r', 'n', 'b', 'q', 'k', 'b', 'n', 'r')
X_AXIS_LABELS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
Y_AXIS_LABELS = range(1, 9)     # 1..8
# locate pieces on the board
# blacks
START_PIECES_POSITION = {}
START_PIECES_POSITION.update(
    {char+"8": piece.lower() for char, piece
     in zip(X_AXIS_LABELS, FIGURES_POSITION)}
)
START_PIECES_POSITION.update(
    {char+"7": "p" for char in X_AXIS_LABELS}
)
# whites
START_PIECES_POSITION.update(
    {char+"2": "P" for char in X_AXIS_LABELS}
)
START_PIECES_POSITION.update(
    {char+"1": piece.upper() for char, piece
     in zip(X_AXIS_LABELS, FIGURES_POSITION)}
)
# locating pieces is done
PIECE_IMAGE_PATH = (
    "../Tkinter GUI Application Development Blueprints_code/B04945_04_code"
)
#
ORTHOGONAL_POSITIONS = (
    (-1, 0),                    # left
    (0, 1),                     # up
    (1, 0),                     # right
    (0, -1)                     # down
)
DIAGONAL_POSITIONS = (
    (-1, -1),                   # left-down
    (-1, 1),                    # left-up
    (1, -1),                    # right-up
    (1, 1)                      # right-left
)
KNIGHT_POSITIONS = (
    (-2, -1),                   # 2left-1down
    (-2, 1),                    # 2left-1up
    (-1, -2),                   # 1down-2left
    (-1, 2),                    # 1down-2right
    (1, -2),                    # 1up-2left
    (1, 2),                     # 1up-2right
    (2, -1),                    # 2up-1left
    (2, 1)                      # 2up-1right
)

# if there is chess_options.ini config
config = ConfigParser()
try:
    config.read('chess_options.ini')
except (IOError, ConfigParserError):
    # do nothing
    pass
else:
    BOARD_COLOR_1 = config.get(
        'chess_colors', 'board_color_1', fallback=BOARD_COLOR_1
    )
    BOARD_COLOR_2 = config.get(
        'chess_colors', 'board_color_2', fallback=BOARD_COLOR_2
    )
    HIGHLIGHT_COLOR = config.get(
        'chess_colors', 'highlight_color', fallback=HIGHLIGHT_COLOR
    )
    DIMENSION_OF_EACH_SQUARE = int(config.get(
        'sizes', 'square_size', fallback=DIMENSION_OF_EACH_SQUARE
    ))
