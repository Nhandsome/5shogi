import argparse
from collections import defaultdict
import re

from shogi import *
# from shogi.CSA import *
from shogi.PGN import *
from shogi.Move import *

CSA_PIECE_SYMBOLS = ['* ', 'FU', 'GI', 'KI', 'KA', 'HI', 'OU',
                       'TO', 'NG',       'UM', 'RY']

def pgn_to_csa(board, move):
    is_droped = False
    is_promoted = False
    is_checkmate = False

    if move[1] == '@':
        is_droped = True
        usi_from = move[0] + '*'
    if move[-1] == '#':
        is_checkmate = True
        move = move[:-1]
    if move[-1] == '+':
        is_promoted = True
        move = move[:-1]
    if move[-1] == '=':
        is_promoted = False
        move = move[:-1]
    
    if len(move) > 2:
        if move[0] == '+':
            p = move[:2]
        else:
            p = move[0]
        move_to = move[-2:]
    else:
        p = 'p'
        move_to = move
    
    if p.islower() :
        p = 'P'

    usi_to = SQUARE_NAMES[PGN_SQUARE_NAMES.index(move_to)]
    if not is_droped:
        usi_froms = []
        for t in board.legal_moves:
            if usi_to in t.usi()[-3:]:
                usi_froms.append(t.usi()[:2]) 
        temp=[]
        for usi in usi_froms:
            if usi[1] == '*':
                break
            csa_from = CSA_SQUARE_NAMES[SQUARE_NAMES.index(usi)]
            csa_piece = board.pieces[CSA_SQUARE_NAMES.index(csa_from)]

            if csa_piece == PIECE_SYMBOLS.index(p.lower()):
                # return_from = csa_from
                # return_piece = CSA_PIECE_SYMBOLS[csa_piece]
                temp.append(usi)
        temp = list(set(temp)) 

        if len(temp) == 1:
            usi_from = temp[0]
        else:
            temp_col = ['e','d','c','b','a']
            temp_row = ['1', '2', '3', '4', '5']
            if len(move) > 4 and move[0] == '+' and move[2] in temp_col:
                col = temp_col.index(move[2]) + 1
                for usi in temp:
                    if usi[0] == str(col):
                        usi_from = usi
                        break

            if len(move) > 3 and move[1] in temp_col:
                col = temp_col.index(move[1]) + 1
                for usi in temp:
                    if usi[0] == str(col):
                        usi_from = usi
                        break
            
            if len(move) > 4 and move[0] == '+' and move[2] in temp_row:
                row = temp_col[int(move[2]) - 1]
                for usi in temp:
                    if usi[1] == str(row):
                        usi_from = usi
                        break

            if len(move) > 3 and move[1] in temp_row:
                row = temp_col[int(move[1]) - 1]
                for usi in temp:
                    if usi[1] == str(row):
                        usi_from = usi
                        break
            
    if is_promoted :
        usi_to += '+'
    
    usi_move = usi_from+usi_to

    board.push_usi(usi_move)

    if not is_droped:
        return_from = CSA_SQUARE_NAMES[SQUARE_NAMES.index(usi_from)]
    else:
        return_from = '00'
    return_to = CSA_SQUARE_NAMES[SQUARE_NAMES.index(usi_to[:2])]
    return_piece = CSA_PIECE_SYMBOLS[board.pieces[SQUARE_NAMES.index(usi_to[:2])]]

    return return_from+return_to+return_piece
   




parser = argparse.ArgumentParser()
parser.add_argument('--pgn', type=str, nargs='+')
parser.add_argument('--outprefix')
parser.add_argument('--uniq', action='store_true')
args = parser.parse_args()

args.pgn = ['./data/pgn/games_7.pgn']
args.outprefix = './data/pgn_3/'

pgns = defaultdict(list)
stats = defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0, 0, 0]))

pgntexts = []
results = []
regex = "\{.*\}|\s-\s.*"
filter = '\n{--------------\nr b s g k\n. . . . p\n. . . . .\nP . . . .\nK G S B R\nwhite to play\n--------------}\n'

import os
args.pgn = os.listdir('./data/pgn')

for file in args.pgn:
    file = './data/pgn/'+file
    header = False
    players = []
    pgntext = ""
    for line in open(file):
        if line[:1] == "[":
            if pgntext != '':
                pgntexts.append(pgntext)
                results.append(result)
            if not header and pgntext != "":
                players = []
                pgntext = ""

            header = True

            if line[1:6] in ['White', 'Black']:
                players.append(line[8:-3])
            elif line[1:7] == 'Result':
                result = line[9:-3]
                
        else:
            header = False
            pgntext += line

last_pgntexts = []
for pgntext, result in zip(pgntexts, results):
    if result != "1/2-1/2":
        filtered = re.sub("\{.*?\}","", pgntext).replace(filter,'').replace('\n',' ')
        ' '.join(filtered.split())
        last_pgntexts.append(filtered)

intro = 'V2\nN+5_shogi_auto1_17_60197\nN-5_shogi_auto1_17_60197\nPI\n+\n'
turns = ['+','-']
csas = []



for key, pgntext in enumerate(last_pgntexts):
    csa = ''
    csa += intro
    splited = pgntext.split()
    board = Board()
    # splited[-1]
    for i, move in enumerate(splited[:-1]):
        t = i%3
        if t != 0:
            turn = turns[t-1]
            csa += turn
            csa += pgn_to_csa(board, move)

            csa += '\n'
    csa += '%TORYO'
    csas.append(csa)
    with open(args.outprefix + str(key) + '.csa', 'w') as f:
        f.writelines(csa)






