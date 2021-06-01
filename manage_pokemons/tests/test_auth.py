from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from manage_pokemons.models import Pokemon

BASE_URL = 'http://127.0.0.1:8000/'


class TestRestrictedViews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='admin', password='secret')
        cls.user2 = User.objects.create_user(username='testuser', password='secret')
        cls.pokemon1 = Pokemon.objects.create(name="test1", type1="Fire",
                                              creator=cls.user1, legendary=True,
                                              hp=15, attack=10)
        cls.pokemon2 = Pokemon.objects.create(name="test2", type1="Fire",
                                              creator=cls.user2, legendary=True,
                                              hp=15, attack=10)

        cls.default_payload = {
            "name": "TestPokemon",
            "type1": "Fire",
            "generation": 1,
            "legendary": True,
            "hp": 150,
            "attack": 10,
            "special_defense": 30,
            "speed": 40
        }

    def test_creating_a_pokemon_by_non_authorized_user(self):
        response = self.client.post(f'{BASE_URL}api/pokemon/', data=self.default_payload)
        self.assertEqual(response.status_code, 403)

    def test_creating_a_pokemon_by_authorized_user(self):
        self.client.login(username='admin', password='secret')
        response = self.client.post(f'{BASE_URL}api/pokemon/', data=self.default_payload)
        self.assertEqual(response.status_code, 201)

    def test_deleting_a_pokemon_by_creator(self):
        self.client.login(username='admin', password='secret')
        response = self.client.delete(f'{BASE_URL}api/pokemon/1/')
        self.assertEqual(response.status_code, 204)

    def test_deleting_a_pokemon_by_non_creator(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.delete(f'{BASE_URL}api/pokemon/')
        self.assertEqual(response.status_code, 405)

    def test_updating_a_pokemon_by_creator(self):
        self.client.login(username='admin', password='secret')
        payload = {'name': 'newname'}
        response = self.client.patch(f'{BASE_URL}api/pokemon/1/', data=payload)
        self.assertEqual(response.status_code, 200)

    def test_updating_a_pokemon_by_non_creator(self):
        self.client.login(username='testuser', password='secret')
        payload = {'name': 'newname'}
        response = self.client.patch(f'{BASE_URL}api/pokemon/', data=payload)
        self.assertEqual(response.status_code, 405)
