import numpy as p
import torch
import torch.nn as nn
import torch.nn.functional as F

import shogi

from shogi.common import *
from shogi.features import *
from shogi.network.policy import *
from shogi.player.base_player import *

device = 'cuda' if torch.cuda.is_available else 'cpu'


def greedy(logits):
  return logits.index(max(logits))

def boltzmann(logits, temperature):
  logits /= temperature
  logits -= logits.max()
  probabilities = np.exp(logits)
  probabilities /= probabilities.sum()
  return np.random.choice(len(logits), p=probabilities)

class PolicyValuePlayer(BasePlayer):
  def __init__(self):
    super().__init__()
    self.modelfile = '/Users/han/python-shogi/checkpoint/5_shogi_210913_1_100_10300'
    self.model = None

  def usi(self):
    print('id name policy_player')
    print('option name modelfile type string default ' + self.modelfile)
    print('usiok')

  def setoption(self, option):
    if option[1] == 'modelfile':
        self.modelfile = option[3]

  def isready(self):
    if self.model is None:
      self.model = PolicyNetwork()
      self.model.to(device)
    else:
      checkpoint = torch.load(self.modelfile, map_location=device, strict=False)
      self.model.load_state_dict(checkpoint['model'])
    print('readyok')

  def go(self):
    if self.board.is_game_over():
      print('bestmove resign')
      return
    
    ## Boardの状況を読み込み、学習に必要な特徴に変換
    features = make_input_features_from_board(self.board)
    x = torch.from_numpy(np.array([features], dtype=np.float32)).to(device)

    with torch.no_grad():
      y = self.model(x)

      logits = y.data[0].to('cpu')
      probabilities = F.softmax(y,dim=1).data[0]

    legal_moves = []
    legal_logits = []
    ## ライブラリーから今の状況からの合法手を呼び出して
    for move in self.board.legal_moves:
      # ラベルに変換
      # make_output_label : MOVE_DIRECTION * 5 * 5 + MOVE_TO
      label = make_output_label(move, self.board.turn)
      # 合法手とその指し手の確率(logits)を格納
      legal_moves.append(move)
      legal_logits.append(logits[label])
      # 確率を表示
      print('info string {:5} : {:.5f}'.format(move.usi(), probabilities[label]))
        
    # 確率が最大の手を選ぶ(グリーディー戦略)
    # selected_index = greedy(legal_logits)
    # 確率に応じて手を選ぶ(ソフトマックス戦略)
    selected_index = boltzmann(np.array(legal_logits, dtype=np.float32), 0.5)
    bestmove = legal_moves[selected_index]

    print('bestmove', bestmove.usi())

if __name__ == '__main__':
    test_player = PolicyValuePlayer()
    test_player.isready()
    test_player.go()