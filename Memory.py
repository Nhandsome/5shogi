from shogi.read_kifu import *
from utils.filter_csa import *
from utils.make_kifu_list import *

import loggers as lg
import pickle
import config
import os

class Memory:

    def __init__(self, position=[]):
        self.MEMORY_SIZE = config.MEMORY_SIZE
        self.position = position
        self.len_memory = len(self.position)
    
    def filter_csa(self, raw_csa_folder):
        lg.logger_main.info(f'FILTER KIFU MEMORIES : {raw_csa_folder}')
        print((f'FILTER KIFU MEMORIES : {raw_csa_folder}'))

        filter_csa_files(raw_csa_folder)

        lg.logger_main.info(f'CLEAN KIFU MEMORIES')
        os.makedirs('./data/temp', exist_ok=True)
        print(f'CLEAN KIFU MEMORIES')
        make_kifu(raw_csa_folder, './data/temp/kifu_list', 1)
    
    def make_kifu_pickle(self, csa_path):
        os.makedirs('./data/pickle/', exist_ok=True)

        position = read_kifu('./data/temp/kifu_list_train.txt')
        
        with open(f'{csa_path}.pickle', 'wb') as f:
            pickle.dump(position, f, pickle.HIGHEST_PROTOCOL)

        lg.logger_main.info(f'SAVE KIFU PICKLE : {csa_path}')
        print(f'SAVE KIFU PICKLE : {csa_path}')

        self.position = position
        self.len_memory = len(position)

        return position

# if __name__=='__main__':
#     # test = Csa(100)
#     # # test.filter_memory('./data/csa/csa_1')
#     # test.make_kifu_pickle('./data/csa/temp/kifu_list_train.txt','./data/pickle/csa_1.pickle')