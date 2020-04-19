from django.test import TestCase

from .models import Player


class PlayerViewsTest(TestCase):

    def test_player_list_view(self):
        response = self.client.get('/players/')

        self.assertIs(response.status_code, 200)

    def test_player_detail_view(self):
        test_player = Player(name='Test Player', age=123, description='Test Description')
        test_player.save()

        response = self.client.get(f'/players/{test_player.pk}/')

        self.assertIs(response.status_code, 200)
        self.assertContains(response, test_player.name)
