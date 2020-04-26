from django.urls import path
from .views import PlayerDetailView, GameView


app_name = 'gcf'
urlpatterns = [
    path('<str:game_slug>/', GameView.as_view(), name='game_detail'),
    path('<str:game_slug>/<str:player_slug>/', PlayerDetailView.as_view(), name='player_detail'),
]
