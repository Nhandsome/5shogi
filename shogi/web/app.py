import sys
import math
import subprocess
import os
import locale
import copy

from shogi import *
from shogi import Board, CSA, KIF, BLACK, WHITE ##, move_from_csa
from shogi.cli import usi_info_to_score, usi_info_to_csa_comment, re_usi_info
from flask import Flask, render_template, Markup, request
from wsgiref.simple_server import make_server


TURN_SYMBOLS = ('▲', '△')
CSA_TURN_SYMBOLS = {'+': '▲', '-': '△'}

class Engine:
    def __init__(self, cmd, connect=True, debug=True):
        self.cmd = cmd
        self.debug = debug
        if connect:
            self.connect()
        else:
            self.proc = None
            self.name = None

    def connect(self, listener=None):
        if self.debug: listener = print
        self.proc = subprocess.Popen([self.cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(self.cmd))

        cmd = 'usi'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline()
            if line == '':
                raise EOFError()
            line = line.strip()
            if line[:7] == b'id name':
                self.name = line[8:].decode('ascii')
            elif line == b'usiok':
                break
        if listener:
            listener(self.name)

    def usi(self, listener=None):
        if self.debug: listener = print
        cmd = 'usi'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

        lines = []
        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline()
            if line == '':
                raise EOFError()
            line = line.strip().decode(locale.getpreferredencoding())
            if listener:
                listener(line)
            if line == 'usiok':
                break
            lines.append(line)
        return lines

    def setoption(self, name, value, listener=None):
        if self.debug: listener = print
        cmd = 'setoption name ' + name + ' value ' + str(value)
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode(locale.getpreferredencoding()) + b'\n')
        self.proc.stdin.flush()

    def isready(self, listener=None):
        if self.debug: listener = print
        cmd = 'isready'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline()
            if line == '':
                raise EOFError()
            line = line.strip().decode('shift-jis')
            if listener:
                listener(line)
            if line == 'readyok':
                break

    def usinewgame(self, listener=None):
        if self.debug: listener = print
        cmd = 'usinewgame'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

    def position(self, moves=None, sfen="startpos", listener=None):
        if self.debug: listener = print
        cmd = 'position ' + sfen
        if moves:
            cmd += ' moves ' + ' '.join(moves)
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

    def go(self, ponder=False, btime=None, wtime=None, byoyomi=None, binc=None, winc=None, nodes=None, listener=None):
        if self.debug: listener = print
        cmd = 'go'
        if ponder:
            cmd += ' ponder'
        else:
            if btime is not None:
                cmd += ' btime ' + str(btime)
            if wtime is not None:
                cmd += ' wtime ' + str(wtime)
            if byoyomi is not None:
                cmd += ' byoyomi ' + str(byoyomi)
            else:
                if binc is not None:
                    cmd += ' binc ' + str(binc)
                if winc is not None:
                    cmd += ' winc ' + str(winc)
            if nodes is not None:
                cmd += ' nodes ' + str(nodes)
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

        while True:
            ## TODO HAN
            self.proc.stdout.flush()
            line = self.proc.stdout.readline()
            if line == b'':
                raise EOFError()
            line = line.strip().decode('ascii')
            if listener:
                listener(line)
            if line[:8] == 'bestmove':
                items = line[9:].split(' ')
                if len(items) == 3 and items[1] == 'ponder':
                    return items[0], items[2]
                else:
                    return items[0], None

    def quit(self, listener=None):
        if self.debug: listener = print
        cmd = 'quit'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()
        self.proc.wait()
        self.proc = None

class Human:
    def __init__(self, human_input):
        self.board = Board()
        self.name = 'Human'
        self.human_input = human_input

    def usi(self, listener=None):
        return []

    def isready(self, listener=None):
        pass

    def usinewgame(self, listener=None):
        pass

    def position(self, moves=None, sfen="startpos", listener=None):
        self.board.reset()
        for move in moves:
            self.board.push_usi(move)

    def go(self, ponder=False, btime=None, wtime=None, byoyomi=None, binc=None, winc=None, nodes=None, listener=None):
        import time
        while True:
            human_input = dict(self.human_input)
            if human_input['number'] == self.board.move_number:
                usi_move = human_input['move']
                move = Move.from_usi(usi_move)
                if self.board.is_legal(move):
                    return usi_move, None
            time.sleep(0.1)

    def quit(self, listener=None):
        pass

def usi_info_to_pv(board, info):
    m = re_usi_info.match(info)
    if m is None:
        return None

    # pv
    pv = []
    board2 = copy.deepcopy(board)
    for usi_move in m[3].split(' '):
        move = Move.from_usi(usi_move)
        if not board2.is_legal(move):
            break
        pv.append(CSA.COLOR_SYMBOLS[board2.turn] + KIF.move_to_kif(move, board2))
        board2.push(move)

    return ' '.join(pv)

def match(moves, engine1=None, engine2=None, options1={}, options2={}, names=None, byoyomi=None, time=None, inc=None, draw=256, human_input=None, csa=None):
    from collections import defaultdict
    from time import perf_counter

    class Listener:
        def __init__(self):
            self.info = self.bestmove = ''

        def __call__(self, line):
            self.info = self.bestmove
            self.bestmove = line
    listener = Listener()

    # CSA
    if csa:
        csa_exporter = CSA.CsaWriter(csa, append=False)

    engines = []
    for engine in (engine1, engine2):
        if engine == 'human':
            engines.append(Human(human_input))
        else:
            engines.append(Engine(engine, connect=True))
    for engine, options in zip(engines, (options1, options2)):
        for name, value in options.items():
            engine.setoption(name, value, listener=listener)
        engine.isready(listener=listener)

    for i in range(2):
        if names[i]:
            engine[i].name = names[i]
        else:
            names[i] = engines[i].name

    board = Board()
    usi_moves = []
    repetition_hash = defaultdict(int)

    # 新規ゲーム
    for engine in engines:
        engine.usinewgame()

    if csa:
        csa_exporter.info(board, names, version='V2')

    # 対局
    is_game_over = False
    is_nyugyoku = False
    is_illegal = False
    is_repetition_win = False
    is_repetition_lose = False
    is_fourfold_repetition = False
    is_timeup = False
    remain_time = [time, time]
    while not is_game_over:
        engine_index = (board.move_number - 1) % 2
        engine = engines[engine_index]

        # 持将棋
        if board.move_number > draw:
            is_game_over = True
            break

        # position
        engine.position(usi_moves)

        start_time = perf_counter()

        # go
        listener.info = ''
        listener.bestmove = ''
        bestmove, _ = engine.go(byoyomi=byoyomi, btime=remain_time[BLACK], wtime=remain_time[WHITE], binc=inc, winc=inc, listener=listener)

        elapsed_time = perf_counter() - start_time

        if remain_time[board.turn] is not None:
            if inc_time[board.turn] is not None:
                remain_time[board.turn] += inc_time[board.turn]
            remain_time[board.turn] -= math.ceil(elapsed_time * 1000)

        if bestmove == 'resign':
            # 投了
            is_game_over = True
            break
        # elif bestmove == 'win':
        #     # 入玉勝ち宣言
        #     is_nyugyoku = True
        #     is_game_over = True
        #     break
        else:
            move = Move.from_usi(bestmove)
            move_hash = board.move_hash(move)
            if board.is_legal(move):
                if csa:
                    csa_exporter.move(move, time=int(elapsed_time))    ##TODO, comment=usi_info_to_csa_comment(board, listener.info))
                score = usi_info_to_score(listener.info)
                pv = usi_info_to_pv(board, listener.info)
                moves.append({
                    'number': board.move_number,
                    'kif_move': TURN_SYMBOLS[(board.move_number + 1) % 2] + KIF.move_to_kif(move, board),
                    'time': math.ceil(elapsed_time),
                    'move': move_hash,
                    'eval': (score * (1 if board.turn == BLACK else -1)) if score is not None else 'null',
                    'pv': pv if pv is not None else '',
                })
                board.push(move)
                usi_moves.append(bestmove)
                key = board.zobrist_hash()
                repetition_hash[key] += 1
                # 千日手
                if repetition_hash[key] == 4:
                    # 連続王手
                    # is_draw = board.is_draw()
                    # if is_draw == REPETITION_WIN:
                    #     is_repetition_win = True
                    #     is_game_over = True
                    #     break
                    # elif is_draw == REPETITION_LOSE:
                    #     is_repetition_lose = True
                    #     is_game_over = True
                    #     break
                    is_fourfold_repetition = True
                    is_game_over = True
                    break
            else:
                is_illegal = True
                is_game_over = True
                break

        # 終局判定
        if board.is_game_over():
            is_game_over = True
            break

    # エンジン終了
    for engine in engines:
        engine.quit()

    # 結果出力
    if not board.is_game_over() and board.move_number > draw:
        result = '持将棋'
        csa_endgame = '%JISHOGI'
    elif is_fourfold_repetition:
        result = '千日手'
        csa_endgame = '%SENNICHITE'
    elif is_nyugyoku:
        result = TURN_SYMBOLS[board.turn] + '入玉宣言'
        csa_endgame = '%KACHI'
    elif is_illegal:
        win = board.opponent(board.turn)
        result = '{}の反則負け'.format('先手' if win == WHITE else '後手')
        csa_endgame = '%ILLEGAL_MOVE'
    elif is_repetition_win:
        win = board.turn
        result = '{}の反則勝ち'.format('先手' if win == BLACK else '後手')
        csa_endgame = '%+ILLEGAL_ACTION' if board.turn == WHITE else '%-ILLEGAL_ACTION'
    elif is_repetition_lose:
        win = board.opponent(board.turn)
        result = '{}の反則負け'.format('先手' if win == WHITE else '後手')
        csa_endgame = 'ILLEGAL_MOVE'
    elif is_timeup:
        win = board.opponent(board.turn)
        result = '{}の切れ負け'.format('先手' if win == WHITE else '後手')
        csa_endgame = '%TIME_UP'
    else:
        result = TURN_SYMBOLS[board.turn] + '投了'
        csa_endgame = '%TORYO'

    # CSA
    if csa:
        csa_exporter.endgame(csa_endgame)

    moves.append({
        'number': board.move_number,
        'kif_move': result,
        'time': 0,
        'move': 0,
        'eval': 'null',
        'pv': ''
    })

def run(engine1=None, engine2=None, options1={}, options2={}, names=None, byoyomi=None, time=None, inc=None, draw=256, csa=None, port=8000):
    is_match = 'false'
    auto_update = 'false'

    if engine1 and engine2:
        from multiprocessing import Process, Manager
        manager = Manager()
        moves = manager.list()
        human_input = manager.dict({ 'number': 0, 'move': None })
        if names is None:
            names = manager.list([None, None])
        else:
            names = manager.list(names)
        match_proc = Process(target=match, args=[moves, engine1, engine2, options1, options2, names, byoyomi, time, inc, draw, human_input, csa])
        match_proc.start()
        is_match = 'true'
        auto_update = 'true'
    # elif csa:
    #     moves = []
    #     kif = CSA.Parser.parse_file(csa)[0]
    #     names = kif.names
    #     for i, (move, prev_move, time, comment) in enumerate(zip(kif.moves, [None] + kif.moves[:-1], kif.times, kif.comments)):
    #         comment_items = comment.split(' ')
    #         eval = 'null'
    #         pv = ''
    #         if len(comment_items) > 0 and comment_items[0] != '':
    #             eval = int(comment_items[0])
    #         if len(comment_items) > 1:
    #             for csa in comment_items[1:]:
    #                 pv += CSA_TURN_SYMBOLS[csa[0]] + KIF.move_to_kif(move_from_csa(csa[1:]))
    #         moves.append({
    #             'number': i + 1,
    #             'kif_move': TURN_SYMBOLS[i % 2] + KIF.move_to_kif(move, prev_move),
    #             'time': time,
    #             'move': move,
    #             'eval': eval,
    #             'pv': pv,
    #             })
    #     moves.append({
    #         'number': i + 2,
    #         'kif_move': TURN_SYMBOLS[(i + 1) % 2] + CSA.JAPANESE_END_GAMES[kif.endgame],
    #         'time': 0,
    #         'move': 0,
    #         'eval': 'null',
    #         'pv': '',
    #     })

    app = Flask(__name__)

    @app.route("/")
    def init_board():
        autoupdate = 'false'
        human = ''
        if is_match == 'true':
            if match_proc.is_alive():
                autoupdate = request.args.get('autoupdate', default=auto_update)
                if names[len(moves) % 2] == 'Human':
                    human = 'black' if len(moves) % 2 == 0 else 'white'
        return render_template('board.html', names=names, moves=moves, is_match=is_match, autoupdate=autoupdate, human=human)

    @app.route("/update")
    def update():
        human = ''
        if names[len(moves) % 2] == 'Human':
            human = 'black' if len(moves) % 2 == 0 else 'white'
        return { 'names': list(names), 'moves': list(moves), 'human':human }

    @app.route("/move")
    def human_move():
        import time
        human_input['move'] = request.args.get('move')
        human_input['number'] = int(request.args.get('number', default=0))
        time.sleep(0.2)
        human = ''
        if names[len(moves) % 2] == 'Human':
            human = 'black' if len(moves) % 2 == 0 else 'white'
        return { 'names': list(names), 'moves': list(moves), 'human':human }

    server = make_server('localhost', port, app)
    server.serve_forever()

def colab(engine1=None, engine2=None, options1={}, options2={}, names=None, byoyomi=None, time=None, inc=None, draw=256, csa=None):
    from multiprocessing import Process
    import portpicker
    from google.colab import output

    global proc
    if 'proc' in globals():
        proc.terminate()
        proc.join()

    port = portpicker.pick_unused_port()
    proc = Process(target=run, args=(engine1, engine2, options1, options2, names, byoyomi, time, inc, draw, csa, port))
    proc.start()
    output.serve_kernel_port_as_iframe(port, height='680')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine1')
    parser.add_argument('--engine2')
    parser.add_argument('--options1', default='')
    parser.add_argument('--options2', default='')
    parser.add_argument('--name1')
    parser.add_argument('--name2')
    parser.add_argument('--byoyomi', type=int)
    parser.add_argument('--time', type=int)
    parser.add_argument('--inc', type=int)
    parser.add_argument('--draw', type=int, default=256)
    parser.add_argument('--csa')
    parser.add_argument('--port', type=int, default=8001)
    args = parser.parse_args()

    options_list = [{}, {}]

    args.engine1 = '/Users/han/python-shogi/parallel_mcts_player_1.sh'
    options_b1 = {'modelfile':'/Users/han/python-shogi/checkpoint/5_shogi_last_4_80_7_45332','temperature':100,'playout':100}
    # args.engine2 = '/Users/han/python-shogi/parallel_mcts_player_2.sh'
    # options_b1 = {'modelfile':'/Users/han/python-shogi/checkpoint/5_shogi_last_4_80_19_123044','temperature':100,'playout':100}

    # args.engine1 = 'human'
    # # options_b1 = {'modelfile':'/Users/han/python-shogi/checkpoint/best/best_pv_2','temperature':100,'playout':100}
    args.engine2 = 'human'
    # options_b1 = {'modelfile':'/Users/han/python-shogi/checkpoint/best/best_pv_2','temperature':100,'playout':100}    

    # for i, kvs in enumerate([options.split(',') for options in (args.options1, args.options2)]):
    #     if len(kvs) == 1 and kvs[0] == '':
    #         continue
    #     for kv_str in kvs:
    #         kv = kv_str.split(':', 1)
    #         if len(kv) != 2:
    #             raise ValueError('options{}'.format(i + 1))
    #         options_list[i][kv[0]] = kv[1]

    run(engine1=args.engine1, engine2=args.engine2,
        options1=options_list[0], options2=options_list[1],
        names=[args.name1, args.name2],
        byoyomi=args.byoyomi, time=args.time, inc=args.inc, draw=args.draw,
        csa=args.csa, port=args.port)
