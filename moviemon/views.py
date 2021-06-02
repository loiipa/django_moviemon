from django.shortcuts import render
import Game
import Game_data
import random

def titlescreen(request):
	return render(request, "titlescreen.html",
	{'commands':{'btn_a':'worldmap/?key=new_game', 'btn_b':'options/load_game/', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})


def location(pos):
	if pos is None:
		return '#'
	else:
		return "/worldmap?x={}&y={}&".format(pos[0], pos[1])

def worldmap(request):
	key = request.GET.get('key', '')
	x = int(request.GET.get('x', -1))
	y = int(request.GET.get('y', -1))

	ball_got = False
	movie_got = False
	btn_a = '#'
	moviemon_id = ''
	my_info = Game.Game()

	if key == 'new_game':
		my_info.load_default_settings()
		x, y = my_info.player.position()
	else:
		my_info.load_data(my_info.load_cache())

		if x == -1 and y == -1:
			x, y = my_info.player.position()
			x = my_info.player.x_position()
			y = my_info.player.y_position()

		if x != my_info.player.x_position() or y != my_info.player.y_position():
			if my_info.battle_status() == True:
				my_info.battle_end()
			event = random.randint(0, 5)
			if event == 0 or event == 1:
				my_info.movie_balls += 1
				ball_got = True
			elif event == 2 and len(my_info.movie.moviedex) > len(my_info.movie.captured):
				my_info.battle_start()
		if my_info.battle_status() == True:
			moviemon_id = my_info.get_random_movie()
			btn_a = '../battle/' + moviemon_id[0]
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
	my_info = Game.Game()
	my_info.load_data(my_info.load_cache())

	result = request.GET.get('result', 'first')
	btn_a = '#'
	movie_info = my_info.get_movie(moviemon_id)

	if result == 'first':
		mention_A = 'Press A! You Can catch that!'
		mention_C = ''
		result = None
		btn_a = './' + moviemon_id + '?result=' + str(result)
	else:
		result = my_info.player_Attack(moviemon_id)
		if result == None:
			mention_A = 'Go Away!'
			mention_C = 'Your Ball is empty.'
		elif result == True:
			mention_A = ''
			mention_C = 'Gotcha!'
		elif result == False:
			mention_A = 'A - Launch Movieball'
			mention_C = 'Unfortunately missed!'
			btn_a = './' + moviemon_id + '?result=' + str(result)

	my_info.battle_end()
	my_info.dump_cache(my_info.dump_data())

	return render(request, "battle.html",
	{'commands':{'btn_a':btn_a, 'btn_b':'../worldmap', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		},'mention_A':mention_A, 'mention_C':mention_C, 'balls' : my_info.movie_balls,
		'player_strength':my_info.get_strength(), 'movie_strength':int(float(movie_info['imdbRating']) * 10),
		'rate':my_info.player.percentage(float(movie_info['imdbRating'])),
		'image':movie_info['Poster'], 'title':movie_info['Title'], 'imdbRating':movie_info['imdbRating'],
		})

def moviedex(request):
	my_info = Game.Game()
	my_info.load_data(my_info.load_cache())
	key = int(request.GET.get('key', 0))
	post_list = []
	title_list = []
	show_list = []
	moviemon_id = ''

	print(my_info.cache['moviedex'])

	movie_count = len(my_info.movie.captured)

	if movie_count == 1:
		show_list = [0]
		key = 0
	elif movie_count == 2:
		key %= 2
		if key == 0:
			show_list = [0, 1]
		else:
			show_list = [1, 0]
	elif movie_count >= 3:
		for i in range(key-1, key+2):
			if i < 0:
				i += movie_count
			elif i >= movie_count:
				i -= movie_count
			show_list.append(i)
		if key < 0:
			key += movie_count
		elif key >= movie_count:
			key -= movie_count
	for i in show_list:
		id = my_info.movie.captured[i]
		post_list.append(my_info.movie.moviedex[id]['Poster'])
		title_list.append(my_info.movie.moviedex[id]['Title'])
	if movie_count > 0:
		moviemon_id = my_info.movie.captured[key]

	return render(request, "moviedex.html",
	{'commands':{'btn_a':'detail/' + moviemon_id + '?key=' + str(key), 'btn_b':'#', 'btn_start':'#', 'btn_select':'../worldmap/',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'./?key=' + str(key - 1), 'btn_right':'./?key=' + str(key + 1)
		},'post_list':post_list, 'title_list':title_list, 'movie_count':movie_count
		})

def detail(request, moviemon_id):
	key = int(request.GET.get('key', 0))
	my_info = Game.Game()
	movie_info = my_info.get_movie(moviemon_id)

	return render(request, "detail.html",
	{'commands':{'btn_a':'#', 'btn_b':'../?key='+ str(key), 'btn_start':'#', 'btn_select':'#', 'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		},'image':movie_info['Poster'], 'title':movie_info['Title'], 'year':movie_info['Year'], 'genre':movie_info['Genre'],'imdbRating':float(movie_info['imdbRating']),'plot':movie_info['Plot']
		})

def option(request):
	return render(request, "option.html",
	{'commands':{'btn_a':'save_game/', 'btn_b':'../', 'btn_start':'../worldmap', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

def save(request):
	indicator = request.GET.get('indicator', None)
	key = request.GET.get('key', None)
	save_slot = bool(request.GET.get('save_slot', False))

	if indicator == None:
		indicator = 'A'
	elif indicator == 'B' and key == 'Up' or indicator == 'C' and key == 'Down':
		indicator = 'A'
	elif indicator == 'C' and key == 'Up' or indicator == 'A' and key == 'Down':
		indicator = 'B'
	elif indicator == 'A' and key == 'Up' or indicator == 'B' and key == 'Down':
		indicator = 'C'

	if save_slot == True:
		Game_data.GameData.save(indicator)

	sav_lst = Game_data.GameData.get_save_list()

	return render(request, "save.html",
	{'commands':{'btn_a':'./?save_slot=True&indicator=' + indicator, 'btn_b':'../', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'./?key=Up&indicator=' + indicator, 'btn_down':'./?key=Down&indicator=' + indicator, 'btn_left':'#', 'btn_right':'#'
		},'indicator':indicator, 'sav_lst':sav_lst
		})

def load(request):
	indicator = request.GET.get('indicator', None)
	key = request.GET.get('key', None)
	load_slot = bool(request.GET.get('load_slot', False))

	if indicator == None:
		indicator = 'A'
	elif indicator == 'B' and key == 'Up' or indicator == 'C' and key == 'Down':
		indicator = 'A'
	elif indicator == 'C' and key == 'Up' or indicator == 'A' and key == 'Down':
		indicator = 'B'
	elif indicator == 'A' and key == 'Up' or indicator == 'B' and key == 'Down':
		indicator = 'C'

	btn_a = './?load_slot=True&indicator=' + indicator
	if load_slot == True:
		if Game_data.GameData.load(indicator) == True:
			btn_a = '/worldmap/?key=load_game'

	sav_lst = Game_data.GameData.get_save_list()

	return render(request, "load.html",
	{'commands':{'btn_a':btn_a, 'btn_b':'/', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'./?key=Up&indicator=' + indicator, 'btn_down':'./?key=Down&indicator=' + indicator,
		'btn_left':'#', 'btn_right':'#'
		},'indicator':indicator, 'load_slot':load_slot, 'sav_lst':sav_lst
		})

