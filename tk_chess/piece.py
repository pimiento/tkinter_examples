import os
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


class King(Piece):
    short_name = "K"


class Queen(Piece):
    short_name = "Q"


class Rook(Piece):
    short_name = "R"


class Bishop(Piece):
    short_name = "B"


class Knight(Piece):
    short_name = "N"


class Pawn(Piece):
    short_name = "P"


pieces = [King, Queen, Rook, Bishop, Knight, Pawn]


def create_piece(piece, color='white'):
    if isinstance(piece, str):
        variants = {cls.short_name: cls for cls in pieces}
        if piece.upper() in variants:
            color = "white" if piece.isupper() else "black"
            piece = variants[piece.upper()]
            return piece(color)
    raise exceptions.ChessError("invalid piece name: '{}'".format(piece))
