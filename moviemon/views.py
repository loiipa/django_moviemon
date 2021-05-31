from django.shortcuts import render

# Create your views here.

def titlescreen(request):
	return render(request, "titlescreen.html",
	{'commands':{'btn_a':'worldmap/', 'btn_b':'options/load_game/', 'btn_start':'#', 'btn_select':'#',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

def worldmap(request):
	return render(request, "worldmap.html",
	{'commands':{'btn_a':'../battle/', 'btn_b':'#', 'btn_start':'../options/', 'btn_select':'../moviedex/',
		'btn_up':'#', 'btn_down':'#', 'btn_left':'#', 'btn_right':'#'
		}})

def battle(request):
	return render(request, "battle.html")

def moviedex(request):
	return render(request, "moviedex.html")

def detail(request):
	return render(request, "detail.html")

def option(request):
	return render(request, "option.html")

def save(request):
	return render(request, "save.html")

def load(request):
	return render(request, "load.html")
