from roster.models import Team, Player, SeasonStats, Season
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def home(request):
	context = {
		'teams': Team.objects.all()
	}
	return render(request, "roster/home.html", context)

def team(request, pk):
	context = {
		'team': get_object_or_404(Team, id=pk),
		'stats': SeasonStats.objects.get(team=get_object_or_404(Team, id=pk)),
		'players': Player.objects.filter(team=get_object_or_404(Team, id=pk)),
		'teams': Team.objects.all()
	}
	return render(request, "roster/team.html", context)

def player(request, pk):
	context = {
		'player': get_object_or_404(Player, id=pk),
		'stats': SeasonStats.objects.get(player=get_object_or_404(Player, id=pk)),
		'teams': Team.objects.all()
	}
	return render(request, "roster/player.html", context)