from django.test import TestCase
from django.urls import reverse
from .models import Player


class PlayerViewsTest(TestCase):

    def test_player_list_view(self):
        response = self.client.get(reverse('gcf:players_list'))

        self.assertIs(response.status_code, 200)

    def test_player_detail_view(self):
        test_player = Player(name='Test Player', age=123, description='Test Description')
        test_player.save()

        # response = self.client.get(f'/players/{test_player.pk}/')
        response = self.client.get(reverse('gcf:player_detail', kwargs={'pk': test_player.pk}))

        self.assertIs(response.status_code, 200)
        self.assertContains(response, test_player.name)
