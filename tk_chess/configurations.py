TITLE = " Chess "
NUMBER_OF_ROWS = 8
NUMBER_OF_COLUMNS = 8
DIMENSION_OF_EACH_SQUARE = 64
BOARD_COLOR_1 = "#DDB88C"
BOARD_COLOR_2 = "#A66D4F"
FIGURES = ('r', 'n', 'b', 'q', 'k', 'b', 'n', 'r')
X_AXIS_LABELS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
Y_AXIS_LABELS = range(1, 9)     # 1..8
# locate pieces on the board
# blacks
START_PIECES_POSITION = {}
START_PIECES_POSITION.update(
    {char+"8": piece.lower() for char, piece in zip(X_AXIS_LABELS, FIGURES)}
)
START_PIECES_POSITION.update(
    {char+"7": "p" for char in X_AXIS_LABELS}
)
# whites
START_PIECES_POSITION.update(
    {char+"2": "P" for char in X_AXIS_LABELS}
)
START_PIECES_POSITION.update(
    {char+"1": piece.upper() for char, piece in zip(X_AXIS_LABELS, FIGURES)}
)
# locating is done
PIECE_IMAGE_PATH = (
    "../Tkinter GUI Application Development Blueprints_code/B04945_04_code"
)
