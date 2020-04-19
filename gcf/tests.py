from django.test import TestCase
from django.urls import reverse
from .models import Player, User


class ViewsTest(TestCase):

    def test_player_list_view(self):
        response = self.client.get(reverse('gcf:players_list'))

        self.assertEqual(response.status_code, 200)

    def test_player_detail_view(self):
        test_player = Player(name='Test Player', age=123, description='Test Description')
        test_player.save()

        # response = self.client.get(f'/players/{test_player.pk}/')
        response = self.client.get(reverse('gcf:player_detail', kwargs={'pk': test_player.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_player.name)


class ModelsCreateTest(TestCase):
    
    def test_update_player(self):
        test_player = Player(name='Test Player', age=123, description='Test Description')
        test_player.save()

        self.assertIsNotNone(test_player.created_at)
        self.assertIsNotNone(test_player.updated_at)

        update_date = test_player.updated_at

        test_player.name = 'Test Player Updated'
        test_player.save()

        self.assertNotEqual(test_player.updated_at, update_date)

    def test_update_user(self):
        test_user = User(username='Test User', email='test@test.ru')
        test_user.save()

        self.test_user(test_user.created_at)
        self.test_user(test_user.updated_at)

        update_date = test_user.updated_at

        test_user.name = 'Test Player Updated'
        test_user.save()

        self.assertNotEqual(test_user.updated_at, update_date)