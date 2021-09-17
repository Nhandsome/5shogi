from Memory import *
from Train import *
from importlib import reload
from shogi import cli

import config

import loggers as lg
import pickle
import os
import random

path = os.getcwd()

lg.logger_main.info('=============================================')
lg.logger_main.info('===============    NEW LOG    ===============')
lg.logger_main.info('=============================================')
print('=============================================')
print('===============    NEW LOG    ===============')
print('=============================================')

###########################################################################
#######################   INITIATION   
###########################################################################
####################### config.pyも参考に

## 並列化 Monte Carlo Tree Searchを行う PLAYER
player_1 = f'{path}/parallel_mcts_player_1.sh'
player_2 = f'{path}/parallel_mcts_player_2.sh'

## Pre-trained BASE POLICY VALUE MODEL
## MODEL / OPTIMIZER 初期化に使う
current_pv = f'{path}/checkpoint/base/base_pv'

## PICKLE INIT DATASET
## Noneの場合は、0から対局データセットを作る
## config.MEMORY_SIZEまで）
# init_csa = f'{path}/data/pickle/csa.pickle'
init_csa = None

## {path}/checkpoint/best/best_pv_{init_best_version}
## の形でPre-trained ModelをSaveすること
## Noneの場合は、currnet_pvと同じ
init_best_version = 1
# init_best_version = 0

## SELF MATCHデータをSAVEするFolder
current_csa = f'{path}/data/csa_current'

###########################################################################
###########################################################################

####################### LOAD INIT CSA_FILES
## momoryに  対局データ（POLICY VALUE NETWORKの学習データ）を保存
if init_csa is not None:
    with open(f'{init_csa}', 'rb') as f:
        position = pickle.load(f)
    lg.logger_main.info(f'LOAD CSA : {init_csa}')
    print(f'LOAD CSA : {init_csa}')
    memory = Memory(position)
else:
    print(f'INIT CSA')
    memory = Memory()

lg.logger_main.info(f'MEMORY LENGTH : {memory.len_memory}')
print(f'MEMORY LENGTH : {memory.len_memory}')   

####################### INIT MODELS

## current_pv / best_pv : PATH of Pre-trained Policy Value Network Model
if init_best_version is not None:
    best_pv = f'{path}/checkpoint/best/best_pv_{init_best_version}'
else:
    best_pv = current_pv
    
## POLICY VALUE NETWORK の　NAME / MCTS PLAYER / MODEL PATH   
current_m = Model('current_player', player_1, current_pv)
best_m= Model(f'best_pv_{init_best_version}', player_2, best_pv)

lg.logger_main.info(f'INIT MODELS')
lg.logger_main.info(f'CURRENT MODELS : {current_m.name}')
lg.logger_main.info(f'BEST MODELS : {best_m.name}')
print(f'INIT MODELS')
print(f'CURRENT MODELS : {current_m.name}')
print(f'BEST MODELS : {best_m.name}')

###########################################################################
####################   ITERATION FOR SELF LEARNING  ####################
###########################################################################
lg.logger_main.info(f'#################################  SELF MATCH  #################################')
print(f'#################################  SELF MATCH  #################################')
itr = 0
best_version = init_best_version

while True:
    itr += 1
    reload(lg)

    print(f'ITERATION NUMBER {str(itr)}')

    lg.logger_main.info(f'BEST PLAYER VERSION : {best_version}')
    print(f'BEST PLAYER VERSION : {best_version}')

    lg.logger_main.info(f'####################  PLAY MATCHES (BEST_{best_version} VS BEST_{best_version})  ####################')
    print(f'####################  PLAY MATCHES (BEST_{best_version} VS BEST_{best_version})  ####################')

    ####################  SELF MATCH

    print('SELF MATCH...')
    options_b = {'modelfile':best_m.model_path,'temperature':config.TEMPERATURE,'playout':config.MCTS_SIMS}
    cli.main(best_m.mcts_player, best_m.mcts_player, options1=options_b, options2=options_b, names=[best_m.name, best_m.name], csa=current_csa, games=config.ROUNDS, draw=config.DRAW)
    print('')

    lg.logger_main.info(f'END MATCHES (BEST_{best_version} VS BEST_{best_version})')
    print(f'END MATCHES (BEST_{best_version} VS BEST_{best_version})')

    temp_memory = Memory()
    temp_memory.filter_csa(current_csa)
    temp_memory.make_kifu_pickle(f'{path}/data/pickle/csa_{itr}')

    memory.position += temp_memory.position
    memory.len_memory += temp_memory.len_memory

    lg.logger_main.info(f'MEMORIES : {memory.len_memory} / {config.MEMORY_SIZE}')
    print(f'MEMORIES : {memory.len_memory} / {config.MEMORY_SIZE}')
    
    if memory.len_memory >= config.MEMORY_SIZE:
        lg.logger_main.info(f'####################  GET ENOUGH CSA FILES TO RETRAIN ####################')
        print(f'####################  GET ENOUGH CSA FILES TO RETRAIN  ####################')
        
        lg.logger_main.info(f'####################  START RETRAINING ####################')
        print(f'####################  START RETRAINING  ####################')

        print('RETRAINING...')
        current_m.retrain(memory.position)
        print('')

        lg.logger_main.info(f'####################  END RETRAINING ####################')
        print(f'####################  END RETRAINING  ####################')

        test_sample = random.sample(memory.position, min(1000, len(memory.position)))

        lg.logger_main.info(f'TEST CURRENT MODEL')
        print(f'TEST CURRENT MODEL')
        current_m.get_pred(test_sample)

        lg.logger_main.info(f'TEST BEST MODEL')
        print(f'TEST BEST MODEL')
        best_m.get_pred(test_sample)

        lg.logger_main.info(f'####################  PLAY MATCHES (current_pv VS best_pv_{init_best_version})  ####################')
        print(f'####################  PLAY MATCHES (current_pv VS best_pv_{init_best_version})  ####################')

        options_c = {'modelfile':current_m.model_path,'temperature':config.TEMPERATURE,'playout':config.MCTS_SIMS}
        options_b = {'modelfile':best_m.model_path,'temperature':config.TEMPERATURE,'playout':config.MCTS_SIMS}
        
        match_result = cli.main(current_m.mcts_player, best_m.mcts_player, options1=options_c, options2=options_b, names=[current_m.name, best_m.name], csa=current_csa, games=config.EVAL_ROUNDS, draw=config.DRAW)
        
        c_name, b_name, c_won, b_won, total = match_result['engine1_name'], match_result['engine2_name'], match_result['engine1_won'], match_result['engine2_won'], match_result['total']

        lg.logger_main.info(f'####################  MATCHES RESULT (current_pv VS best_pv_{init_best_version})  ####################')
        lg.logger_main.info(f'####################  {c_name} WON : {c_won} / {total}  ####################')
        lg.logger_main.info(f'####################  {b_name} WON : {b_won} / {total}  ####################')
        print(f'####################  MATCHES RESULT (current_pv VS best_pv_{init_best_version})  ####################')
        print(f'####################  {c_name} WON : {c_won} / {total}  ####################')
        print(f'####################  {b_name} WON : {b_won} / {total}  ####################')

        if c_won > b_won + config.EVAL_THRESHOLD:
            lg.logger_main.info(f'####################  UPDATE BEST MODEL VERSION  ####################')
            print(f'####################  UPDATE BEST MODEL VERSION  ####################')
            best_version += 1
            best_pv = f'{path}/checkpoint/best/best_pv_{best_version}'
            save_checkpoint(best_pv, current_m.model, current_m.optimizer)
            best_m = Model(f'best_pv_{best_version}', player_2, best_pv)
            lg.logger_main.info(f'SAVE NEW BEST MODEL : {best_m.name}')
            print(f'SAVE NEW BEST MODEL : {best_m.name}')
            # current_m = base_m

