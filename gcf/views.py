from django.http import Http404
from django.views import generic
from .models import Player, Game, PlayerConfig
from django.shortcuts import get_object_or_404


class PlayerView(generic.ListView):
    model = Player


class PlayerDetailView(generic.DetailView):
    model = Player

    def get_object(self):
        player_slug = self.kwargs.get('player_slug')
        obj = get_object_or_404(Player, slug=player_slug)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = get_object_or_404(Game, slug=self.kwargs.get('game_slug', ''))
        config = PlayerConfig.objects.filter(game__id=context['game'].id, player__id=context['player'].id).first()

        if config:
            context['config'] = config
        else:
            raise Http404('Конфига не существует')

        return context


class GameView(generic.DetailView):
    model = Game

    def get_object(self):
        game_slug = self.kwargs.get('game_slug')
        obj = get_object_or_404(Game, slug=game_slug)
        return obj
