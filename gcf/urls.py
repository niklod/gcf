from django.urls import path
from .views import PlayerView, PlayerDetailView

app_name = 'gcf'
urlpatterns = [
    path('players/', PlayerView.as_view(), name='players_list'),
    path('players/<int:pk>/', PlayerDetailView.as_view(), name='player_detail'),
]