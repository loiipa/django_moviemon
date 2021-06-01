import os
from django.conf import settings
import Game
import pickle

class GameData:

    def __init__(self):
        #slot<n>_<movieball>_<score>.mmg 파일을 찾음. 
        pass

    @staticmethod
    def __load_cache(save_file):
        _cache = {}
        with open('cache.pkl', 'rb') as cache:
            _cache = pickle.load(cache)
        return _cache

    @staticmethod
    def str_builder(id = '', movie_balls = 10, score = 0):
        return "slot{id}_{ball}_{score}.mmg".format(id = id, ball = movie_balls, score = score)
        
    @staticmethod
    def save(id = ''):
        try:
            cache = GameData.__dump_cache()
            file = open(GameData.str_builder(id, cache['strength'], len(cache['captured']), 'w'))
            file.write(cache)
            file.close()
            return True
        except:
            return False
        
    @staticmethod
    def __dump_cache():
        _cache = {}
        with open('cache.pkl', 'wb') as cache:
            pickle.dump(_cache, cache)
