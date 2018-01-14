# coding: utf-8

import utils
import itertools
import exceptions
import configurations as conf
from copy import deepcopy
from piece import create_piece, Piece, King, Pawn


class Model(dict):

    captured_pieces = {Piece.white: [], Piece.black: []}
    player_turn = None
    halfmove_clock = 0
    fullmove_number = 1
    history = []

    def get_piece_at(self, position):
        return self.get(position)

    def reset_game_data(self):
        captured_pieces = {Piece.white: [], Piece.black: []}
        player_turn = None
        halfmove_clock = 0
        fullmove_number = 1
        history = []

    def reset_to_initial_locations(self):
        self.clear()
        for position, value in conf.START_PIECES_POSITION.items():
            self[position] = create_piece(value)
            self[position].keep_reference(self)
        self.player_turn = Piece.white

    def all_positions_occupied_by_color(self, color):
        for position in self.keys():
            piece = self.get_piece_at(position)
            if piece.color == color:
                yield position

    def all_occupied_positions(self):
        return itertools.chain(
            self.all_positions_occupied_by_color(Piece.white),
            self.all_positions_occupied_by_color(Piece.black)
        )

    def get_all_available_moves(self, color):
        for position in self.keys():
            piece = self.get_piece_at(position)
            if piece and piece.color == color:
                moves = piece.moves_available(position)
                for m in moves:
                    yield m

    def get_alphanumeric_position_of_king(self, color):
        for position in self.keys():
            this_piece = self.get_piece_at(position)
            if isinstance(this_piece, King) and this_piece.color == color:
                return position

    def is_king_under_check(self, color):
        position_of_king = self.get_alphanumeric_position_of_king(color)
        opponent = Piece.black if color == Piece.white else Piece.white
        return position_of_king in self.get_all_available_moves(opponent)

    def pre_move_validation(self, initial_pos, final_pos):
        initial_pos, final_pos = initial_pos.upper(), final_pos.upper()
        piece = self.get_piece_at(initial_pos)
        try:
            piece_at_destination = self.get_piece_at(final_pos)
        except Exception as e:
            piece_at_destination = None
        if self.player_turn != piece.color:
            raise exceptions.NotYourTurn("Not " + piece.color + "'s turn!")
        enemy = utils.get_enemy(piece.color)
        moves_available = piece.moves_available(initial_pos)
        if final_pos not in moves_available:
            raise exceptions.InvalidMove
        if self.get_all_available_moves(enemy):
            if self.will_move_cause_check(initial_pos, final_pos):
                raise exceptions.Check
        if len(moves_available) == 0 and self.is_king_under_check(piece.color):
            raise exceptions.CheckMate
        elif len(moves_available) == 0:
            raise exceptions.Draw
        else:
            self.move(initial_pos, final_pos)
            self.update_game_statistics(
                piece, piece_at_destination, initial_pos, final_pos
            )
            self.change_player_turn(piece.color)

    def move(self, start_pos, final_pos):
        self[final_pos] = self.pop(start_pos, None)

    def will_move_cause_check(self, start_position, end_position):
        tmp = deepcopy(self)
        tmp.move(start_position, end_position)
        return tmp.is_king_under_check(self[start_position].color)

    def update_game_statistics(self, piece, dest, start_pos, end_pos):
        if piece.color == Piece.black:
            self.fullmove_number += 1
        self.halfmove_clock += 1
        abbr = piece.name
        if abbr == Pawn.__name__.lower():
            abbr = ''
            self.halfmove_clock = 0
        if dest is None:
            move_text = abbr + end_pos.lower()
        else:
            move_text = abbr + '×' + end_pos.lower()
            self.halfmove_clock = 0
        self.history.append(move_text)

    def change_player_turn(self, color):
        self.player_turn = utils.get_enemy(color)
