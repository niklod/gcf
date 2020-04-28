from django.test import TestCase
from django.urls import reverse
from .models import Player, User, Game, PlayerConfig


class ViewsTest(TestCase):

    def test_games_detail_view(self):
        test_game = Game(name='Test game')
        test_game.save()

        response = self.client.get(reverse('gcf:game_detail', kwargs={
            'game_slug': test_game.slug
        }))

        self.assertEqual(response.status_code, 200)

    def test_player_detail_view_without_config(self):
        test_game = Game(name='Test game')
        test_game.save()
        test_player = Player(name='Test Player', nickname='testplayer', age=123, description='Test Description')
        test_player.save()
        test_player.games.add(test_game)

        response = self.client.get(reverse('gcf:player_detail', kwargs={
            'player_slug': test_player.slug,
            'game_slug': test_game.slug}))

        self.assertEqual(response.status_code, 404)

    def test_player_detail_view_with_config(self):
        test_game = Game(name='Test game')
        test_game.save()
        test_player = Player(name='Test Player', nickname='testplayer', age=123, description='Test Description')
        test_player.save()
        test_player.games.add(test_game)
        test_config = PlayerConfig(game=test_game, player=test_player)
        test_config.save()

        response = self.client.get(reverse('gcf:player_detail', kwargs={
            'player_slug': test_player.slug,
            'game_slug': test_game.slug}))

        self.assertEqual(response.status_code, 200)

    def test_player_detail_view_with_twi_configs(self):
        test_game_1 = Game(name='Test game1')
        test_game_1.save()
        test_game_2 = Game(name='Test game2')
        test_game_2.save()

        test_player = Player(name='Test Player', nickname='testplayer', age=123, description='Test Description')
        test_player.save()
        test_player.games.add(test_game_1)
        test_player.games.add(test_game_2)

        test_config_1 = PlayerConfig(game=test_game_1, player=test_player)
        test_config_1.save()
        test_config_2 = PlayerConfig(game=test_game_2, player=test_player)
        test_config_2.save()

        response = self.client.get(reverse('gcf:player_detail', kwargs={
            'player_slug': test_player.slug,
            'game_slug': test_game_1.slug}))

        self.assertEqual(response.context['config'], test_config_1)

        response = self.client.get(reverse('gcf:player_detail', kwargs={
            'player_slug': test_player.slug,
            'game_slug': test_game_2.slug}))

        self.assertEqual(response.context['config'], test_config_2)

        response = self.client.get(reverse('gcf:player_detail', kwargs={
            'player_slug': test_player.slug,
            'game_slug': test_game_2.slug}))

        self.assertNotEqual(response.context['config'], test_config_1)


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

        self.assertIsNotNone(test_user.created_at)
        self.assertIsNotNone(test_user.updated_at)

        update_date = test_user.updated_at

        test_user.name = 'Test Player Updated'
        test_user.save()

        self.assertNotEqual(test_user.updated_at, update_date)

    def test_generate_same_player_slug(self):
        test_player1 = Player(name='Test Player 1', nickname='TestPlayer')
        test_player1.save()

        self.assertIsNotNone(test_player1.slug)

        test_player2 = Player(name='Test Player 2', nickname='Testplayer')
        test_player2.save()

        self.assertNotEqual(test_player1.slug, test_player2.slug)

    def test_generate_cyrillic_slug(self):
        test_player = Player(name='Test Player', nickname='Тестовый игрок')
        test_player.save()

        self.assertIsNotNone(test_player.slug)
        self.assertNotEqual(test_player.slug, 'Тестовый игрок')
        self.assertNotEqual(test_player.slug, 'тестовый-игрок')

    def test_generate_game_slug(self):
        test_game = Game(name='Test Game')
        test_game.save()

        self.assertIsNotNone(test_game.slug)
        self.assertNotEqual(test_game.slug, 'Test Game')
        self.assertEqual(test_game.slug, 'test-game')
