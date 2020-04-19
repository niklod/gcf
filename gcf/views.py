from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Player


class PlayerView(generic.ListView):
    model = Player
    context_object_name = 'players_list'
