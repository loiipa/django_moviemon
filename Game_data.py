import os
#from django.conf import settings
import pickle
import glob

class GameData:

    @staticmethod
    def str_builder(id = '', movie_balls = 10, score = 0):
        return "slot{id}_{ball}_{score}.mmg".format(id = id, ball = movie_balls, score = score)

    @staticmethod
    def save(id = ''):
        try:
            cache = GameData.__load_cache()
            for p in glob.glob('slot'+id+'_*_*.mmg'):
                print(p)
                os.remove(p)
            with open(GameData.str_builder(id, cache['ball_count'], len(cache['captured'])), 'wb') as file:
                pickle.dump(cache, file)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def __load_cache():
        _cache = {}
        with open('cache.pkl', 'rb') as cache:
            _cache = pickle.load(cache)
        return _cache

    @staticmethod
    def load(id = ''):
        try:
            file_name = glob.glob('slot'+id+'_*_*.mmg')
            print(file_name)
            if len(file_name) > 1 or len(file_name) == 0:
                return False
            with open(file_name[0], 'rb') as file:
                GameData.__dump_cache(file)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def __dump_cache(_cache):
        _cache = {}
        with open('cache.pkl', 'wb') as cache:
            pickle.dump(_cache, cache)

# #     # @staticmethod
# #     # def get_file_list(args):


# def main():
#     print(GameData.save('A'))
#     print(GameData.load('A'))

# if __name__ == "__main__":
#     main()
