from django.shortcuts import render
import Game
import random

def titlescreen(request):
	return render(request, "titlescreen.html",
	{'commands':{'btn_a':'worldmap/?key=new_game', 'btn_b':'options/load_game/?indicator=a', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})


def location(pos):
	if pos is None:
		return '#'
	else:
		return "/worldmap?x={}&y={}".format(pos[0], pos[1])

def worldmap(request):
	key = request.GET.get('key', None)
	x = int(request.GET.get('x', -1))
	y = int(request.GET.get('y', -1))
	ball_got = False
	movie_got = False
	btn_a = '#'
	moviemon_id = ''
	my_info = Game.Game()

	if key == 'new_game':
		my_info.movie.load_default_settings()
		x = my_info.player.x_position()
		y = my_info.player.y_position()
	else:
		my_info.load_data(my_info.load_cache())
		if x == -1 and y == -1:
			x = my_info.player.x_position()
			y = my_info.player.y_position()
		if x != my_info.player.x_position() or y != my_info.player.y_position():
			event = random.randint(0, 5)
			if event == 0:
				my_info.movie_balls += 1
				ball_got = True
			elif event == 1:
				""" Moviemon 임의로 표기 """
				moviemon_id = 'tt0468492'
				btn_a = '../battle/' + moviemon_id
				movie_got = True
		my_info.player.pos_x = x
		my_info.player.pos_y = y
	my_info.dump_cache(my_info.dump_data())

	return render(request, "worldmap.html",
	{'commands':{'btn_a':btn_a, 'btn_b':'#', 'btn_start':'../options/', 'btn_select':'../moviedex/',
		'btn_up':location(my_info.move_player('Up')), 'btn_down':location(my_info.move_player('Down')),
		'btn_left':location(my_info.move_player('Left')), 'btn_right':location(my_info.move_player('Right'))
		},
		'my_location_x':my_info.player.x_position(), 'my_location_y':my_info.player.y_position(),
		'map_size_x':range(0, my_info.world.grid_x), 'map_size_y':range(0, my_info.world.grid_y),
		'ball_count':my_info.movie_balls, 'ball_got':ball_got, 'movie_got':movie_got
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

