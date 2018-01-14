# coding: utf-8
import utils
import configurations as conf
from tkinter import (
    Tk, Menu, Canvas, Frame, Label, messagebox, PhotoImage
)


class View(object):

    board_color_1 = conf.BOARD_COLOR_1
    board_color_2 = conf.BOARD_COLOR_2

    def __init__(self, controller):
        self.controller = controller
        self.parent = Tk()
        self.parent.title(conf.TITLE)
        self.create_chess_base()
        self.canvas.bind("<Button-1>", self.on_square_clicked)
        self.start_new_game()

    def mainloop(self):
        self.parent.mainloop()

    def create_chess_base(self):
        self.create_top_menu()
        self.create_canvas()
        self.draw_board()
        self.create_bottom_frame()

    def create_top_menu(self):
        self.menu_bar = Menu(self.parent)
        self.create_file_menu()
        self.create_edit_menu()
        self.create_about_menu()

    def __add_menu(self, label, cascade=None):
        menu = Menu(self.menu_bar, tearoff=0)
        if cascade is None:
            cascade = []
        for entry in cascade:
            menu.add_command(
                label=entry[0], command=entry[1]
            )
        self.menu_bar.add_cascade(label=label, menu=menu)
        self.parent.config(menu=self.menu_bar)

    def create_file_menu(self):
        self.__add_menu(
            "File", [("New Game", self.on_new_game_menu_clicked)]
        )

    def create_edit_menu(self):
        self.__add_menu(
            "Edit", [("Preferences", self.on_preference_menu_clicked)]
        )

    def create_about_menu(self):
        self.__add_menu(
            "About", [("About", self.on_about_menu_clicked)]
        )

    def on_new_game_menu_clicked(self):
        pass

    def on_preference_menu_clicked(self):
        pass

    def on_about_menu_clicked(self):
        messagebox.showinfo("More information",
                            "Visit https://pimiento.github.io")

    def create_canvas(self):
        canvas_width = conf.NUMBER_OF_COLUMNS * conf.DIMENSION_OF_EACH_SQUARE
        canvas_height = conf.NUMBER_OF_ROWS * conf.DIMENSION_OF_EACH_SQUARE
        self.canvas = Canvas(
            self.parent, width=canvas_width, height=canvas_height
        )
        self.canvas.pack(padx=8, pady=8)

    def draw_board(self):
        current_color = conf.BOARD_COLOR_2
        for row in range(conf.NUMBER_OF_ROWS):
            current_color = utils.get_alternate_color(current_color)
            for col in range(conf.NUMBER_OF_COLUMNS):
                x1, y1 = utils.get_x_y_coordinate(row, col)
                x2 = x1 + conf.DIMENSION_OF_EACH_SQUARE
                y2 = y1 + conf.DIMENSION_OF_EACH_SQUARE
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=current_color
                )
                current_color = utils.get_alternate_color(current_color)

    def create_bottom_frame(self):
        self.bottom_frame = Frame(self.parent, height=64)
        self.info_label = Label(
            self.bottom_frame, text=" White to Start Game ",
            fg=conf.BOARD_COLOR_2
        )
        self.info_label.pack(side="right", padx=8, pady=5)
        self.bottom_frame.pack(fill="x", side="bottom")

    def on_square_clicked(self, event):
        clicked_column = event.x // conf.DIMENSION_OF_EACH_SQUARE
        clicked_row = 7 - (event.y // conf.DIMENSION_OF_EACH_SQUARE)
        print("Hey you clicked on %d×%d" % (clicked_row, clicked_column))

    def draw_single_piece(self, position, piece):
        x, y = utils.get_numeric_notation(position)
        if piece:
            x0, y0 = self.calculate_piece_coordinate(x, y)

            if piece.__class__.__dict__.get("images") is None:
                piece.__class__.images = {}

            if piece.__class__.images.get(piece.color) is None:
                piece.__class__.images[
                    piece.color
                ] = PhotoImage(file=piece.filename)

            self.canvas.create_image(
                x0, y0, image=piece.__class__.images[piece.color],
                tags=("occupied"), anchor="center"
            )

    def calculate_piece_coordinate(self, row, col):
        x0 = (col * conf.DIMENSION_OF_EACH_SQUARE) +\
             int(conf.DIMENSION_OF_EACH_SQUARE / 2)
        y0 = ((7 - row) * conf.DIMENSION_OF_EACH_SQUARE) +\
             int(conf.DIMENSION_OF_EACH_SQUARE / 2)
        return (x0, y0)

    def draw_all_pieces(self):
        self.canvas.delete("occupied")
        for position, piece in self.controller.get_board_state():
            self.draw_single_piece(position, piece)

    def start_new_game(self):
        self.controller.reset_game_data()
        self.controller.reset_to_initial_locations()
        self.draw_all_pieces()
        self.info_label.config(text=" White to Start the Game ")
