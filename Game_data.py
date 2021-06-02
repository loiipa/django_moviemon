import os
from django.conf import settings
import pickle
import glob

class GameData:

    @staticmethod
    def str_builder(id = '', movie_balls = settings.BALL_COUNT, score = 0):
        return "saved_game/slot{id}_{ball}_{score}.mmg".format(id = id, ball = movie_balls, score = score)
        
    @staticmethod
    def save(id = ''):
        try:
            if not os.path.exists('saved_game'):
                os.makedirs('saved_game')
            with open('cache.pkl', 'rb') as _cache:
                cache = pickle.load(_cache)
            for p in glob.glob('saved_game/slot'+id+'_*_*.mmg'):
                os.remove(p)
            if len(cache) > 0:
                with open(GameData.str_builder(id, len(cache['captured']), len(cache['moviedex'])), 'wb') as file:
                    pickle.dump(cache, file)
                    return True
            return False
        except GameData.GameDataError as e:
            print(e)
            return False

    @staticmethod
    def load(id = ''):
        try:
            if not os.path.exists('saved_game'):
                return False
            file_name = glob.glob('saved_game/slot'+id+'_*_*.mmg')
            if len(file_name) > 1 or len(file_name) == 0:
                return False
            with open(file_name[0], 'rb') as file:
                data = pickle.load(file)
            with open('cache.pkl', 'wb') as cache:
                pickle.dump(data, cache)
            return True
        except GameData.GameDataError as e:
            print(e)
            return False
   
    @staticmethod
    def __make_slot_name(slot_file_name = ''):
        name_list = slot_file_name.replace('saved_game/', '').split('_')
        name = name_list[1]+'/'+name_list[2].replace('.mmg', '')
        return name
        

    @staticmethod
    def get_save_list():
        sav_lst = ['Free', 'Free', 'Free']
        a_file = glob.glob('saved_game/slotA_*_*.mmg')
        if len(a_file) == 1:
            sav_lst[0] = GameData.__make_slot_name(a_file[0])
        b_file = glob.glob('saved_game/slotB_*_*.mmg')
        if len(b_file) == 1:
            sav_lst[1] = GameData.__make_slot_name(b_file[0])
        c_file = glob.glob('saved_game/slotC_*_*.mmg')
        if len(c_file) == 1:
            sav_lst[2] = GameData.__make_slot_name(c_file[0])
        return sav_lst

    @staticmethod
    class GameDataError(Exception):
        def __init__(self, str = 'GameDataError : Game_data.py'):
            super().__init__(str)
            