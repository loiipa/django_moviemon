import sys
import random
from django.utils.functional import Promise
import requests
import pickle
from django.conf import settings

class GameObject:
    def __init__(self, x = 0, y = 0):
        self.pos_x = x
        self.pos_y = y

    def x_position(self):
        return self.pos_x

    def y_position(self):
        return self.pos_y

    def position(self):
        return self.pos_x, self.pos_y

    def set_power(self, power = 0):
        self.power = power

    def add_power(self, inc = 1):
        self.power += inc

    def strength(self):
        return self.power

class Player(GameObject):

    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)
        self.set_power()

    def load_data(self, cache):
        self.pos_x = cache['player_pos'][0]
        self.pos_y = cache['player_pos'][1]
        self.set_power(cache['strength'])

    def move(self, x_inc, y_inc):
        self.pos_x += x_inc
        self.pos_y += y_inc
        return self.position()

    def attack(self, monster_power):
        atk = 50 - (monster_power * 10) + (self.strength * 5)
        if atk < 1:
            atk = 1
        if atk > 90:
            atk = 90
        r_num = random.range(0, 100)
        if r_num < atk:
            return True
        return False

class Movimon(GameObject):
    #영화 정보
    def __init__(self, id = "", power = 0):
        super().__init__()
        self.id = id
        self.set_power(power)

    # def movie_id(self):
    #     return self._info['id']

class World:

    def __init__(self, size_x = 10, size_y = 10):
        self.grid_x = size_x
        self.grid_y = size_y

    def load_data(self, cache):
        None

class Movie:

    def __init__(self):
        self.captured = []

    def load_data(self, cache):
        self.captured = cache['captured']
        self.moviedex = cache['moviedex']

    def capture(self, id):
        self.captured.append(id)

    def get_random_movie(self):
        result = True
        while result:
            dup = self.captured
            id = random.choice(settings.MOVIES)
            dup.append(id)
            if len(dup) != len(set(dup)):
                result = False
            dup.remove(id)
        return id, self.moviedex[id]

    @staticmethod
    def get_movie(self, id = ''):
        params = { 'i':id, 'r':'json', 'apikey':"c94fad6" }
        URL = 'http://www.omdbapi.com/'
        response = requests.get(URL, params = params)
        my_json = response.json()
        return my_json

    def load_default_settings(self, lst = settings.MOVIES):
        dic = {}
        for movie in lst:
            this_json = Movie.get_movie(movie)
            dic[movie] = this_json
        self.moviedex = dic

class Game:

    def __init__(self, ball_count = 10):
        self.player = Player()
        self.world = World()
        self.movie = Movie()
        self.movie_balls = ball_count

    #////////////////
    #//data control//
    #////////////////
    
    def dump_data(self):
        return {
            'player_pos' : self.player.position(),
            'ball_count' : self.movie_balls,
            'strength' : self.player.strength(),
            'captured' : self.movie.captured,
            'moviedex' : self.movie.moviedex
        }

    def load_data(self, cache):
        self.player.load_data(cache)
        self.world.load_data(cache)
        self.movie.load_data(cache)
        self.movie_balls = cache['ball_count']

    #////////////////
    #/Player control/
    #////////////////
    
    def __move_player_Up(self):
        if self.player.y_position() >= self.world.grid_y - 1:
            return self.player.position()
        return self.player.move(0, 1)
    def __move_player_Down(self):
        if self.player.y_position() <= 0:
            return self.player.position()
        return self.player.move(0, -1)
    def __move_player_Right(self):
        if self.player.x_position() >= self.world.grid_x - 1:
            return self.player.position()
        return self.player.move(1, 0)
    def __move_player_Left(self):
        if self.player.x_position() <= 0:
            return self.player.position()
        return self.player.move(-1, 0)
    _player_move = {
        'Up'    :   __move_player_Down,
        'Down'  :   __move_player_Up,
        'Left'  :   __move_player_Left,
        'Right' :   __move_player_Right
    }
    
    def move_player(self, order):
        return (self._player_move[order](self))

    def player_Attack(self, moviemon):
        if self.movie_balls <= 0:
            return None
        self.movie_balls -= 1
        if self.player.attack(moviemon) == True:
            #잡았을 때 분기
            return True
        else:
            #놓쳤을 때 분기
            return False
    
    #////////////////
    #//pickle_cache//
    #////////////////
    
    def dump_cache(self, _cache):
        with open('cache.pkl', 'wb') as cache:
            pickle.dump(_cache, cache)
    
    def load_cache(self):
        self.cache = {}
        with open('cache.pkl', 'rb') as cache:
            self.cache = pickle.load(cache)
        return self.cache

def main():
    game = Game()
    game.movie.load_default_settings()
    print(game.movie.moviedex.items())

if __name__ == "__main__":
    main()