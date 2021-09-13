import shogi

# 移動の定数 
MOVE_DIRECTION = [
    UP, UP_LEFT, UP_RIGHT, LEFT, RIGHT, DOWN, DOWN_LEFT, DOWN_RIGHT, #UP2_LEFT, UP2_RIGHT,
    UP_PROMOTE, UP_LEFT_PROMOTE, UP_RIGHT_PROMOTE, LEFT_PROMOTE, RIGHT_PROMOTE, DOWN_PROMOTE, DOWN_LEFT_PROMOTE, DOWN_RIGHT_PROMOTE, #UP2_LEFT_PROMOTE, UP2_RIGHT_PROMOTE
] = range(16)

# 成り変換テーブル
MOVE_DIRECTION_PROMOTED = [
    UP_PROMOTE, UP_LEFT_PROMOTE, UP_RIGHT_PROMOTE, LEFT_PROMOTE, RIGHT_PROMOTE, DOWN_PROMOTE, DOWN_LEFT_PROMOTE, DOWN_RIGHT_PROMOTE, #UP2_LEFT_PROMOTE, UP2_RIGHT_PROMOTE
]

# 指し手を表すラベルの数
MOVE_DIRECTION_LABEL_NUM = len(MOVE_DIRECTION) + 5 # 5 : P S G B R

# rotate 180degree
SQUARES_R180 = [
    shogi.E1, shogi.E2, shogi.E3, shogi.E4, shogi.E5, 
    shogi.D1, shogi.D2, shogi.D3, shogi.D4, shogi.D5, 
    shogi.C1, shogi.C2, shogi.C3, shogi.C4, shogi.C5, 
    shogi.B1, shogi.B2, shogi.B3, shogi.B4, shogi.B5, 
    shogi.A1, shogi.A2, shogi.A3, shogi.A4, shogi.A5, 
]
def bb_rotate_180(bb):
    bb_r180 = 0
    for pos in shogi.SQUARES:
        if bb & shogi.BB_SQUARES[pos] > 0:
            bb_r180 += 1 << SQUARES_R180[pos]
    return bb_r180