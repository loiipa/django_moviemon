import sys
import random
from django.utils.functional import Promise
import requests
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
    def __init__(self, x = 0, y = 0, id = "", power = 0):
        super().__init__(x, y)
        self.id = id
        self.set_power(power)

    # def movie_id(self):
    #     return self._info['id']

class World:

    def __init__(self, size_x = 10, size_y = 10):
        self.grid_x = size_x
        self.grid_y = size_y
        #moviemon생성, 배치
        
class Game:

    def __init__(self, ball_count = 10):
        self.player = Player()
        self.world = World()
        self.ball = ball_count
        # MOVIES리스트로 Dic 만들기

    def __imDB(self, id = 0):
        params = { 'i':id, 'r':'json', 'apikey':"c94fad6" }
        URL = 'http://www.omdbapi.com/'
    #////////////////
    #/Player control/
    #////////////////
    def __move_player_Down(self):
        if self.player.y_position() >= self.world.grid_y - 1:
            return None
        return self.player.move(0, -1)
    def __move_player_Up(self):
        if self.player.y_position() <= 0:
            return None
        return self.player.move(0, 1)
    def __move_player_Right(self):
        if self.player.x_position() >= self.world.grid_x - 1:
            return None
        return self.player.move(1, 0)
    def __move_player_Left(self):
        if self.player.x_position() <= 0:
            return None
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
        if self.ball <= 0:
            return None
        self.ball -= 1
        if self.player.attack(moviemon) == True:
            #잡았을 때 분기
            return True
        else:
            #놓쳤을 때 분기
            return False
