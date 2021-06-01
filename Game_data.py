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
        # try:
            if not os.path.exists('saved_game'):
                os.makedirs('saved_game')
            with open('cache.pkl', 'rb') as _cache:
                cache = pickle.load(_cache)
            print(cache)
            for p in glob.glob('saved_game/slot'+id+'_*_*.mmg'):
                os.remove(p)
            if len(cache) > 0:
                with open(GameData.str_builder(id, cache['ball_count'], len(cache['captured'])), 'wb') as file:
                    pickle.dump(cache, file)
                    return True
            return False
        # except Exception as e:
        #     print(e)
        #     return False

    @staticmethod
    def load(id = ''):
        # try:
            if not os.path.exists('saved_game'):
                return False
            file_name = glob.glob('saved_game/slot'+id+'_*_*.mmg')
            if len(file_name) > 1 or len(file_name) == 0:
                return False
            with open(file_name[0], 'rb') as file:
                data = pickle.load(file)
            with open('cache.pkl', 'wb') as cache:
                pickle.dump(cache, data)
            return True
        # except Exception as e:
        #     print(e)
        #     return False
    
#     # @staticmethod
#     # def get_file_list(args):

def main():
    print(GameData.save('A'))
    print(GameData.load('A'))

if __name__ == "__main__":
    main()