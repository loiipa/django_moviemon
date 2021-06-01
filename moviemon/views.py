from django.shortcuts import render
import Game
import random

# Create your views here.

g_pos = [0,0]
g_ball = 10

def titlescreen(request):
	return render(request, "titlescreen.html",
	{'commands':{'btn_a':'worldmap/?key=new_game', 'btn_b':'options/load_game/?indicator=a', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

def worldmap(request):
	key = request.GET.get('key', None)
	global g_pos
	global g_ball
	ball_got = False
	movie_got = False
	pos_tmp = g_pos
	btn_a = '#'
	moviemon_id = ''

	my_info = Game.Game()
	my_info.player.pos_x = g_pos[0]
	my_info.player.pos_y = g_pos[1]
	my_info.ball = g_ball

	if key == 'new_game':
		pass
	elif key == 'Up' or key == 'Down' or key == 'Left' or key == 'Right':
		g_pos = my_info.move_player(key)
	if g_pos != pos_tmp:
		event = random.randint(0, 5)
		if event == 0:
			my_info.ball += 1
			g_ball = my_info.ball
			ball_got = True
		elif event == 1:
			btn_a = '../battle/' + moviemon_id
			movie_got = True

	return render(request, "worldmap.html",
	{'commands':{'btn_a':btn_a, 'btn_b':'#', 'btn_start':'../options/', 'btn_select':'../moviedex/',
		'btn_up':'./?key=Up', 'btn_down':'./?key=Down', 'btn_left':'./?key=Left', 'btn_right':'./?key=Right'
		}, 'my_location_x':g_pos[0], 'my_location_y':g_pos[1],
		'map_size_x':range(0, my_info.world.grid_x), 'map_size_y':range(0, my_info.world.grid_y),
		'ball_count':g_ball, 'ball_got':ball_got, 'movie_got':movie_got
		})

def battle(request, moviemon_id):
	return render(request, "battle.html",
	{'commands':{'btn_a':'../battle', 'btn_b':'../worldmap', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

def moviedex(request):
	return render(request, "moviedex.html",
	{'commands':{'btn_a':'detail/', 'btn_b':'../worldmap', 'btn_start':'#', 'btn_select':'../worldmap/',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

def detail(request):
	return render(request, "detail.html",
	{'commands':{'btn_a':'#', 'btn_b':'../', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

def option(request):
	return render(request, "option.html",
	{'commands':{'btn_a':'save_game/?indicator=a', 'btn_b':'../', 'btn_start':'../worldmap', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

def save(request):
	indicator = request.GET.get('indicator', None)
	key = request.GET.get('key', None)

	if indicator == None:
		indicator = 'a'
	elif indicator == 'b' and key == 'Up' or indicator == 'c' and key == 'Down':
		indicator = 'a'
	elif indicator == 'c' and key == 'Up' or indicator == 'a' and key == 'Down':
		indicator = 'b'
	elif indicator == 'a' and key == 'Up' or indicator == 'b' and key == 'Down':
		indicator = 'c'

	return render(request, "save.html",
	{'commands':{'btn_a':'./?indicator=' + indicator, 'btn_b':'../', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'./?key=Up&indicator=' + indicator, 'btn_down':'./?key=Down&indicator=' + indicator, 'btn_left':'#', 'btn_right':'#'
		},'indicator':indicator
		})

def load(request):
	indicator = request.GET.get('indicator', None)
	key = request.GET.get('key', None)
	load_slot = request.GET.get('load_slot', None)

	if load_slot == None:
		load_slot = 'False'
	if indicator == None:
		indicator = 'a'
	elif indicator == 'b' and key == 'Up' or indicator == 'c' and key == 'Down':
		indicator = 'a'
	elif indicator == 'c' and key == 'Up' or indicator == 'a' and key == 'Down':
		indicator = 'b'
	elif indicator == 'a' and key == 'Up' or indicator == 'b' and key == 'Down':
		indicator = 'c'

	return render(request, "load.html",
	{'commands':{'btn_a':'./?load_slot=True&indicator=' + indicator, 'btn_b':'/', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'./?key=Up&indicator=' + indicator + '&load_slot=' + load_slot,
		'btn_down':'./?key=Down&indicator=' + indicator + '&load_slot=' + load_slot,
		'btn_left':'#', 'btn_right':'#'
		},'indicator':indicator, 'load_slot':load_slot
		})

