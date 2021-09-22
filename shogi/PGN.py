import shogi
from datetime import datetime

## SQUARE_NAMES
PGN_SQUARE_NAMES = [
	# 'e5', 'e4', 'e3', 'e2', 'e1',
	# 'd5', 'd4', 'd3', 'd2', 'd1',
	# 'c5', 'c4', 'c3', 'c2', 'c1',
	# 'b5', 'b4', 'b3', 'b2', 'b1',
	# 'a5', 'a4', 'a3', 'a2', 'a1',
    'a5', 'b5', 'c5', 'd5', 'e5',
    'a4', 'b4', 'c4', 'd4', 'e4',
    'a3', 'b3', 'c3', 'd3', 'e3',
    'a2', 'b2', 'c2', 'd2', 'e2',
    'a1', 'b1', 'c1', 'd1', 'e1',
]
## 
PGN_HAND_PIECES = [
    'p', 's', 'g', 'b', 'r',
]
## PIECE_SYMBOLS
PGN_PIECE_TYPES = [
    None,
    'P', 'S', 'B', 'R', 'G', 'K',
    '+P', '+S', '+B', '+R',
]

def move_to_san(move):
    move_to = PGN_SQUARE_NAMES[shogi.move_to(move)]

    if shogi.move_is_drop(move):
        return PGN_HAND_PIECES[shogi.move_drop_hand_piece(move)] + '@' + move_to

    move_from = PGN_SQUARE_NAMES[shogi.move_from(move)]
    promotion = '+' if shogi.move_is_promotion(move) else ''
    return PGN_PIECE_TYPES[shogi.move_from_piece_type(move)] + move_from + move_to + promotion

class Exporter:
    def __init__(self, path=None, append=False):
        if path:
            self.open(path, append)
        else:
            self.f = None

    def open(self, path, append=False):
        self.f = open(path, 'a' if append else 'w', newline='\n')

    def close(self):
        self.f.close()

    def tag_pair(self, names, result, event='?', site='?', starttime=datetime.now(), round=1):
        self.f.write('[Event "' + event +'"]\n')
        self.f.write('[Site "' + site + '"]\n')
        self.f.write('[Date "' + (starttime.strftime('%Y.%m.%d') if starttime else '????.??.??') + '"]\n')
        self.f.write('[Round "' + str(round) + '"]\n')
        self.f.write('[White "' + names[0] + '"]\n')
        self.f.write('[Black "' + names[1] + '"]\n')
        if result == shogi.BLACK_WIN:
            self.result_str = '1-0'
        elif result == shogi.WHITE_WIN:
            self.result_str = '0-1'
        elif result == shogi.DRAW:
            self.result_str = '1/2-1/2'
        else:
            self.result_str = '*'
        self.f.write('[Result "' + self.result_str + '"]\n\n')
        self.f.flush()

    def movetext(self, moves):
        line = ''
        for i, move in enumerate(moves):
            if i % 2 == 0:
                part = str(i // 2 + 1) + '. '
            else:
                part = ''
            part += move_to_san(moves[i])
            if i + 1 == len(moves):
                part += ' ' + self.result_str
            if len(line) + len(part) <= 80:
                if line != '':
                    line += ' '
                line += part
            else:
                self.f.write(line + '\n')
                line = part

        self.f.write(line + '\n\n')
        self.f.flush()

if __name__ == '__main__':
    test = Exporter()
    test.movetext('5d5e')