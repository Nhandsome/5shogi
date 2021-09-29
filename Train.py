import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from shogi.common import *
from shogi.features import *
from shogi.read_kifu import *
from shogi.network.policyvalue_res import PolicyValueResNetwork
from torch.utils.tensorboard import SummaryWriter
import config

import os
import random
import numpy as np
import loggers as lg


device = 'cuda' if torch.cuda.is_available else 'cpu'

def mini_batch(positions, i, batchsize):
    mini_batch_data = []
    mini_batch_move = []
    mini_batch_win = []
    for b in range(batchsize):
        features, move, win = make_features(positions[i + b])
        mini_batch_data.append(features)
        mini_batch_move.append(move)
        mini_batch_win.append(win)

    return (torch.from_numpy(np.array(mini_batch_data, dtype=np.float32)).to(device),
            torch.from_numpy(np.array(mini_batch_move, dtype=np.long)).to(device),
            torch.from_numpy(np.array(mini_batch_win, dtype=np.float32).reshape((-1, 1))).to(device))

def mini_batch_for_test(positions, batchsize):
    mini_batch_data = []
    mini_batch_move = []
    mini_batch_win = []
    for b in range(batchsize):
        features, move, win = make_features(random.choice(positions))
        mini_batch_data.append(features)
        mini_batch_move.append(move)
        mini_batch_win.append(win)

    return (torch.from_numpy(np.array(mini_batch_data, dtype=np.float32)).to(device),
            torch.from_numpy(np.array(mini_batch_move, dtype=np.long)).to(device),
            torch.from_numpy(np.array(mini_batch_win, dtype=np.float32).reshape((-1, 1))).to(device))
    
def accuracy(y, t):
    return (torch.max(y, 1)[1] == t).sum().item() / len(t)

def binary_accuracy(y, t):
    pred = y >= 0
    truth = t >= 0.5
    return pred.eq(truth).sum().item() / len(t)

def save_checkpoint(path, model, optimizer):        
    lg.logger_model.info('save checkpoint')
    checkpoint = {
        'model': model.state_dict(),
        'optimizer': optimizer.state_dict()
    }
    torch.save(checkpoint, path)


class Model():
    def __init__(self, name, mcts_player, model_path=None, resnets=config.RESNETS, channels=config.CHANNELS):
        lg.logger_main.info(f'INITIATE MODEL : {name}')
        print(f'INITIATE MODEL : {name}')

        self.name = name
        self.model_path = model_path
        self.mcts_player = mcts_player

        self.resnets = resnets
        self.channels = channels

        self.model = PolicyValueResNetwork(self.resnets, self.channels)
        self.model.to(device)
        self.optimizer = optim.SGD(self.model.parameters(), lr=config.LEARNING_RATE)

        if self.model_path is not None:
            checkpoint = torch.load(self.model_path, map_location=device)
            lg.logger_model.info(f'LOADING MODEL : {self.model_path}')
            print(f'LOADING MODEL : {self.model_path}')
            self.model.load_state_dict(checkpoint['model'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])

    def retrain(self, train_memory, batch_size=config.BATCH_SIZE, epoch=config.EPOCHES, eval_interval=10):
        writer = SummaryWriter()

        lg.logger_model.info(f'RETRAIN MODEL : {self.name}')
        print(f'RETRAIN MODEL : {self.name}')

        cross_entropy_loss = nn.CrossEntropyLoss()
        bce_with_logits_loss = nn.BCEWithLogitsLoss()

        lg.logger_main.info(f'NUM TRAIN POSITION {len(train_memory)}')

        # t = 0
        itr = 0
        # sum_loss1 = 0
        # sum_loss2 = 0
        # sum_loss = 0

        for e in range(epoch):
            epoch += 1
            itr_eval = 0
            sum_loss1_eval = 0
            sum_loss2_eval = 0
            sum_loss_eval = 0

            positions_train_shuffled = random.sample(train_memory, len(train_memory))
        
            for i in range(0, len(positions_train_shuffled)-(batch_size), batch_size):
                # itr += 1
                itr_eval += 1

                self.model.train()
                x, t1, t2 = mini_batch(positions_train_shuffled, i, batch_size)
                y1, y2 = self.model(x)

                loss1 = cross_entropy_loss(y1, t1)
                loss1 = loss1.mean()
                loss2 = bce_with_logits_loss(y2, t2)
                loss = loss1 + loss2

                self.model.zero_grad()
                loss.backward()
                self.optimizer.step()

                sum_loss1_eval += loss1.item()
                sum_loss2_eval += loss2.item()
                sum_loss_eval += loss.item()
            
            lg.logger_model.info('epoch = {}, iteration = {}, loss_policy = {}, loss_value = {}, loss = {}'.format(
                                e, itr, sum_loss1_eval/itr_eval, sum_loss1_eval/itr_eval, sum_loss1_eval/itr_eval))
            print('epoch = {}, iteration = {}, loss_policy = {}, loss_value = {}, loss = {}'.format(
                                e, itr, sum_loss1_eval/itr_eval, sum_loss1_eval/itr_eval, sum_loss1_eval/itr_eval))
            print('epoch = {}, iteration = {}, loss_policy = {}, loss_value = {}, loss = {}'.format(
                                epoch, itr, sum_loss1_eval/itr_eval, sum_loss1_eval/itr_eval, sum_loss1_eval/itr_eval))
            writer.add_scalar('Train_Loss_Policy/Iteration', sum_loss1_eval/itr_eval, e)
            writer.add_scalar('Train_Loss_Value/Iteration', sum_loss2_eval/itr_eval, e)
            writer.add_scalar('Train_Loss/Iteration', sum_loss_eval/itr_eval, e)

            writer.close()

                # sum_loss1 += loss1.item()
                # sum_loss2 += loss2.item()
                # sum_loss += loss.item()

            #     if t % eval_interval == 0:
            #         with torch.no_grad():
            #             x, t1, t2 = mini_batch_for_test(test_memory, batch_size)
            #             y1, y2 = self.model(x)

            #             loss1 = cross_entropy_loss(y1, t1)
            #             loss1 = loss1.mean()
            #             loss2 = bce_with_logits_loss(y2, t2)
            #             loss = loss1 + loss2

            #             lg.logger_model.info('epoch = {}, iteration = {}, loss_policy = {}, loss_value = {}, loss = {}, accuracy = {}, {}'.format(
            #                 epoch, t, sum_loss1/itr, sum_loss2/itr, sum_loss/itr ,accuracy(y1,t1), binary_accuracy(y2,t2)))

            #             itr = 0
            #             sum_loss1 = 0
            #             sum_loss2 = 0
            #             sum_loss = 0
                
            # lg.logger_model.info('VALIDATION')
            # itr_test = 0
            # sum_test_accuracy1 = 0
            # sum_test_accuracy2 = 0
            
            # with torch.no_grad():
            #     for i in range(0, len(test_memory)-batch_size, batch_size):
            #         x, t1, t2 = mini_batch_for_test(test_memory, batch_size)
            #         y1, y2 = self.model(x)

            #         itr_test += 1
            #         sum_test_accuracy1 += accuracy(y1, t1)
            #         sum_test_accuracy2 += binary_accuracy(y2, t2)

            #     lg.logger_model.info('epoch = {}, iteration = {}, loss_polish = {}, loss_value = {}, loss = {}, accuracy = {}, {}'.format(
            #         epoch, t, sum_loss1_eval/itr_eval, sum_loss2_eval/itr_eval, sum_loss_eval/itr_eval, sum_test_accuracy1/itr_test, sum_test_accuracy2/itr_test))

            #     writer.add_scalar('Train_Loss_Policy/Iteration', sum_loss1_eval/itr_eval, t)
            #     writer.add_scalar('Train_Loss_Value/Iteration', sum_loss2_eval/itr_eval, t)
            #     writer.add_scalar('Train_Loss/Iteration', sum_loss_eval/itr_eval, t)

            #     writer.add_scalar('Test_Acc_Policy/Iteration', sum_test_accuracy1/itr_test, t)
            #     writer.add_scalar('Test_Acc_/Iteration', sum_test_accuracy2/itr_test, t)

        lg.logger_model.info('END RETRAIN')
        print('END RETRAIN')
        self.model_path = './checkpoint/current/last'
        save_checkpoint(self.model_path, self.model, self.optimizer)

        # writer.close()
        
    def get_pred(self, test_memory, batch_size=config.BATCH_SIZE,):
        itr_test = 0
        sum_test_accuracy1 = 0
        sum_test_accuracy2 = 0

        with torch.no_grad():
            for i in range(0, len(test_memory)-batch_size, batch_size):
                x, t1, t2 = mini_batch_for_test(test_memory, batch_size)
                y1, y2 = self.model(x)

                itr_test += 1
                sum_test_accuracy1 += accuracy(y1, t1)
                sum_test_accuracy2 += binary_accuracy(y2, t2)

            lg.logger_main.info('ACCURACY_POLICY : {}, ACCURACY_VALUE : {}'.format(
                sum_test_accuracy1/itr_test, sum_test_accuracy2/itr_test))
            print('ACCURACY_POLICY : {}, ACCURACY_VALUE : {}'.format(
                sum_test_accuracy1/itr_test, sum_test_accuracy2/itr_test))


                
