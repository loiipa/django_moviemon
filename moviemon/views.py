from django.shortcuts import render
from Game import Game

# Create your views here.

def titlescreen(request):
	return render(request, "titlescreen.html",
	{'commands':{'btn_a':'worldmap/?key=new_game', 'btn_b':'options/load_game/', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

def worldmap(request):
	key = request.GET.get('key', None)

	# my_info.player.pos_x = pos[0]
	# my_info.player.pos_y = pos[1]
	my_info = Game()
	if key == 'new_game':
		my_info.movie.load_default_settings()
	else:
		my_info.load_data(my_info.load_cache())
		if key == 'Up' or key == 'Down' or key == 'Left' or key == 'Right':
			my_info.move_player(key)

	my_info.dump_cache(my_info.dump_data())

	return render(request, "worldmap.html",
	{'commands':{'btn_a':'../battle/', 'btn_b':'#', 'btn_start':'../options/', 'btn_select':'../moviedex/',
		'btn_up':'./?key=Up', 'btn_down':'./?key=Down', 'btn_left':'./?key=Left', 'btn_right':'./?key=Right'
		}, 'my_location_x':my_info.player.x_position(), 'my_location_y':my_info.player.y_position(), 'map_size_x':range(0, my_info.world.grid_x), 'map_size_y':range(0, my_info.world.grid_y)
		})

def battle(request):
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
	{'commands':{'btn_a':'save_game/', 'btn_b':'../', 'btn_start':'../worldmap', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

def save(request):
	return render(request, "save.html",
	{'commands':{'btn_a':'./', 'btn_b':'../', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

def load(request):
	return render(request, "load.html",
	{'commands':{'btn_a':'./', 'btn_b':'/', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

