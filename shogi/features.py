import numpy as np
import shogi
import copy

from shogi.common import *

def make_input_features(piece_bb, occupied, pieces_in_hand):
    features = []
    for color in shogi.COLORS:
        # the place of pieces on the board: Normal(6) + Promoted(4) = 10
        for piece_type in shogi.PIECE_TYPES_WITH_NONE[1:]:
            bb = piece_bb[piece_type] & occupied[color]
            feature = np.zeros(5*5)
            for pos in shogi.SQUARES:
                if bb & shogi.BB_SQUARES[pos] > 0:
                    feature[pos] = 1
            features.append(feature.reshape((5, 5)))

        # pieces in hand
        # 5 pieces : P, S, G, B, R : 5
        for piece_type in range(1, 6):
            for n in range(shogi.MAX_PIECES_IN_HAND[piece_type]):
                if piece_type in pieces_in_hand[color] and n < pieces_in_hand[color][piece_type]:
                    feature = np.ones(5*5)
                else:
                    feature = np.zeros(5*5)
                features.append(feature.reshape((5, 5)))
    return features

def make_input_features_from_board(board):
    if board.turn == shogi.BLACK:
        piece_bb = board.piece_bb                                                               # 10
        occupied = (board.occupied[shogi.BLACK], board.occupied[shogi.WHITE])                   # 1
        pieces_in_hand = (board.pieces_in_hand[shogi.BLACK], board.pieces_in_hand[shogi.WHITE]) # 5
    else:
        piece_bb = [bb_rotate_180(bb) for bb in board.piece_bb]
        occupied = (bb_rotate_180(board.occupied[shogi.WHITE]), bb_rotate_180(board.occupied[shogi.BLACK]))
        pieces_in_hand = (board.pieces_in_hand[shogi.WHITE], board.pieces_in_hand[shogi.BLACK])

    return make_input_features(piece_bb, occupied, pieces_in_hand)

def make_output_label(move, color):
    move_to = move.to_square
    move_from = move.from_square

    # 白の場合盤を回転
    if color == shogi.WHITE:
        move_to = SQUARES_R180[move_to]
        if move_from is not None:
            move_from = SQUARES_R180[move_from]

    # move direction
    if move_from is not None:
        to_y, to_x = divmod(move_to, 5)
        from_y, from_x = divmod(move_from, 5)
        dir_x = to_x - from_x
        dir_y = to_y - from_y
        if dir_y < 0 and dir_x == 0:
            move_direction = UP
        elif dir_y < 0 and dir_x < 0:
            move_direction = UP_LEFT
        elif dir_y < 0 and dir_x > 0:
            move_direction = UP_RIGHT
        elif dir_y == 0 and dir_x < 0:
            move_direction = LEFT
        elif dir_y == 0 and dir_x > 0:
            move_direction = RIGHT
        elif dir_y > 0 and dir_x == 0:
            move_direction = DOWN
        elif dir_y > 0 and dir_x < 0:
            move_direction = DOWN_LEFT
        elif dir_y > 0 and dir_x > 0:
            move_direction = DOWN_RIGHT

        # promote
        if move.promotion:
            move_direction = MOVE_DIRECTION_PROMOTED[move_direction]
    else:
        # 持ち駒
        move_direction = len(MOVE_DIRECTION) + move.drop_piece_type - 1

    move_label = 5 * 5 * move_direction + move_to

    return move_label

def make_features(position):
    piece_bb, occupied, pieces_in_hand, move, win = position
    features = make_input_features(piece_bb, occupied, pieces_in_hand)

    return (features, move, win)

def make_input_features_2(piece_bb, occupied, pieces_in_hand):
    features1 = []
    features2 = []
    for color in shogi.COLORS:
        # the place of pieces on the board: Normal(6) + Promoted(4) = 10
        for piece_type in shogi.PIECE_TYPES_WITH_NONE[1:]:
            bb = piece_bb[piece_type] & occupied[color]
            feature = np.zeros(5*5)
            for pos in shogi.SQUARES:
                if bb & shogi.BB_SQUARES[pos] > 0:
                    feature[pos] = 1
            features1.append(feature.reshape((5, 5)))

        # pieces in hand
        # 5 pieces : P, S, G, B, R : 5
        for piece_type in range(1, 6):
            for n in range(shogi.MAX_PIECES_IN_HAND[piece_type]):
                if piece_type in pieces_in_hand[color] and n < pieces_in_hand[color][piece_type]:
                    feature = np.ones(5*5)
                else:
                    feature = np.zeros(5*5)
                features2.append(feature.reshape((5, 5)))

    return features1, features2

def make_features_2(position):
    piece_bb, occupied, pieces_in_hand, move, win = position
    features1, features2 = make_input_features_2(piece_bb, occupied, pieces_in_hand)

    return (features1, features2, move, win)

def make_input_features_from_board_2(board):
    if board.turn == shogi.BLACK:
        piece_bb = board.piece_bb                                                               # 10
        occupied = (board.occupied[shogi.BLACK], board.occupied[shogi.WHITE])                   # 1
        pieces_in_hand = (board.pieces_in_hand[shogi.BLACK], board.pieces_in_hand[shogi.WHITE]) # 5
    else:
        piece_bb = [bb_rotate_180(bb) for bb in board.piece_bb]
        occupied = (bb_rotate_180(board.occupied[shogi.WHITE]), bb_rotate_180(board.occupied[shogi.BLACK]))
        pieces_in_hand = (board.pieces_in_hand[shogi.WHITE], board.pieces_in_hand[shogi.BLACK])

    return make_input_features_2(piece_bb, occupied, pieces_in_hand)


# if __name__ == '__main__':
#     board = shogi.Board()
#     board.push_usi('3e3a')
#     board.push_usi('1a2b')
    
#     temp = (make_input_features_2(board.piece_bb,board.occupied,board.pieces_in_hand))
#     print(len(temp))
#     print(temp[0])

#     print(make_input_features_from_board(board))

#     for move in board.legal_moves:
#         print(move)
#         # ラベルに変換
#         label = make_output_label(move, 0)
#         print(label)

