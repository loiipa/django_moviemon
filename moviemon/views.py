from django.shortcuts import render
import Game

# Create your views here.

pos = [0,0]

def titlescreen(request):
	return render(request, "titlescreen.html",
	{'commands':{'btn_a':'worldmap/?key=new_game', 'btn_b':'options/load_game/', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

def worldmap(request):
	key = request.GET.get('key', None)
	my_info = Game.Game()
	my_info.player.pos_x = pos[0]
	my_info.player.pos_y = pos[1]
	if key == 'new_game':
		pass
	elif key == 'Up' or key == 'Down' or key == 'Left' or key == 'Right':
		pos[0], pos[1] = my_info.move_player(key)

	return render(request, "worldmap.html",
	{'commands':{'btn_a':'../battle/', 'btn_b':'#', 'btn_start':'../options/', 'btn_select':'../moviedex/',
		'btn_up':'./?key=Up', 'btn_down':'./?key=Down', 'btn_left':'./?key=Left', 'btn_right':'./?key=Right'
		}, 'my_location_x':pos[0], 'my_location_y':pos[1], 'map_size_x':range(0, my_info.world.grid_x), 'map_size_y':range(0, my_info.world.grid_y)
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

