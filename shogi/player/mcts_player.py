import numpy as p
import torch
import torch.nn as nn
import torch.nn.functional as F

import shogi

from shogi.common import *
from shogi.features import *
from shogi.network.policyvalue_res import *
from shogi.player.base_player import *
from shogi.uct.uct_node import *

import math
import time
import copy

# UCBのボーナス項の定数
# 今まで選ばれなかったノードに関してのボーナス
C_PUCT = 1.0
# 1手当たりのプレイアウト数
# ランダムにゲームを進み、結果でノードを評価
CONST_PLAYOUT = 300
# 投了する勝率の閾値
RESIGN_THRESHOLD = 0
# 温度パラメータ
# Normalizationの一種？
TEMPERATURE = 1.0

device = 'cuda' if torch.cuda.is_available else 'cpu'

def softmax_temperature_with_normalize(logits, temperature):
    # 温度パラメータを適用
    logits /= temperature

    # 確率を計算(オーバーフローを防止するため最大値で引く)
    max_logit = max(logits)
    probabilities = np.exp(logits - max_logit)

    # 合計が1になるように正規化
    sum_probabilities = sum(probabilities)
    probabilities /= sum_probabilities

    return probabilities

# 子ノードがない時、Playout(ランダムにゲームを進む)を行う
class PlayoutInfo:
    def __init__(self):
        self.halt = 0 # 探索を打ち切る回数
        self.count = 0 # 現在の探索回数

class MctsPlayer(BasePlayer):
    def __init__(self):
        super().__init__()
        # モデルファイルのパス
        # 学習済みのモデルを呼び出す
        self.modelfile = r'/content/drive/MyDrive/fusic/shogi/checkpoint/210909_10_43700'
        self.model = None # モデル

        # ノードの情報
        # ノードには、子ノードの情報を含め、Policy/Value Network、MCTSをベースとした勝率情報がある
        self.node_hash = NodeHash()
        self.uct_node = [UctNode() for _ in range(UCT_HASH_SIZE)]

        # プレイアウト回数管理
        self.po_info = PlayoutInfo()
        self.playout = CONST_PLAYOUT

        # 温度パラメータ
        self.temperature = TEMPERATURE

    # UCB値が最大の手を求める
    # child_win / child_move_count：現ノードの評価、勝率
    # current_node.nnrate：Policy Networkで予測した子ノードの選び確率
    # u：選ばれて子ノードに対してボーナスを与える
    # C_PUCT：ボーナスの重みパラメーター
    def select_max_ucb_child(self, board, current_node):
        child_num = current_node.child_num
        child_win = current_node.child_win
        child_move_count = current_node.child_move_count

        q = np.divide(child_win, child_move_count, out=np.repeat(np.float32(0.5), child_num), where=child_move_count != 0)
        u = np.sqrt(np.float32(current_node.move_count)) / (1 + child_move_count)
        tmp_current_node = current_node.nnrate.to('cpu').detach().numpy().copy()
        ucb = q + C_PUCT * tmp_current_node * u

        return np.argmax(ucb)


    # ノードの展開
    # hashに保存されているnodeを探す。無い時は、
    # 空いているhashを探し
    # ノードを初期化（子ノード作り、現状況の評価）
    def expand_node(self, board):
        # 今の状況と同じhashがあるかを確認
        # 対応するhashが無い時は、UCT_HASH_SIZEを返す
        index = self.node_hash.find_same_hash_index(board.zobrist_hash(), board.turn, board.move_number)

        # 合流先が検知できれば, それを返す
        # 対応するhashを探したら、以前のhash indexを返す
        if not index == UCT_HASH_SIZE:
            return index
    
        # 空のインデックスを探す
        index = self.node_hash.search_empty_index(board.zobrist_hash(), board.turn, board.move_number)

        # 現在のノードの初期化
        current_node = self.uct_node[index]
        current_node.move_count = 0
        current_node.win = 0.0
        current_node.child_num = 0
        current_node.evaled = False
        current_node.value_win = 0.0

        # 候補手の展開
        # 現状況で展開できるmoveを全て探す（子ノード）
        current_node.child_move = [move for move in board.legal_moves]
        # 子ノードを数
        child_num = len(current_node.child_move)
        # 子ノードはまだ初期化されてない
        # zeroベース
        current_node.child_index = [NOT_EXPANDED for _ in range(child_num)]
        current_node.child_move_count = np.zeros(child_num, dtype=np.int32)
        current_node.child_win = np.zeros(child_num, dtype=np.float32)

        # 子ノードの個数を設定
        current_node.child_num = child_num

        # ノードを評価
        # 可能な着手がないと価値は0
        # eval_node：Policy / Value Networkを返す
        # nnrate：Policy Networkからの子ノードに対する予測確率
        # value_win：Value Networkからの勝率
        # evaled：True
        if child_num > 0:
            self.eval_node(board, index)
        else:
            current_node.value_win = 0.0
            current_node.evaled = True

        return index

    # 探索を打ち切るか確認
    # 検索できる数より、最も多く選ばれたfirst - secondの差が大きい時、打ち切る。
    def interruption_check(self):
        child_num = self.uct_node[self.current_root].child_num
        child_move_count = self.uct_node[self.current_root].child_move_count
        rest = self.po_info.halt - self.po_info.count

        # 探索回数が最も多い手と次に多い手を求める
        second, first = child_move_count[np.argpartition(child_move_count, -2)[-2:]]

        # 残りの探索を全て次善手に費やしても最善手を超えられない場合は探索を打ち切る
        if first - second > rest:
            return True
        else:
            return False

    # UCT探索
    # 子ノードが無い時、1を返す（負けなので相手の勝利）
    # 子ノードがある時、最もらしい手を打つ
    # 深く検索しながら、最後負けになる時点から逆順に評価をつける
    def uct_search(self, board, current):
        current_node = self.uct_node[current]

        # 詰みのチェック
        if current_node.child_num == 0:
            return 1.0 # 反転して値を返すため1を返す

        child_move = current_node.child_move
        child_move_count = current_node.child_move_count
        child_index = current_node.child_index

        # UCB値が最大の手を求める
        next_index = self.select_max_ucb_child(board, current_node)
        # 選んだ手を着手
        board.push(child_move[next_index])

        # ノードの展開の確認
        # 次の手が展開されてない場合、今の状況を評価する
        if child_index[next_index] == NOT_EXPANDED:
            # ノードの展開(ノード展開処理の中でノードを評価する)
            # 空いているhashを探して、初期化し、ノードの評価を行う
            index = self.expand_node(board)
            child_index[next_index] = index
            child_node = self.uct_node[index]

            # valueを勝敗として返す
            result = 1 - child_node.value_win
        # 子ノードが展開されている場合、繰り返し
        else:
            # 手番を入れ替えて1手深く読む
            result = self.uct_search(board, child_index[next_index])

        # 探索結果の反映
        current_node.win += result
        current_node.move_count += 1
        current_node.child_win[next_index] += result
        current_node.child_move_count[next_index] += 1

        # 手を戻す
        board.pop()

        return 1 - result

    # ノードを評価
    # 現状況を学習したモデルで評価、情報更新
    def eval_node(self, board, index):
        # 現状況でのFeatureを生成
        eval_features = [make_input_features_from_board(board)]
        
        # 学習モデルを用いた予測
        x = torch.from_numpy(np.array(eval_features, dtype=np.float32)).to(device)
        with torch.no_grad():
            y1, y2 = self.model(x)
    
            logits = y1.data[0].to('cpu')
            value = F.softmax(y2,dim=1).data[0].to('cpu')

        current_node = self.uct_node[index]
        child_num = current_node.child_num
        child_move = current_node.child_move
        color = self.node_hash[index].color

        # 合法手でフィルター
        # っていうことよりは、可能な次の手を表すlabelを生成
        legal_move_labels = []
        for i in range(child_num):
            legal_move_labels.append(make_output_label(child_move[i], color))

        # Boltzmann分布
        # 生成したlabelにモデルのPolicy Networkの予測値を適応
        probabilities = softmax_temperature_with_normalize(logits[legal_move_labels], self.temperature)

        # ノードの値を更新
        current_node.nnrate = probabilities
        current_node.value_win = float(value)
        current_node.evaled = True

    def usi(self):
        print('id name mcts_player')
        print('option name modelfile type string default ' + self.modelfile)
        print('option name playout type spin default ' + str(self.playout) + ' min 100 max 10000')
        print('option name temperature type spin default ' + str(int(self.temperature * 100)) + ' min 10 max 1000')
        print('usiok')

    def setoption(self, option):
        if option[1] == 'modelfile':
            self.modelfile = option[3]
        elif option[1] == 'playout':
            self.playout = int(option[3])
        elif option[1] == 'temperature':
            self.temperature = int(option[3]) / 100

    def isready(self):
        # モデルをロード
        if self.model is None:
            self.model = PolicyValueNetwork()
            self.model.to(device)
        checkpoint = torch.load(self.modelfile, map_location=device)
        self.model.load_state_dict(checkpoint['model'])
        
        # ハッシュを初期化
        self.node_hash.initialize()
        print('readyok')

    def go(self):
        if self.board.is_game_over():
            print('bestmove resign')
            return

        # 探索情報をクリア
        self.po_info.count = 0

        # 古いハッシュを削除
        self.node_hash.delete_old_hash(self.board, self.uct_node)

        # 探索開始時刻の記録
        begin_time = time.time()

        # 探索回数の閾値を設定
        self.po_info.halt = self.playout

        # ルートノードの展開
        self.current_root = self.expand_node(self.board)

        # 候補手が1つの場合は、その手を返す
        current_node = self.uct_node[self.current_root]
        child_num = current_node.child_num
        child_move = current_node.child_move
        if child_num == 1:
            print('bestmove', child_move[0].usi())
            return

        # プレイアウトを繰り返す
        # 探索回数が閾値を超える, または探索が打ち切られたらループを抜ける
        while self.po_info.count < self.po_info.halt:
            # 探索回数を1回増やす
            self.po_info.count += 1
            # 1回プレイアウトする
            self.uct_search(self.board, self.current_root)
            # 探索を打ち切るか確認
            if self.interruption_check() or not self.node_hash.enough_size:
                break

        # 探索にかかった時間を求める
        finish_time = time.time() - begin_time

        child_move_count = current_node.child_move_count
        if self.board.move_number < 10:
            # 訪問回数に応じた確率で手を選択する
            selected_index = np.random.choice(np.arange(child_num), p=child_move_count/sum(child_move_count))
        else:
            # 訪問回数最大の手を選択する
            selected_index = np.argmax(child_move_count)

        child_win = current_node.child_win

        # for debug
        for i in range(child_num):
            print('{:3}:{:5} move_count:{:4} nn_rate:{:.5f} win_rate:{:.5f}'.format(
                i, child_move[i].usi(), child_move_count[i],
                current_node.nnrate[i],
                child_win[i] / child_move_count[i] if child_move_count[i] > 0 else 0))

        # 選択した着手の勝率の算出
        best_wp = child_win[selected_index] / child_move_count[selected_index]

        # 閾値未満の場合投了
        if best_wp < RESIGN_THRESHOLD:
            print('bestmove resign')
            return

        bestmove = child_move[selected_index]

        # 勝率を評価値に変換
        if best_wp == 1.0:
            cp = 30000
        else:
            cp = int(-math.log(1.0 / best_wp - 1.0) * 600)

        print('info nps {} time {} nodes {} hashfull {} score cp {} pv {}'.format(
            int(current_node.move_count / finish_time),
            int(finish_time * 1000),
            current_node.move_count,
            int(self.node_hash.get_usage_rate() * 1000),
            cp, bestmove.usi()))

        print('bestmove', bestmove.usi())