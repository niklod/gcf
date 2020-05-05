from django.http import Http404
from django.views import generic
from .models import Player, Game, PlayerConfig, PlayerStats
from django.shortcuts import get_object_or_404
from django.db.models import Avg, F, FloatField
from django.db.models.functions import Cast


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
        context['game'] = get_object_or_404(Game,
                                            slug=self.kwargs.get(
                                                'game_slug', ''))

        kda_annotate = Cast(F('total_kills'),
                            output_field=FloatField()) / Cast(
                                F('total_deaths'), output_field=FloatField())

        kill_per_round_annotate = Cast(
            F('total_kills'), output_field=FloatField()) / Cast(
                F('rounds_played'), output_field=FloatField())

        death_per_round_annotate = Cast(
            F('total_deaths'), output_field=FloatField()) / Cast(
                F('rounds_played'), output_field=FloatField())

        context['stats_avg'] = PlayerStats.objects.annotate(
            kill_per_round=kill_per_round_annotate,
            kda=kda_annotate,
            death_per_round=death_per_round_annotate).all().aggregate(
                Avg('rating'), Avg('total_kills'), Avg('total_deaths'),
                Avg('rounds_played'), Avg('damage_per_round'),
                Avg('grenade_damage_per_round'), Avg('assists_per_round'),
                Avg('headshots_percent'), Avg('kill_per_round'),
                Avg('death_per_round'), Avg('kda'))

        context['player_stats'] = PlayerStats.objects.filter(
            game__id=context['game'].id,
            player__id=context['player'].id).annotate(
                kda=kda_annotate,
                kill_per_round=kill_per_round_annotate,
                death_per_round=death_per_round_annotate).first()

        config = PlayerConfig.objects.filter(
            game__id=context['game'].id,
            player__id=context['player'].id).first()

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
