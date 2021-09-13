# -*- coding: utf-8 -*-
#
# This file is part of the python-shogi library.
# Copyright (C) 2012-2014 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>
# Copyright (C) 2015- Tasuku SUENAGA <tasuku-s-github@titech.ac>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

__author__ = 'Tasuku SUENAGA a.k.a. gunyarakun'
__email__ = 'tasuku-s-github@titech.ac'
__version__ = '1.0.14'

import collections

from .Move import *
from .Piece import *
from .Consts import *

PIECE_TYPES_WITHOUT_KING = [
    #        PAWN,      LANCE,      KNIGHT,      SILVER,
    #        GOLD,
    #      BISHOP,       ROOK,
    #   PROM_PAWN, PROM_LANCE, PROM_KNIGHT, PROM_SILVER,
    # PROM_BISHOP,  PROM_ROOK,
    PAWN, SILVER, GOLD, BISHOP, ROOK,
    PROM_PAWN, PROM_SILVER, PROM_BISHOP, PROM_ROOK,
]

MAX_PIECES_IN_HAND = [0,
        # 18, 4, 4, 4,
        # 4,
        # 2, 2,
        # 0,
        # 0, 0, 0, 0,
        # 0, 0,
        2, 2, 2, 2, 2,
        0, 0, 0, 0,
]

PIECE_PROMOTED = [
    #        None,
    #   PROM_PAWN, PROM_LANCE, PROM_KNIGHT, PROM_SILVER,
    #        None,
    # PROM_BISHOP,  PROM_ROOK,
    #        None,
    #        None,       None,        None,        None,
    #        None,       None,
    None,
    PROM_PAWN, PROM_SILVER, None, PROM_BISHOP, PROM_ROOK,
    None, None, None, None, None, 
]

NUMBER_JAPANESE_NUMBER_SYMBOLS = [
    # '０', '１', '２', '３', '４', 
    # '５', '６', '７', '８', '９'
    '０', '１', '２', '３', '４', '5'
]
NUMBER_JAPANESE_KANJI_SYMBOLS = [ #TODO
    '零', '一', '二', '三', '四',
    '五', '六', '七', '八', '九',
    '十', '十一', '十二', '十三', '十四',
    '十五', '十六', '十七', '十八'
]

# STARTING_SFEN = 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1'

# SQUARES = [
#     A9, A8, A7, A6, A5, A4, A3, A2, A1,
#     B9, B8, B7, B6, B5, B4, B3, B2, B1,
#     C9, C8, C7, C6, C5, C4, C3, C2, C1,
#     D9, D8, D7, D6, D5, D4, D3, D2, D1,
#     E9, E8, E7, E6, E5, E4, E3, E2, E1,
#     F9, F8, F7, F6, F5, F4, F3, F2, F1,
#     G9, G8, G7, G6, G5, G4, G3, G2, G1,
#     H9, H8, H7, H6, H5, H4, H3, H2, H1,
#     I9, I8, I7, I6, I5, I4, I3, I2, I1,
# ] = range(81)

STARTING_SFEN = 'kgsbr/p4/ppppp/5/PPPPP/4P/RBSGK b - 1'

SQUARES = [
    A5, A4, A3, A2, A1,
    B5, B4, B3, B2, B1,
    C5, C4, C3, C2, C1,
    D5, D4, D3, D2, D1,
    E5, E4, E3, E2, E1,
] = range(25)

SQUARES_L90 = [
    A1, B1, C1, D1, E1, 
    A2, B2, C2, D2, E2, 
    A3, B3, C3, D3, E3, 
    A4, B4, C4, D4, E4, 
    A5, B5, C5, D5, E5, 
]

SQUARES_R45 = [
    # A9, I8, H7, G6, F5, E4, D3, C2, B1,
    # B9, A8, I7, H6, G5, F4, E3, D2, C1,
    # C9, B8, A7, I6, H5, G4, F3, E2, D1,
    # D9, C8, B7, A6, I5, H4, G3, F2, E1,
    # E9, D8, C7, B6, A5, I4, H3, G2, F1,
    # F9, E8, D7, C6, B5, A4, I3, H2, G1,
    # G9, F8, E7, D6, C5, B4, A3, I2, H1,
    # H9, G8, F7, E6, D5, C4, B3, A2, I1,
    # I9, H8, G7, F6, E5, D4, C3, B2, A1,
    A5, E4, D3, C2, B1,
    B5, A4, E3, D2, C1,
    C5, B4, A3, E2, D1,
    D5, C4, B3, A2, E1,
    E5, D4, C3, B2, A1,
]

SQUARES_L45 = [
    # B9, C8, D7, E6, F5, G4, H3, I2, A1,
    # C9, D8, E7, F6, G5, H4, I3, A2, B1,
    # D9, E8, F7, G6, H5, I4, A3, B2, C1,
    # E9, F8, G7, H6, I5, A4, B3, C2, D1,
    # F9, G8, H7, I6, A5, B4, C3, D2, E1,
    # G9, H8, I7, A6, B5, C4, D3, E2, F1,
    # H9, I8, A7, B6, C5, D4, E3, F2, G1,
    # I9, A8, B7, C6, D5, E4, F3, G2, H1,
    # A9, B8, C7, D6, E5, F4, G3, H2, I1,
    B5, C4, D3, E2, A1,
    C5, D4, E3, A2, B1,
    D5, E4, A3, B2, C1,
    E5, A4, B3, C2, D1,
    A5, B4, C3, D2, E1,
]

def file_index(square):
    return square % 5

def rank_index(square):
    return square // 5

BB_VOID = 0b0000000000000000000000000
BB_ALL = 0b1111111111111111111111111

BB_SQUARES = [
    BB_A5, BB_A4, BB_A3, BB_A2, BB_A1,
    BB_B5, BB_B4, BB_B3, BB_B2, BB_B1,
    BB_C5, BB_C4, BB_C3, BB_C2, BB_C1,
    BB_D5, BB_D4, BB_D3, BB_D2, BB_D1,
    BB_E5, BB_E4, BB_E3, BB_E2, BB_E1,
] = [1 << i for i in SQUARES]

BB_SQUARES_L90 = [BB_SQUARES[SQUARES_L90[square]] for square in SQUARES]
BB_SQUARES_L45 = [BB_SQUARES[SQUARES_L45[square]] for square in SQUARES]
BB_SQUARES_R45 = [BB_SQUARES[SQUARES_R45[square]] for square in SQUARES]

BB_FILES = [
    BB_FILE_5,
    BB_FILE_4,
    BB_FILE_3,
    BB_FILE_2,
    BB_FILE_1,
] = [
    BB_A5 | BB_B5 | BB_C5 | BB_D5 | BB_E5,
    BB_A4 | BB_B4 | BB_C4 | BB_D4 | BB_E4,
    BB_A3 | BB_B3 | BB_C3 | BB_D3 | BB_E3,
    BB_A2 | BB_B2 | BB_C2 | BB_D2 | BB_E2,
    BB_A1 | BB_B1 | BB_C1 | BB_D1 | BB_E1,
]

BB_RANKS = [
    BB_RANK_A,
    BB_RANK_B,
    BB_RANK_C,
    BB_RANK_D,
    BB_RANK_E,
] = [
    BB_A1 | BB_A2 | BB_A3 | BB_A4 | BB_A5,
    BB_B1 | BB_B2 | BB_B3 | BB_B4 | BB_B5,
    BB_C1 | BB_C2 | BB_C3 | BB_C4 | BB_C5,
    BB_D1 | BB_D2 | BB_D3 | BB_D4 | BB_D5,
    BB_E1 | BB_E2 | BB_E3 | BB_E4 | BB_E5,
]


def shift_down(b):
    return (b << 5) & BB_ALL


def shift_2_down(b):
    return (b << 10) & BB_ALL


def shift_up(b):
    return b >> 5


def shift_2_up(b):
    return b >> 10


def shift_right(b):
    return (b << 1) & ~BB_FILE_5


def shift_2_right(b):
    return (b << 2) & ~BB_FILE_5 & ~BB_FILE_4


def shift_left(b):
    return (b >> 1) & ~BB_FILE_1


def shift_2_left(b):
    return (b >> 2) & ~BB_FILE_1 & ~BB_FILE_2


def shift_up_left(b):
    return (b >> 6) & ~BB_FILE_1


def shift_up_right(b):
    return (b >> 4) & ~BB_FILE_5


def shift_down_left(b):
    return (b << 4) & ~BB_FILE_1


def shift_down_right(b):
    return (b << 6) & ~BB_FILE_5

BB_PAWN_ATTACKS = [
    [shift_up(s) for s in BB_SQUARES],
    [shift_down(s) for s in BB_SQUARES],
]
BB_SILVER_ATTACKS = [[], []]
BB_GOLD_ATTACKS = [[], []]
BB_KING_ATTACKS = []

for bb_square in BB_SQUARES:
    mask = BB_VOID
    mask |= shift_up_left(bb_square)
    mask |= shift_up(bb_square)
    mask |= shift_up_right(bb_square)
    mask |= shift_down_left(bb_square)
    mask |= shift_down_right(bb_square)

    BB_SILVER_ATTACKS[BLACK].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_down_left(bb_square)
    mask |= shift_down(bb_square)
    mask |= shift_down_right(bb_square)
    mask |= shift_up_left(bb_square)
    mask |= shift_up_right(bb_square)

    BB_SILVER_ATTACKS[WHITE].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_up_left(bb_square)
    mask |= shift_up(bb_square)
    mask |= shift_up_right(bb_square)
    mask |= shift_left(bb_square)
    mask |= shift_right(bb_square)
    mask |= shift_down(bb_square)

    BB_GOLD_ATTACKS[BLACK].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_down_left(bb_square)
    mask |= shift_down(bb_square)
    mask |= shift_down_right(bb_square)
    mask |= shift_left(bb_square)
    mask |= shift_right(bb_square)
    mask |= shift_up(bb_square)

    BB_GOLD_ATTACKS[WHITE].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_left(bb_square)
    mask |= shift_right(bb_square)
    mask |= shift_up(bb_square)
    mask |= shift_down(bb_square)
    mask |= shift_up_left(bb_square)
    mask |= shift_up_right(bb_square)
    mask |= shift_down_left(bb_square)
    mask |= shift_down_right(bb_square)
    BB_KING_ATTACKS.append(mask & BB_ALL)

# 128 means 2 ^ (9 - 1 - 1), patterns of emptiness of one row without each ends
BB_RANK_ATTACKS = [[BB_VOID for i in range(8)] for k in SQUARES]
BB_FILE_ATTACKS = [[BB_VOID for i in range(8)] for k in SQUARES]

for square in SQUARES:
    for bitrow in range(0, 8):
        ## f : Num of col
        f = file_index(square) + 1
        ## q : Num of place 
        q = square + 1
        ## about all col
        while f < 5:
            BB_RANK_ATTACKS[square][bitrow] |= BB_SQUARES[q]
            if (1 << f) & (bitrow << 1):
                break
            q += 1
            f += 1

        f = file_index(square) - 1
        q = square - 1
        while f >= 0:
            BB_RANK_ATTACKS[square][bitrow] |= BB_SQUARES[q]
            if (1 << f) & (bitrow << 1):
                break
            q -= 1
            f -= 1

        r = rank_index(square) + 1
        q = square + 5
        while r < 5:
            BB_FILE_ATTACKS[square][bitrow] |= BB_SQUARES[q]
            if (1 << (4 - r)) & (bitrow << 1):
                break
            q += 5
            r += 1

        r = rank_index(square) - 1
        q = square - 5
        while r >= 0:
            BB_FILE_ATTACKS[square][bitrow] |= BB_SQUARES[q]
            if (1 << (4 - r)) & (bitrow << 1):
                break
            q -= 5
            r -= 1

BB_SHIFT_R45 = [
#      1, 73, 65, 57, 49, 41, 33, 25, 17,
#     10,  1, 73, 65, 57, 49, 41, 33, 25,
#     19, 10,  1, 73, 65, 57, 49, 41, 33,
#     28, 19, 10,  1, 73, 65, 57, 49, 41,
#     36, 28, 19, 10,  1, 73, 65, 57, 49,
#     45, 36, 28, 19, 10,  1, 73, 65, 57,
#     54, 45, 36, 28, 19, 10,  1, 73, 65,
#     63, 54, 45, 36, 28, 19, 10,  1, 73,
#     72, 63, 54, 45, 36, 28, 19, 10,  1
    1, 21,17,13, 9,
    6,  1,21,17,13,
    10, 6, 1,21,17,
    15,10, 6, 1,21,
    20,15,10, 6, 1,
]

BB_SHIFT_L45 = [
#     10, 19, 28, 36, 45, 54, 63, 72,  1,
#     19, 28, 36, 45, 54, 63, 72,  1, 11,
#     28, 36, 45, 54, 63, 72,  1, 11, 21,
#     36, 45, 54, 63, 72,  1, 11, 21, 31,
#     45, 54, 63, 72,  1, 11, 21, 31, 41,
#     54, 63, 72,  1, 11, 21, 31, 41, 51,
#     63, 72,  1, 11, 21, 31, 41, 51, 61,
#     72,  1, 11, 21, 31, 41, 51, 61, 71,
#      1, 11, 21, 31, 41, 51, 61, 71, 81
    6, 10,15,20, 1,
    10,15,20, 1, 7,
    15,20, 1, 7,13,
    20, 1, 7,13,19,
     1, 7,13,19,25,
]
##TODO 128
BB_L45_ATTACKS = [[BB_VOID for i in range(8)] for k in SQUARES]
BB_R45_ATTACKS = [[BB_VOID for i in range(8)] for k in SQUARES]

for s in SQUARES:
    for b in range(0, 8):
        mask = BB_VOID
        ## s : 0, 1, ..., 24
        q = s
        ## q : 0, 1, ..., 24
        ## rank_index(q) : 3 #, #, #, #, 
        ## rank_index(q) : 2 #, #, #, #, 
        ## rank_index(q) : 1 #, #, #, #, 
        ## file_index(q) : 0, 1, 2, 3, 4
        while file_index(q) > 0 and rank_index(q) < 4:
            q += 4
            mask |= BB_SQUARES[q]
            if b & (BB_SQUARES_L45[q] >> BB_SHIFT_L45[s]):
                break

        q = s
        while file_index(q) < 4 and rank_index(q) > 0:
            q -= 4
            mask |= BB_SQUARES[q]
            if b & (BB_SQUARES_L45[q] >> BB_SHIFT_L45[s]):
                break

        BB_L45_ATTACKS[s][b] = mask

        mask = BB_VOID

        q = s
        while file_index(q) < 4 and rank_index(q) < 4:
            q += 6
            mask |= BB_SQUARES[q]
            if b & (BB_SQUARES_R45[q] >> BB_SHIFT_R45[s]):
                break

        q = s
        while file_index(q) > 0 and rank_index(q) > 0:
            q -= 6
            mask |= BB_SQUARES[q]
            if b & (BB_SQUARES_R45[q] >> BB_SHIFT_R45[s]):
                break

        BB_R45_ATTACKS[s][b] = mask

try:
    from gmpy2 import popcount as pop_count
    from gmpy2 import bit_scan1 as bit_scan
except ImportError:
    try:
        from gmpy import popcount as pop_count
        from gmpy import scan1 as bit_scan
    except ImportError:
        def pop_count(b):
            return bin(b).count('1')

        def bit_scan(b, n=0):
            string = bin(b)
            l = len(string)
            r = string.rfind('1', 0, l - n)
            if r == -1:
                return -1
            else:
                return l - r - 1

def can_promote(square, piece_type, color):
    if piece_type not in [PAWN, SILVER, BISHOP, ROOK]:
        return False
    elif color == BLACK:
        return rank_index(square) == 0
    else:
        return rank_index(square) == 4

def can_move_without_promotion(to_square, piece_type, color):
    if color == BLACK:
        return ((piece_type != PAWN) or
                (piece_type == PAWN and rank_index(to_square) > 0))
    else:
        return ((piece_type != PAWN) or
                (piece_type == PAWN and rank_index(to_square) < 4))


class Occupied(object):
    def __init__(self, occupied_by_black, occupied_by_white):
        self.by_color = [occupied_by_black, occupied_by_white]
        self.bits = occupied_by_black | occupied_by_white
        self.l45 = BB_VOID
        self.r45 = BB_VOID
        self.l90 = BB_VOID
        self.update_rotated()

    def update_rotated(self):
        for i in SQUARES:
            if BB_SQUARES[i] & self.bits:
                self.l90 |= BB_SQUARES_L90[i]
                self.r45 |= BB_SQUARES_R45[i]
                self.l45 |= BB_SQUARES_L45[i]

    def __getitem__(self, key):
        if key in COLORS:
            return self.by_color[key]
        raise KeyError('Occupied must be looked up with shogi.BLACK or shogi.WHITE')

    def ixor(self, mask, color, square):
        self.bits ^= mask
        self.by_color[color] ^= mask
        self.l90 ^= BB_SQUARES[SQUARES_L90[square]]
        self.r45 ^= BB_SQUARES[SQUARES_R45[square]]
        self.l45 ^= BB_SQUARES[SQUARES_L45[square]]

    def non_occupied(self):
        return ~self.bits & BB_ALL

    def __eq__(self, occupied):
        return not self.__ne__(occupied)

    def __ne__(self, occupied):
        if self.by_color[BLACK] != occupied.by_color[BLACK]:
            return True
        if self.by_color[WHITE] != occupied.by_color[WHITE]:
            return True
        return False

    def __repr__(self):
        return 'Occupied({0})'.format(repr(self.by_color))


class Board(object):
    '''
    A bitboard and additional information representing a position.
    Provides move generation, validation, parsing, attack generation,
    game end detection, move counters and the capability to make and unmake
    moves.
    The bitboard is initialized to the starting position, unless otherwise
    specified in the optional `sfen` argument.
    '''

    def __init__(self, sfen=None):
        self.pseudo_legal_moves = PseudoLegalMoveGenerator(self)
        self.legal_moves = LegalMoveGenerator(self)

        if sfen is None:
            self.reset()
        else:
            self.set_sfen(sfen)

    def reset(self):
        '''Restores the starting position.'''
        self.piece_bb = [
                BB_VOID,                        # NONE
                BB_B1 | BB_D5,                  # PAWN
                BB_A3 | BB_E3,                  # SILVER
                BB_A2 | BB_E4,                  # GOLD
                BB_A4 | BB_E2,                  # BISHOP
                BB_A5 | BB_E1,                  # ROOK
                BB_A1 | BB_E5,                  # KING
                BB_VOID,                        # PROM_PAWN
                BB_VOID,                        # PROM_SILVER
                BB_VOID,                        # PROM_BISHOP
                BB_VOID,                        # PROM_ROOK
        ]

        self.pieces_in_hand = [collections.Counter(), collections.Counter()]

        self.occupied = Occupied(BB_D5 | BB_RANK_E, BB_RANK_A | BB_B1)

        self.king_squares = [E5, A1]
        self.pieces = [NONE for i in SQUARES]

        for i in SQUARES:
            mask = BB_SQUARES[i]
            for piece_type in PIECE_TYPES:
                if mask & self.piece_bb[piece_type]:
                    self.pieces[i] = piece_type

        self.turn = BLACK
        self.move_number = 1
        self.captured_piece_stack = collections.deque()
        self.move_stack = collections.deque()
        self.incremental_zobrist_hash = self.board_zobrist_hash(DEFAULT_RANDOM_ARRAY)
        self.transpositions = collections.Counter((self.zobrist_hash(), ))

    def clear(self):
        self.piece_bb = [
                BB_VOID,                       # NONE
                BB_VOID,                       # PAWN
                BB_VOID,                       # SILVER
                BB_VOID,                       # GOLD
                BB_VOID,                       # BISHOP
                BB_VOID,                       # ROOK
                BB_VOID,                       # KING
                BB_VOID,                       # PROM_PAWN
                BB_VOID,                       # PROM_SILVER
                BB_VOID,                       # PROM_BISHOP
                BB_VOID,                       # PROM_ROOK
        ]

        self.pieces_in_hand = [collections.Counter(), collections.Counter()]

        self.occupied = Occupied(BB_VOID, BB_VOID)

        self.king_squares = [None, None]
        self.pieces = [NONE for i in SQUARES]

        self.turn = BLACK
        self.move_number = 1
        self.captured_piece_stack = collections.deque()
        self.move_stack = collections.deque()
        self.incremental_zobrist_hash = self.board_zobrist_hash(DEFAULT_RANDOM_ARRAY)
        self.transpositions = collections.Counter((self.zobrist_hash(), ))

    def piece_at(self, square):
        '''Gets the piece at the given square.'''
        mask = BB_SQUARES[square]
        color = int(bool(self.occupied[WHITE] & mask))

        piece_type = self.piece_type_at(square)
        if piece_type:
            return Piece(piece_type, color)

    def piece_type_at(self, square):
        '''Gets the piece type at the given square.'''
        return self.pieces[square]

    def add_piece_into_hand(self, piece_type, color, count=1):
        p = self.pieces_in_hand[color]
        if piece_type >= PROM_PAWN:
            piece_type = PIECE_PROMOTED.index(piece_type)
        p[piece_type] += count

    def remove_piece_from_hand(self, piece_type, color):
        p = self.pieces_in_hand[color]
        if piece_type >= PROM_PAWN:
            piece_type = PIECE_PROMOTED.index(piece_type)
        p[piece_type] -= 1
        if p[piece_type] == 0:
            del p[piece_type]
        elif p[piece_type] < 0:
            raise ValueError('The piece is not in hand: {0}'.format(Piece(piece_type, self.turn)))

    def has_piece_in_hand(self, piece_type, color):
        if piece_type >= PROM_PAWN:
            piece_type = PIECE_PROMOTED.index(piece_type)
        return piece_type in self.pieces_in_hand[color]

    def remove_piece_at(self, square, into_hand=False):
        '''Removes a piece from the given square if present.'''
        piece_type = self.piece_type_at(square)

        if piece_type == NONE:
            return

        if into_hand:
            self.add_piece_into_hand(piece_type, self.turn)

        mask = BB_SQUARES[square]

        self.piece_bb[piece_type] ^= mask

        color = int(bool(self.occupied[WHITE] & mask))

        self.pieces[square] = NONE
        self.occupied.ixor(mask, color, square)

        # Update incremental zobrist hash.
        if color == BLACK:
            piece_index = (piece_type - 1) * 2
        else:
            piece_index = (piece_type - 1) * 2 + 1
        self.incremental_zobrist_hash ^= DEFAULT_RANDOM_ARRAY[25 * piece_index + 5 * rank_index(square) + file_index(square)]

    def set_piece_at(self, square, piece, from_hand=False, into_hand=False):
        '''Sets a piece at the given square. An existing piece is replaced.'''
        if from_hand:
            self.remove_piece_from_hand(piece.piece_type, self.turn)

        self.remove_piece_at(square, into_hand)

        self.pieces[square] = piece.piece_type

        mask = BB_SQUARES[square]

        piece_type = piece.piece_type

        self.piece_bb[piece_type] |= mask

        if piece_type == KING:
            self.king_squares[piece.color] = square

        self.occupied.ixor(mask, piece.color, square)

        # Update incremental zorbist hash.
        if piece.color == BLACK:
            piece_index = (piece.piece_type - 1) * 2
        else:
            piece_index = (piece.piece_type - 1) * 2 + 1
        self.incremental_zobrist_hash ^= DEFAULT_RANDOM_ARRAY[25 * piece_index + 5 * rank_index(square) + file_index(square)]

    def generate_pseudo_legal_moves(self, pawns=True, silvers=True, golds=True,
            bishops=True, rooks=True,
            kings=True,
            prom_pawns=True, prom_silvers=True, prom_bishops=True, prom_rooks=True,
            pawns_drop=True, silvers_drop=True, golds_drop=True,
            bishops_drop=True, rooks_drop=True):

        move_flags = [False,
                      pawns, silvers,
                      golds, bishops, rooks,
                      kings,
                      prom_pawns, prom_silvers,
                      prom_bishops, prom_rooks]
        drop_flags = [False,
                      pawns_drop, silvers_drop,
                      golds_drop, bishops_drop, rooks_drop]

        for piece_type in PIECE_TYPES:
            # piece move
            if move_flags[piece_type]:
                movers = self.piece_bb[piece_type] & self.occupied[self.turn]
                from_square = bit_scan(movers)

                while from_square != -1 and from_square is not None:
                    moves = Board.attacks_from(piece_type, from_square, self.occupied, self.turn) & ~self.occupied[self.turn]
                    to_square = bit_scan(moves)
                    while to_square != - 1 and to_square is not None:
                        if can_move_without_promotion(to_square, piece_type, self.turn):
                            yield Move(from_square, to_square)
                        if can_promote(from_square, piece_type, self.turn) or can_promote(to_square, piece_type, self.turn):
                            yield Move(from_square, to_square, True)
                        to_square = bit_scan(moves, to_square + 1)
                    from_square = bit_scan(movers, from_square + 1)

        # Drop pieces in hand.
        moves = self.occupied.non_occupied()
        to_square = bit_scan(moves)

        while to_square != -1 and to_square is not None:
            for piece_type in range(PAWN, KING):
                # Check having the piece in hand, can move after place
                # and double pawn
                if drop_flags[piece_type] and self.has_piece_in_hand(piece_type, self.turn) and \
                        can_move_without_promotion(to_square, piece_type, self.turn) and \
                        not self.is_double_pawn(to_square, piece_type):
                    yield Move(None, to_square, False, piece_type)

            to_square = bit_scan(moves, to_square + 1)

    def is_attacked_by(self, color, square, piece_types=PIECE_TYPES):
        if square is None:
            return False

        for piece_type in piece_types:
            is_attacked = Board.attacks_from(piece_type, square, self.occupied, color ^ 1) & self.piece_bb[piece_type] & self.occupied[color]
            if is_attacked:
                return True

        return False

    def attacker_mask(self, color, square):
        attackers = BB_VOID
        for piece_type in PIECE_TYPES:
            attackers |= Board.attacks_from(piece_type, square, self.occupied, color ^ 1) & self.piece_bb[piece_type]
        return attackers & self.occupied[color]

    def attackers(self, color, square):
        return SquareSet(self.attacker_mask(color, square))

    def is_check(self):
        return self.is_attacked_by(self.turn ^ 1, self.king_squares[self.turn])

    @staticmethod
    def attacks_from(piece_type, square, occupied, move_color):
        if piece_type == NONE:
            return BB_VOID
        if piece_type == PAWN:
            return BB_PAWN_ATTACKS[move_color][square]
        elif piece_type == SILVER:
            return BB_SILVER_ATTACKS[move_color][square]
        elif piece_type in [GOLD, PROM_PAWN, PROM_SILVER]:
            return BB_GOLD_ATTACKS[move_color][square]
        elif piece_type == BISHOP:
            return (BB_R45_ATTACKS[square][(occupied.r45 >> BB_SHIFT_R45[square]) & 7] |
                    BB_L45_ATTACKS[square][(occupied.l45 >> BB_SHIFT_L45[square]) & 7])
        elif piece_type == ROOK:
            return (BB_RANK_ATTACKS[square][(occupied.bits >> (((square // 5) * 5) + 1)) & 7] |
                    BB_FILE_ATTACKS[square][(occupied.l90 >> (((square % 5) * 5) + 1)) & 7])
        elif piece_type == KING:
            return BB_KING_ATTACKS[square]
        elif piece_type == PROM_BISHOP:
            return (BB_KING_ATTACKS[square] |
                    BB_R45_ATTACKS[square][(occupied.r45 >> BB_SHIFT_R45[square]) & 7] |
                    BB_L45_ATTACKS[square][(occupied.l45 >> BB_SHIFT_L45[square]) & 7])
        elif piece_type == PROM_ROOK:
            return (BB_KING_ATTACKS[square] |
                    BB_RANK_ATTACKS[square][(occupied.bits >> (((square // 5) * 5) + 1)) & 7] |
                    BB_FILE_ATTACKS[square][(occupied.l90 >> (((square % 5) * 5) + 1)) & 7])

    def is_suicide_or_check_by_dropping_pawn(self, move):
        '''
        Checks if the given move would move would leave the king in check or
        put it into check.
        '''

        self.push(move)
        is_suicide = self.was_suicide()
        is_check_by_dropping_pawn = self.was_check_by_dropping_pawn(move)
        self.pop()
        return is_suicide or is_check_by_dropping_pawn

    def was_suicide(self):
        '''
        Checks if the king of the other side is attacked. Such a position is not
        valid and could only be reached by an illegal move.
        '''
        return self.is_attacked_by(self.turn, self.king_squares[self.turn ^ 1])

    def was_check_by_dropping_pawn(self, move):
        # NOTE: We ignore the case "Saigo no shinpan" (by Koji Nuita, 1997)
        # We don't use is_checkmate() because it's slow due to generating all leagl moves
        # And we don't consider suicide of a king.

        pawn_square = move.to_square

        # Pawn is dropped?
        if move.drop_piece_type != PAWN:
            return False

        king_square = self.king_squares[self.turn]

        # Does king exist?
        if king_square is None:
            return False

        # Pawn can capture a king next move?
        moves = BB_PAWN_ATTACKS[self.turn ^ 1][pawn_square] & ~self.occupied[self.turn ^ 1]
        if not moves & BB_SQUARES[king_square]:
            return False

        # Can king escape? (including capturing a dropped pawn)
        moves = Board.attacks_from(KING, king_square, self.occupied, self.turn) & ~self.occupied[self.turn]
        square = bit_scan(moves)
        while square != -1 and square is not None:
            if not self.is_attacked_by(self.turn ^ 1, square):
                return False
            square = bit_scan(moves, square + 1)

        # Pieces besides king can capture the pawn?
        if self.is_attacked_by(self.turn, pawn_square, PIECE_TYPES_WITHOUT_KING):
            return False

        return True

    def generate_legal_moves(self, pawns=True, silvers=True, golds=True, bishops=True,
            rooks=True, king=True,
            pawns_drop=True, silvers_drop=True, golds_drop=True,
            bishops_drop=True, rooks_drop=True):
        return (move for move in self.generate_pseudo_legal_moves(
                pawns, silvers, golds, bishops, rooks, king,
                pawns_drop, silvers_drop, golds_drop, bishops_drop, rooks_drop
            ) if not self.is_suicide_or_check_by_dropping_pawn(move))

    def is_pseudo_legal(self, move):
        # Null moves are not pseudo legal.
        if not move:
            return False

        # Get square masks of the move destination.
        to_mask = BB_SQUARES[move.to_square]

        # Destination square can not be occupied by self.
        if self.occupied[self.turn] & to_mask:
            return False

        if move.from_square is not None:
            from_mask = BB_SQUARES[move.from_square]
            # Source square must not be vacant.
            piece = self.piece_type_at(move.from_square)
            if not piece:
                return False
            # Check turn.
            if not self.occupied[self.turn] & from_mask:
                return False

            # Promotion check
            if move.promotion:
                if piece == GOLD or piece == KING or piece >= PROM_PAWN:
                    return False
                if self.turn == BLACK and rank_index(move.to_square) > 2 and rank_index(move.from_square) > 2:
                    return False
                elif self.turn == WHITE and rank_index(move.to_square) < 6 and rank_index(move.from_square) < 6:
                    return False

            # Can move without promotion
            if not move.promotion and not can_move_without_promotion(move.to_square, piece, self.turn):
                return False

            # Handle moves by piece type.
            return bool(Board.attacks_from(piece, move.from_square, self.occupied, self.turn) & to_mask)
        elif move.drop_piece_type:
            # Cannot set promoted piece
            if move.promotion:
                return False

            # Have a piece in hand
            if not self.has_piece_in_hand(move.drop_piece_type, self.turn):
                return False

            # Can move without promotion
            if not can_move_without_promotion(move.to_square, move.drop_piece_type, self.turn):
                return False

            # Not double pawn
            if self.is_double_pawn(move.to_square, move.drop_piece_type):
                return False

            return True
        else:
            # Drop piece or move piece
            return False

    def is_legal(self, move):
        return self.is_pseudo_legal(move) and not self.is_suicide_or_check_by_dropping_pawn(move)

    def is_game_over(self):
        '''
        Checks if the game is over due to checkmate, stalemate or
        fourfold repetition.
        '''

        # Stalemate or checkmate.
        try:
            next(self.generate_legal_moves().__iter__())
        except StopIteration:
            return True

        # Fourfold repetition.
        if self.is_fourfold_repetition():
            return True

        return False

    def is_checkmate(self):
        '''Checks if the current position is a checkmate.'''
        if not self.is_check():
            return False

        try:
            next(self.generate_legal_moves().__iter__())
            return False
        except StopIteration:
            return True

    def is_stalemate(self):
        '''Checks if the current position is a stalemate.'''
        if self.is_check():
            return False

        try:
            next(self.generate_legal_moves().__iter__())
            return False
        except StopIteration:
            return True

    def is_fourfold_repetition(self):
        '''
        a game is ended if a position occurs for the fourth time
        on consecutive alternating moves.
        '''
        zobrist_hash = self.zobrist_hash()

        # A minimum amount of moves must have been played and the position
        # in question must have appeared at least four times.
        if self.transpositions[zobrist_hash] < 4:
            return False

        return True

    def is_double_pawn(self, to_square, piece_type):
        if piece_type != PAWN:
            return False
        return self.piece_bb[PAWN] & self.occupied[self.turn] & BB_FILES[file_index(to_square)]

    def push_usi_position_cmd(self, usi_position_cmd):
        '''
        Updates the position from position command in USI protocol.

        Example:
        >>> board.push_usi_position_cmd("position startpos moves 7g7f 3c3d")
        '''
        if usi_position_cmd.startswith("position startpos") or usi_position_cmd.startswith("position sfen"):
            sfen_id = usi_position_cmd.find("sfen")
            moves_id = usi_position_cmd.find("moves")
        else:
            raise ValueError("Invalid command {0} position cmd in USI protocol must starts from 'position startpos' or 'position sfen'".format(repr(usi_position_cmd)))

        if sfen_id != -1:
            if moves_id != -1:
                sfen = usi_position_cmd[sfen_id+5:moves_id]
            else:
                sfen = usi_position_cmd[sfen_id+5:]
            self.set_sfen(sfen)
        else:
            self.reset()

        if moves_id != -1:
            moves = usi_position_cmd[moves_id+6:].split(" ")
            for move in moves:
                if move != "":
                    self.push_usi(move)

    def push(self, move):
        '''
        Updates the position with the given move and puts it onto a stack.
        Null moves just increment the move counters, switch turns and forfeit
        en passant capturing.
        No validation is performed. For performance moves are assumed to be at
        least pseudo legal. Otherwise there is no guarantee that the previous
        board state can be restored. To check it yourself you can use:
        >>> move in board.pseudo_legal_moves
        True
        '''
        # Increment move number.
        self.move_number += 1

        # Remember game state.
        captured_piece = self.piece_type_at(move.to_square) if move else NONE
        self.captured_piece_stack.append(captured_piece)
        self.move_stack.append(move)

        # On a null move simply swap turns.
        if not move:
            self.turn ^= 1
            return

        if move.drop_piece_type:
            # Drops.
            piece_type = move.drop_piece_type
            from_hand = True
        else:
            # Promotion.
            piece_type = self.piece_type_at(move.from_square)
            from_hand = False

            if move.promotion:
                piece_type = PIECE_PROMOTED[piece_type]

            # Remove piece from target square.
            self.remove_piece_at(move.from_square, False)

        # Put piece on target square.
        self.set_piece_at(move.to_square, Piece(piece_type, self.turn), from_hand, True)

        # Swap turn.
        self.turn ^= 1

        # Update transposition table.
        self.transpositions.update((self.zobrist_hash(), ))

    def pop(self):
        '''
        Restores the previous position and returns the last move from the stack.
        '''
        move = self.move_stack.pop()

        # Update transposition table.
        self.transpositions.subtract((self.zobrist_hash(), ))

        # Decrement move number.
        self.move_number -= 1

        # Restore state.
        captured_piece_type = self.captured_piece_stack.pop()
        captured_piece_color = self.turn

        # On a null move simply swap the turn.
        if not move:
            self.turn ^= 1
            return move

        # Restore the source square.
        piece_type = self.piece_type_at(move.to_square)
        if move.promotion:
            piece_type = PIECE_PROMOTED.index(piece_type)

        if move.from_square is None:
            self.add_piece_into_hand(piece_type, self.turn ^ 1)
        else:
            self.set_piece_at(move.from_square, Piece(piece_type, self.turn ^ 1))

        # Restore target square.
        if captured_piece_type:
            self.remove_piece_from_hand(captured_piece_type, captured_piece_color ^ 1)
            self.set_piece_at(move.to_square, Piece(captured_piece_type, captured_piece_color))
        else:
            self.remove_piece_at(move.to_square)

        # Swap turn.
        self.turn ^= 1

        return move

    def peek(self):
        '''Gets the last move from the move stack.'''
        return self.move_stack[-1]

    def sfen(self):
        '''
        Gets an SFEN representation of the current position.
        '''
        sfen = []
        empty = 0

        # Position part.
        for square in SQUARES:
            piece = self.piece_at(square)

            if not piece:
                empty += 1
            else:
                if empty:
                    sfen.append(str(empty))
                    empty = 0
                sfen.append(piece.symbol())

            if BB_SQUARES[square] & BB_FILE_1:
                if empty:
                    sfen.append(str(empty))
                    empty = 0

                if square != E1:
                    sfen.append('/')

        sfen.append(' ')

        # Side to move.
        if self.turn == WHITE:
            sfen.append('w')
        else:
            sfen.append('b')

        sfen.append(' ')

        # Pieces in hand
        pih_len = 0
        for color in COLORS:
            p = self.pieces_in_hand[color]
            pih_len += len(p)
            for piece_type in sorted(p.keys(), reverse=True):
                if p[piece_type] >= 1:
                    if p[piece_type] > 1:
                        sfen.append(str(p[piece_type]))
                    piece = Piece(piece_type, color)
                    sfen.append(piece.symbol())
        if pih_len == 0:
            sfen.append('-')

        sfen.append(' ')

        # Move count
        sfen.append(str(self.move_number))

        return ''.join(sfen)

    def set_sfen(self, sfen):
        '''
        Parses a SFEN and sets the position from it.
        Rasies `ValueError` if the SFEN string is invalid.
        '''
        # Ensure there are six parts.
        parts = sfen.split()
        if len(parts) != 4:
            raise ValueError('sfen string should consist of 6 parts: {0}'.format(repr(sfen)))

        # Ensure the board part is valid.
        rows = parts[0].split('/')
        if len(rows) != 5:
            raise ValueError('expected 5 rows in position part of sfen: {0}'.format(repr(sfen)))

        # Validate each row.
        for row in rows:
            field_sum = 0
            previous_was_digit = False
            previous_was_plus = False

            for c in row:
                if c in ['1', '2', '3', '4', '5']:
                    if previous_was_digit:
                        raise ValueError('two subsequent digits in position part of sfen: {0}'.format(repr(sfen)))
                    if previous_was_plus:
                        raise ValueError('Cannot promote squares in position part of sfen: {0}'.format(repr(sfen)))
                    field_sum += int(c)
                    previous_was_digit = True
                    previous_was_plus = False
                elif c == '+':
                    if previous_was_plus:
                        raise ValueError('Double promotion prefixes in position part of sfen: {0}'.format(repr(sfen)))
                    previous_was_digit = False
                    previous_was_plus = True
                elif c.lower() in ['p', 's', 'g', 'b', 'r', 'k']:
                    field_sum += 1
                    if previous_was_plus and (c.lower() == 'g' or c.lower() == 'k'):
                      raise ValueError('Gold and King cannot promote in position part of sfen: {0}')
                    previous_was_digit = False
                    previous_was_plus = False
                else:
                    raise ValueError('invalid character in position part of sfen: {0}'.format(repr(sfen)))

            if field_sum != 5:
                raise ValueError('expected 5 columns per row in position part of sfen: {0}'.format(repr(sfen)))

        # Check that the turn part is valid.
        if not parts[1] in ['b', 'w']:
            raise ValueError("expected 'b' or 'w' for turn part of sfen: {0}".format(repr(sfen)))

        # Check pieces in hand is valid.
        # TODO: implement with checking parts[2]

        # Check that the fullmove number part is valid.
        # 0 is allowed for compability but later replaced with 1.
        if int(parts[3]) < 0:
            raise ValueError('fullmove number must be positive: {0}'.format(repr(sfen)))

        # Clear board.
        self.clear()

        # Put pieces on the board.
        square_index = 0
        previous_was_plus = False
        for c in parts[0]:
            if c in ['1', '2', '3', '4', '5']:
                square_index += int(c)
            elif c == '+':
                previous_was_plus = True
            elif c == '/':
                pass
            else:
                piece_symbol = c
                if previous_was_plus:
                  piece_symbol = '+' + piece_symbol
                self.set_piece_at(square_index, Piece.from_symbol(piece_symbol))
                square_index += 1
                previous_was_plus = False

        # Set the turn.
        if parts[1] == 'w':
            self.turn = WHITE
        else:
            self.turn = BLACK

        # Set the pieces in hand
        self.pieces_in_hand = [collections.Counter(), collections.Counter()]
        if parts[2] != '-':
            piece_count = 0
            for c in parts[2]:
                if c in ['0', '1', '2', '3', '4', '5']:
                    ## TODO HAN
                    piece_count *= 10
                    piece_count += int(c)
                else:
                    piece = Piece.from_symbol(c)
                    if piece_count == 0:
                        piece_count = 1
                    self.add_piece_into_hand(piece.piece_type, piece.color, piece_count)
                    piece_count = 0

        # Set the mover counters.
        self.move_number = int(parts[3]) or 1

        # Reset the transposition table.
        self.transpositions = collections.Counter((self.zobrist_hash(), ))

    def push_usi(self, usi):
        '''
        Parses a move in standard coordinate notation, makes the move and puts
        it on the the move stack.
        Raises `ValueError` if neither legal nor a null move.
        Returns the move.
        '''
        move = Move.from_usi(usi)
        self.push(move)
        return move

    def kif_pieces_in_hand_str(self, color):
        builder = [[
            '先手の持駒：',
            '後手の持駒：',
        ][color]]

        for piece_type in range(ROOK, NONE, -1):
            if self.has_piece_in_hand(piece_type, color):
                piece_count = self.pieces_in_hand[color][piece_type]
                if piece_count:
                    builder.append('　')
                    piece = Piece(piece_type, color)
                    builder.append(piece.japanese_symbol())
                    if piece_count > 1:
                        builder.append(NUMBER_JAPANESE_KANJI_SYMBOLS[piece_count])

        return ''.join(builder)


    def kif_str(self):
        builder = []

        builder.append(self.kif_pieces_in_hand_str(WHITE))

        builder.append('\n ')
        for file_num in range(5, 0, -1):
            builder.append(' ')
            builder.append(NUMBER_JAPANESE_NUMBER_SYMBOLS[file_num])
        builder.append('\n+---------------------------+\n')

        for square in SQUARES:
            piece = self.piece_at(square)

            if BB_SQUARES[square] & BB_FILE_5:
                builder.append('|')

            if piece:
                builder.append(piece.japanese_symbol_with_direction())
            else:
                builder.append(' ・')

            if BB_SQUARES[square] & BB_FILE_1:
                builder.append('|')
                builder.append(NUMBER_JAPANESE_KANJI_SYMBOLS[rank_index(square) + 1])
                builder.append('\n')

        builder.append('+---------------------------+\n')

        builder.append(self.kif_pieces_in_hand_str(BLACK))

        return ''.join(builder)

    def __repr__(self):
        return "Board('{0}')".format(self.sfen())

    def __str__(self):
        builder = []

        for square in SQUARES:
            piece = self.piece_at(square)

            if piece:
                if not piece.is_promoted():
                    builder.append(' ')
                builder.append(piece.symbol())
            else:
                builder.append(' .')

            if BB_SQUARES[square] & BB_FILE_1:
                if square != E1:
                    builder.append('\n')
            else:
                builder.append(' ')

        if len(self.pieces_in_hand[BLACK]) + len(self.pieces_in_hand[WHITE]) > 0:
            builder.append('\n\n')

            # pieces in hand
            for color in COLORS:
                for piece_type, piece_count in self.pieces_in_hand[color].items():
                    builder.append(' ')
                    piece = Piece(piece_type, color)
                    builder.append(piece.symbol())
                    builder.append('*')
                    builder.append(str(piece_count))

        return ''.join(builder)

    def __eq__(self, board):
        return not self.__ne__(board)

    def __ne__(self, board):
        try:
            if self.occupied != board.occupied:
                return True
            if self.piece_bb != board.piece_bb:
                return True
            if self.pieces_in_hand != board.pieces_in_hand:
                return True
            if self.turn != board.turn:
                return True
            if self.move_number != board.move_number:
                return True
        except AttributeError:
            return True

        return False

    def zobrist_hash(self, array=None):
        '''
        Returns a Zobrist hash of the current position.
        '''
        # Hash in the board setup.
        zobrist_hash = self.board_zobrist_hash(array)

        if array is None:
            array = DEFAULT_RANDOM_ARRAY

        if self.turn == WHITE:
            ## TODO HAN
            zobrist_hash ^= array[316]

        # pieces in hand pattern is
        # 19 * 5 * 5 * 5 * 5 * 3 * 3 = 106875 < pow(2, 17)
        # 3 * 3 * 3 * 3 * 3 = 81 < pow(2, 7)
        # just checking black side is okay in normal state
        i = (
                self.pieces_in_hand[BLACK][ROOK] * 81 +
                self.pieces_in_hand[BLACK][BISHOP] * 27 +
                self.pieces_in_hand[BLACK][GOLD] * 9 +
                self.pieces_in_hand[BLACK][SILVER] * 3 +
                self.pieces_in_hand[BLACK][PAWN])
        bit = bit_scan(i)
        while bit != -1 and bit is not None:
            zobrist_hash ^= array[317 + bit]
            bit = bit_scan(i, bit + 1)

        return zobrist_hash

    def board_zobrist_hash(self, array=None):
        if array is None:
            return self.incremental_zobrist_hash

        zobrist_hash = 0

        squares = self.occupied[BLACK]
        square = bit_scan(squares)
        while square != -1 and square is not None:
            piece_index = (self.piece_type_at(square) - 1) * 2
            zobrist_hash ^= array[25 * piece_index + 5 * rank_index(square) + file_index(square)]
            square = bit_scan(squares, square + 1)

        squares = self.occupied[WHITE]
        square = bit_scan(squares)
        while square != -1 and square is not None:
            piece_index = (self.piece_type_at(square) - 1) * 2 + 1
            zobrist_hash ^= array[25 * piece_index + 5 * rank_index(square) + file_index(square)]
            square = bit_scan(squares, square + 1)

        return zobrist_hash


class PseudoLegalMoveGenerator(object):

    def __init__(self, board):
        self.board = board

    def __bool__(self):
        try:
            next(self.board.generate_pseudo_legal_moves())
            return True
        except StopIteration:
            return False

    __nonzero__ = __bool__

    # TODO: Counting without generating actual moves
    def __len__(self):
        return sum(1 for _ in self)

    def __iter__(self):
        return self.board.generate_pseudo_legal_moves()

    def __contains__(self, move):
        return self.board.is_pseudo_legal(move)


class LegalMoveGenerator(object):

    def __init__(self, board):
        self.board = board

    def __bool__(self):
        try:
            next(self.board.generate_legal_moves())
            return True
        except StopIteration:
            return False

    __nonzero__ = __bool__

    def __len__(self):
        count = 0

        for move in self.board.generate_legal_moves():
            count += 1

        return count

    def __iter__(self):
        return self.board.generate_legal_moves()

    def __contains__(self, move):
        return self.board.is_legal(move)


class SquareSet(object):

    def __init__(self, mask):
        self.mask = mask

    def __bool__(self):
        return bool(self.mask)

    __nonzero__ = __bool__

    def __eq__(self, other):
        try:
            return int(self) == int(other)
        except ValueError:
            return False

    def __ne__(self, other):
        try:
            return int(self) != int(other)
        except ValueError:
            return False

    def __len__(self):
        return pop_count(self.mask)

    def __iter__(self):
        square = bit_scan(self.mask)
        while square != -1 and square is not None:
            yield square
            square = bit_scan(self.mask, square + 1)

    def __contains__(self, square):
        return bool(BB_SQUARES[square] & self.mask)

    def __lshift__(self, shift):
        return self.__class__((self.mask << shift) & BB_ALL)

    def __rshift__(self, shift):
        return self.__class__(self.mask >> shift)

    def __and__(self, other):
        try:
            return self.__class__(self.mask & other.mask)
        except AttributeError:
            return self.__class__(self.mask & other)

    def __xor__(self, other):
        try:
            return self.__class__((self.mask ^ other.mask) & BB_ALL)
        except AttributeError:
            return self.__class__((self.mask ^ other) & BB_ALL)

    def __or__(self, other):
        try:
            return self.__class__((self.mask | other.mask) & BB_ALL)
        except AttributeError:
            return self.__class__((self.mask | other) & BB_ALL)

    def __ilshift__(self, shift):
        self.mask = (self.mask << shift & BB_ALL)
        return self

    def __irshift__(self, shift):
        self.mask >>= shift
        return self

    def __iand__(self, other):
        try:
            self.mask &= other.mask
        except AttributeError:
            self.mask &= other
        return self

    def __ixor__(self, other):
        try:
            self.mask = (self.mask ^ other.mask) & BB_ALL
        except AttributeError:
            self.mask = (self.mask ^ other) & BB_ALL
        return self

    def __ior__(self, other):
        try:
            self.mask = (self.mask | other.mask) & BB_ALL
        except AttributeError:
            self.mask = (self.mask | other) & BB_ALL
        return self

    def __invert__(self):
        return self.__class__(~self.mask & BB_ALL)

    def __oct__(self):
        return oct(self.mask)

    def __hex__(self):
        return hex(self.mask)

    def __int__(self):
        return self.mask

    def __index__(self):
        return self.mask

    def __repr__(self):
        return 'SquareSet({0})'.format(bin(self.mask))

    def __str__(self):
        builder = []

        for square in SQUARES:
            mask = BB_SQUARES[square]

            if self.mask & mask:
                builder.append('1')
            else:
                builder.append('.')

            if mask & BB_FILE_1:
                if square != E1:
                    builder.append('\n')
            else:
                builder.append(' ')

        return ''.join(builder)

    def __hash__(self):
        return self.mask

# 81 * (14 piece types * (white or black) - 1) + 9 * (ranks - 1) + (files - 1) + ((white or black) - 1) + (current turn) + log2((19 pawn in hand) * (5 lance in hand) * (5 knight in hand) * (5 silver in hand) * (5 gold in hand) * (3 bishop) * (3 rook))
#  = 2268 + 1 + 17 = 2286
# print(25 * (10 * 2 - 1) + 5 * (5 - 1) + (5 - 1) + (2 - 1)  + (1) + math.log2(3 * 3 * 3 * 3 * 3))

# Genetation code example:
# import random
# for i in range(2286):
#     if i % 4 == 0:
#         print '    ',
#     print '0x{0:016X},'.format(random.randint(0, 0xffffffffffffffffL)),
#     if i % 4 == 3:
#         print ''

DEFAULT_RANDOM_ARRAY = [
    0x0A82F6F3C159640B,0xB95B1031846C1C7F,0x69E32C60FD3643E3,0x381C66A41D4DF6CD,

0x4FCC7BACEDB68B00,0x7302AF66262C43C6,0x09A4B73AE746D4C4,0xAD1F87A976FC7D9C,

0xACA024799FD530FC,0x83FD4547EA1A90AF,0x536E97A9F7232E83,0x14832ECD2ADED7AE,

0x41971879E537BD93,0x2B9176693DA88BFA,0xD1DE7442388636D2,0xE238C62D02ADB2DA,

0x61D6B45F8614890B,0x1A628786CE61E55B,0xC842191B7EB5B343,0xAADDDFEE696CB11F,

0x3155594A8F643037,0x5853682E216EE7B3,0x08466AC278297E43,0x1A7FD0558334A9B3,

0x4EDDE2CFF1332134,0x4533A8F55193BF2D,0xC44350883750FC8C,0x0B5C95599BBDC428,

0x93D73DBC35E25B88,0x019985B723E78CE8,0x4FD4BA8B372AC19B,0xAA22EE53199B301C,

0xF092E1DE4F3E9B4C,0x140817965FF4F8A3,0x4712EE18A1662CE9,0x130FB5451390932B,

0x0127B33843967538,0xC66151F3A51C2EED,0x04B4EB791D2C9BB0,0x86775F6C56A636F0,

0x054C20DB1ABC1C61,0xEB8403E49BCD1DB9,0x2BA1D21A2BD9C5C6,0xE91DF9C71A6B7E74,

0xB8524D32BC019626,0x44A1DA2AE350E98A,0xB7EA85596E68362A,0x903FD02AC6BE2AE3,

0xE70369A537908E49,0x0EFB44161D7968C8,0xDAFD93AF780CDFD1,0x498CD0C10508EBC6,

0x419AB94AAC042F03,0x324ED74C40925EC1,0x1B6BE50E5B1664DD,0x00EB5C5B4F2BCE21,

0x36367AC41C5A6C63,0x2BB868DE18C2CAEA,0xB8144472FDD55DFA,0xC3186228368F7801,

0xA37A08F2C2BA0CCA,0x7059721EE4C08AA0,0x599F61A3FD854AB4,0x8CEBDB245A3A35CD,

0x1EEEC7F66F35DFCF,0xE9EEC6A436A127B5,0xD8B7A0B4719FDA9D,0x42A4965DEC8AEDE9,

0x095F44EC0B0C1290,0x878380818855D352,0xCC06E994B021A5E9,0xBDCA9860F1A6D97F,

0x9CC02C154D1F2688,0xFA9384ED2C252341,0x77B03BE32A54E80A,0x8BFAEED694F458F1,

0x4EAA89DEA9B9A30C,0xB3B686F248AA5DFB,0x94667435A30CB352,0xA92A3B7F4BDA3509,

0x75005BABE38B34B3,0xB95F44DB87B4D3B7,0x515B3519346ABB77,0xA6738DA6D0A1CC9A,

0xC42932F8D900BB6E,0xF8A20681747B062C,0x76A1951A09D7824B,0x972C0CD1C1F813AD,

0xB74E91B411CA6A24,0x63817E9392A53F90,0x9B8623D3B020F0CA,0x0F353A569095F3FA,

0xB8863A6955A0F518,0x0839ACC7D0AD8E26,0x59E511A4D6844216,0xC3ACE59741440FF6,

0xD9BA10AB348ECF52,0x62642244ABC52C0D,0x098178992AE28E45,0xB7995300170143C1,

0x348AF2D0B48A387C,0x9869AED988D87ECC,0xED90B7307CB48850,0x82C58794C295163F,

0x144B6762E533D3CD,0x4D8E12010E4EC9BA,0xB84B980C5FF46144,0xAF97EE21D0A45300,

0x59B804847B4BF71C,0x542B3641205CE84D,0x4337D06F04191862,0x116888496E89E431,

0xA3DB081738200F35,0xF34C6A301E1CDDBE,0x76B30E4B96E0AEA2,0xF0C12A3A950A4B4F,

0x3C6A9C0AE8374752,0x5E4F9132C48724C3,0x2C6B5777A9D57FCF,0x76D41F493C7FB868,

0x03B8C708A8DBFD41,0x975E23E92BFF1A57,0xEC6A847F73968333,0xE10389BDCC1AEF3E,

0x653CC5FA28DA6A57,0xD0E6C3BD670CC1E0,0x55BA9D93C1FC2F27,0x306E68EDFBCB4A44,

0x80E67030D2CAB18A,0x6A1DEDFF7CADC261,0xE179351B7F004AC5,0x5502DB4E1B3510B4,

0xE029AEE9E2D0B82B,0x502597042205E50E,0x7F94A82D8D47BD7E,0x34A475BE4F0A5428,

0x829BA020C797F83C,0x9F0719CF6843219A,0x3E6CFEE32CBF6408,0x5B8E3FD1E2AF598F,

0x82B4145C23F03E9E,0xC68C3C863ABB2A3D,0xB1FC1CB1A8536644,0x479643E8FF8C8EC2,

0x181E760D71D3E561,0xB669E82471F28793,0x0C6D41D582031024,0x4DE9095962B0AC54,

0x938806873ABB5182,0x4D667604E9F9C08F,0x41AADC7DB58CC886,0x77D258CFB08B5843,

0x1E76BC2165D13335,0xB213EF75BF303886,0x80719F3F34363A9A,0x92E743FBD3E98DEC,

0x48BF6788D3F16709,0x9612A08DDB93962A,0xEFDC31F0ECB0DF82,0x4903B88229B62F57,

0x5BAE409C265A2E5D,0x8775C10EB69ACEF4,0x0A8C7A712B3F7309,0x760B0CF4863EDAB5,

0x1857304DF4A3BAAD,0xC068116B397ABE58,0xD79166B616EE722E,0x603FA663183B628D,

0xCD798DBBB5B0A57E,0x40F33825FC6A756B,0x385AF47F44615F1A,0x67A509FC9FCE7D6A,

0x07A8609DB4E69116,0x8DF636498063E62E,0x7538DB907F451416,0x936FD02450B02D62,

0x65FE282AA335933F,0xE9796ED0AB98DB75,0x8E44651BAD9891B2,0xC811F4CC48AC1084,

0x7230C713BD3DCCC3,0xD4C9E832EF86207E,0xC29B846DDD35B3BB,0x9F1A81392648F5CD,

0xE93307A3F14F3FF5,0xECA4F1958E8C9B7A,0xF50539695E507457,0xC1081A0E51164D57,

0x604B107632FD54D9,0xCB943F66760CDD19,0xA7EA5E4C044F7830,0x58BB13CC3FE58E88,

0x009D49AC949BD95F,0x38897F4B232F89F7,0xA49C607D82CC6592,0x9D686232902EC8DC,

0x354580F97988B088,0xA70D257DF146CFC2,0x47CE683B1D54F3F5,0x6E393E92830273DE,

0x15803C333810C552,0x3BB9A60931865D4F,0xB44FDF510E40E221,0x0DEAA6F6BD2D5118,

0xA6696FB9DB950BE9,0xA764C3F06B6241E2,0xFB8E71DF066E6F55,0xF1B8BBCA01BA5A17,

0x342C5B4ACD4D41FC,0x2526C7C744EB042B,0xCA5E13B90467C648,0xBC64FD4AA204A40B,

0x0891A6C24B6F6B9B,0xD6F554FC66915D18,0xBD8513DF8E3085CC,0xAEAEAF94F53C5F9A,

0x0048A224E4B7AEF1,0x770DADF66E168DA4,0x8652147503ABF615,0x686AF49D804134CE,

0xB29E805AA988F41D,0x275E4D1206A3085F,0xD1B579200C73C187,0x522732FA4BA49B3F,

0xA11F82B1137109EF,0xDE3AD313972CCFCC,0x78C8DA39DEBD3914,0x5909B3676F3355A7,

0xE08376988F125C14,0x712BA915020210F2,0x13B73663F1487F28,0x0D6E1C107C0C43EF,

0x5B8213EBD95D1077,0x0542C90956F8CA40,0xF01FF42DA1C0F17B,0x506974D92BFCCB1A,

0xCCA11E97C0D79C8B,0x195C9D22E147EA58,0x8CA3AD0FE46748B9,0x9F844CF05E133677,

0x1F26B502FEAF648A,0x584D950B2C0FE5D5,0xC48D087FDCB38402,0xFFA93067CA929C05,

0x879C39607AEC1F14,0xBB94CC19F8A51D07,0x553A9C8B279A845C,0x94CF12B7E173616C,

0x4C53B881BF49016E,0xA25813DC296A93F9,0x975CA60C25D7A219,0x7D05F23FF88960DC,

0x8AD7FD3BC3FA66CC,0x51498002BAE678F4,0x33B9E09428625F49,0xEB712788E353A6CB,

0xECC7021D723B89C0,0x2504974020C4F381,0x31E81B5309412867,0x3386CE1E473A517C,

0xA73C3C13B15F4F2F,0x9E6B712285F3480D,0xD5E79A373ADCC6E7,0xBFDDD189AD478E0C,

0xC45492B245CCEC6A,0x70B17157C1BA014F,0x8133C73F435BC3CA,0xF1388424FB6CFFCB,

0x7C6561F2E9D7A8C7,0xE5536CC53785449E,0xCFF845D978F0CD47,0x35BF1162CB1BB6A7,

0x0E8A0DE03E1F4163,0x6957C84503897485,0x5779C6F277F16A72,0xBEFC7A44A9507F0A,

0xE61164C16F9D5267,0xF907E57FEC016488,0x7DA7011CB5CF1014,0x125105C76811F182,

0x9EC4514018022B5B,0x15ABDF0C73C5D8AA,0x4538DDC547E8EEFA,0xE5ED2D6729C97720,

0x22A09655798289B0,0xC0D058D10D6C58D6,0xCEF1818F84C9FA1E,0xA85F6F45C753471D,

0x2AB0A009219DC207,0xB817E3FBB4D7A689,0x25BDC56BCF24E3A8,0x49F29EC4F39F2D0B,

0xFFF77D24F77754FD,0x8F70F71500BCA30A,0x68556B4BC56F6E08,0x07C179DDD11AC28F,

0xB33C6F76896AD829,0x21900EDC7C8383A8,0x49FB9AB09DD25117,0x3CCA535B8E1CA84C,

0x2E78F857A266CD1A,0x10EC4ACC8F60C19C,0xED555BD8EB88AC6B,0x891E44CC92710A0C,

0xFB991119710DF573,0x419BA595EB2EC53E,0x5D12D2B95CFC4B6F,0x304C9BB159D21842,

0xF1B76AEFC442DC4D,0xA43D452F0BBEAF05,0x0D5140FA3F81D074,0xBEB2E8C64A67564C,

0x2D4A170B54542E32,0x6A83FAB2C78CCDEE,0x844FE07C258FAB07,0x049E5669F98041FC,

0xA11EBD5E3D360521,0x5122E401D894A82F,0x5B5E519F173F028F,0x610F281131DF4BA0,

0xD314690C841A4F3C,0x61542D801C4B8406,0xE48782CBA6CE3931,0x36D56222F4A28EE4,

0x5AEB5ACEC3D5C12F,0x21FF996ED993BD8B,0x88612F7ACA547C3B,0xEF55CF7C288C3A99,

0x61626E778A108677,0x1E35BEE7A1EF02E2,0xDF92BCEF42D2A1D9,0xA78CE5E947FC78F4,

0x692BB4CFFED78AB9,0x74A12968919B1AF7,0x2C3CAF6916626668,0xEDA1A4A1D56E0F97,

0x179324EB9BD7443A,0x60CE2C2CF9E892FF,0x511CD51938C3412D,0x0D4139D5912221F5,

0x80C594E855FB029E,0xCCFA972DB21D8F5A,0xF4837EC2F04F7F79,0x4E9B37812E43C226,

0xAE2285C74FAA5C4C,0xB24CB66A381741CD,0xFB0FF1937B13BF82,0xB622A3FD5DDD4F39,

0x8255A2EEFB6DB0C7,0x61914B35CDA8248C,0x9B03B7D501CDD301,0xA88D93FBC7EBEB12,

0x5EF8C43408F38EAA,0x8BC79D0CCA3CFB75,0xDDC696894431B426,0xED6994AB0FD0BAE8,

0xFB7665693C9EA9B3,0xE8F0795E247F59CE,0x7B6F2BB39FBEF809,0x890AA99198FF8296,

0xD8E113483791E23F,0xB219F834F1F1CD9E,0x49CCE961B5F70A64,0x5D8867D363A1F438,

0xC7E398BF9AEA87DC,0x4A31FE4576338779,0x9FCC8B4D923ECBD3,0x87134308913DF66C,

0x83E9DFE495155D8B,0xCD5770CDEC44D3DA,0xF4DD84D481F3EA2F,0x69781983AD28A647,

0x4ED7EF3212F0EB61,0xE18A757DE337613E,0x414A3E27B682FB97,0x4398E97923C97762,

0x71CE16C46C682E01,0x56A365851570D467,0x8B00067B67ED440D,0x633698A115187C69,

0x6E27C065D4BEAA88,0xAECC7CC28FA84C27,0xFB8BC8D8773835F4,0x5984D5F23991C545,

0xEEB8E705B3288DCF,0xBE749F37D1029CA4,0xB26454743BDECB6D,0xA8B4DDCD1C38DC9E,

0x1A8D0C1A7A585C45,0x67352A4F7CC28970,0xA7A7393D440A3051,0x90726E9996AC1952,

0x8655B89173858652,0x74A77127CE824637,0x7CB9CE5B9E49B74D,0x219096A6B73831F3,

0x8317C43FBA4D62EE,0x9EC221623937AB30,0x979C3881DD38F35B,0x535120A9A826E7A3,

0x9BAD2BA58CF4ADAC,0xE174D985FB365B45,0x91EEECD21B8D00F3,0xB5D690304B826C2A,

0x0BF49AA0907196B3,0x7B5CA664EBB7B0E7,0x44926BDB5833DF2E,0x0BE698837DF31CAF,

0xEF8E91EBB5AF9ABC,0xBEA8EE329D5C5CDD,0x6587053FEFE2FCC1,0x6D668039BF4F83A3,

0x9B960ECFDE6EEBB2,0x5FA1F19D1220EAD1,0x3025237AEC029A73,0xF41AEAD69BB6EF67,

0xED76A53DBD55D479,0x370F737602321AC8,0x54477E4DE462C7E4,0x115514C83A2BB129,

0x6FF92DEE13FBF4E8,0xDB9885E8DF84F43C,0x614BFC86D0775395,0xE4A830F2EF1E174C,

0xF8734ADB82F73309,0xF03208A67B38EB64,0xC361F287481DDED2,0xA3C8BE2C3CD068CA,

0xC20493D805F0C880,0x1423CFF2E8FB18E8,0x6F5524FA696FD6AF,0x99D5271557CC26F9,

0xCF4E7CABE8B00D5C,0x621A37A092DB36DD,0x85FFE1FD3B3041DB,0x724397C4CD2BDC62,

0xA77EA237788C99A6,0xB811DFF94760C1F8,0x8606EC3491EB4F57,0x980F1768B64CEBE5,

0xC39B73CF00C3EFC4,0x07EED4869C1916CA,0x8B6296E3E131D475,0xEBEC6E3E800DEEA1,

0xE32A5CB52A142890,0x6A293451746780EF,0x6D3CB3080F7F7B67,0x5B131B7E1E679EA8,

0xA20942111D4D51F4,0x7449CF39BD6F67FE,0x48C1352C79002610,0x56BBDF153CA4A54E,

0x8A93A35BB1853392,0x6A1F3F745E953D64,0x3FC19AEF3D5EC00B,0x27D4E2781FF6708D,

0x6440EE0F4EEA2BBD,0xDB16390590AFC128,0x4AA8B2AAF02B3246,0x6554E5FED6568381,

0x3FE400D6EC8026E5,0x9D2FAD5F12DB4D51,0x7D3E9A3D36F829C8,0x9FFDFE0941C33C9E,

0x00D146D7F43CF281,0xF0F12DAC0F5CF7C5,0xCB6F7297D584839D,0x19A9898BFFD6281F,

0x09B970F0425BC53B,0xF208E9F4A10262BC,0x883E5AE7D3450CB8,0x8CF7133E03060357,

0x97771BC6E9BE410F,0x5BA35BB613D8A257,0x8EA1B54157FE307F,0xE5EFDBC3888EC96E,

0x0105ACA157925E16,0x5A41F3BB8F717B8B,0x769CFAED43991080,0x0C16D93D4E4339DE,

0x838AD3CD74EBEB8E,0x1D03762A1C906714,0x4F94A185DD2A5BAE,0xC456D6502266625D,

0xAB59E252DF780D62,0xA618068001F9B9A2,0x6419689E1930366F,0xFB7AE9C7792A1ACE,

0x1B21A13DD138E62C,0x69D1EC179545767A,0x27C3627F9304DE85,0xE6573C166BCA52A1,

0x0AE95CCE3B8D8787,0xBBAA3617D1B1B2E6,0x8706A69573A73DBD,0xE4C5D18627F58CE9,

0xB96A3C3893177E4C,0xAF9DDE08E96B1992,0xBCC5B9E5D5189EE4,0xD465D3EDBAB54474,

0x3DFD15F6AC928541,0x7368A83E7D2F9D2A,0xE6836D77384B9077,0xC978442A52BDE15A,

0xF5AD667702E69E7F,0x423C12091E60E987,0xA169B0DB9374F0C7,0x6AF2ECC3C14DFE35,

0x21CBB229E8F329C2,
]
