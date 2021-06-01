from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APITestCase

# You could argue that some of the tests seem redundant, because they check the built-in
# functions of Django, and DRF, but i decided to write them anyway, as a sanity check

BASE_URL = 'http://127.0.0.1:8000/'


class TestListPokemons(APITestCase):
    fixtures = ['test_fixtures.json']

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'{BASE_URL}api/pokemon/')
        self.assertEqual(response.status_code, 200)

    def test_all_pokemons_are_returned(self):
        response = self.client.get(f'{BASE_URL}api/pokemon/')
        # There are 40 Pokemons in test fixture
        self.assertEqual(len(response.json().get('results')), 40)


class TestRetrievePokemon(APITestCase):
    fixtures = ['test_fixtures.json']

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'{BASE_URL}api/pokemon/40/')
        self.assertEqual(response.status_code, 200)

    def test_correct_pokemon_returned(self):
        response = self.client.get(f'{BASE_URL}api/pokemon/1/')
        self.assertEqual(response.json().get('name'), 'Bulbasaur')


class TestDeletePokemon(APITestCase):
    fixtures = ['test_fixtures.json']

    def setUp(self):
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

    def test_correct_status_code(self):
        response = self.client.delete(f'{BASE_URL}api/pokemon/40/')
        self.assertEqual(response.status_code, 204)

    def test_pokemons_number_smaller_after_deletion(self):
        response = self.client.get(f'{BASE_URL}api/pokemon/')
        number_before_deletion = len(response.json().get('results'))
        self.client.delete(f'{BASE_URL}api/pokemon/30/')
        response = self.client.get(f'{BASE_URL}api/pokemon/')
        number_after_deletion = len(response.json().get('results'))
        self.assertEqual(number_before_deletion - number_after_deletion, 1)


class TestCreatePokemon(APITestCase):
    fixtures = ['test_fixtures.json']
    default_payload = {
        "name": "TestPokemon",
        "type1": "Fire",
        "generation": 1,
        "legendary": True,
        "hp": 150,
        "attack": 10,
        "special_defense": 30,
        "speed": 40
    }
    user = User.objects.get(username='admin')

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_correct_status_code(self):
        response = self.client.post(f'{BASE_URL}api/pokemon/', data=self.default_payload)
        self.assertEqual(response.status_code, 201)

    def test_pokemons_number_bigger_after_creation(self):
        response = self.client.get(f'{BASE_URL}api/pokemon/')
        number_before_creation = len(response.json()['results'])
        self.client.post(f'{BASE_URL}api/pokemon/', data=self.default_payload)
        response = self.client.get(f'{BASE_URL}api/pokemon/')
        number_after_creation = len(response.json()['results'])
        self.assertEqual(number_after_creation - number_before_creation, 1)

    def test_creator_is_set_correctly(self):
        response = self.client.post(f'{BASE_URL}api/pokemon/', data=self.default_payload)
        response_creator = response.json().get('creator')
        self.assertEqual(self.user.username, response_creator)

    def test_default_values_are_set_correctly(self):
        response = self.client.post(f'{BASE_URL}api/pokemon/', data=self.default_payload)
        self.assertEqual(response.json().get('defense'), 50)
        self.assertEqual(response.json().get('special_attack'), 50)

    def test_total_is_calculated_correctly(self):
        response = self.client.post(f'{BASE_URL}api/pokemon/', data=self.default_payload)
        # 150 + 10 + 50 + 50 + 30 + 40
        self.assertEqual(response.json().get('total'), 330)

    def test_required_parameter_missing(self):
        payload = {
            "type1": "Fire",
            "legendary": True,
        }
        response = self.client.post(f'{BASE_URL}api/pokemon/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('name' in response_json)
        self.assertEqual(response_json.get('name')[0], "This field is required.")

        payload = {
            "name": "TestPokemon",
            "legendary": True,
        }
        response = self.client.post(f'{BASE_URL}api/pokemon/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('type1' in response_json)
        self.assertEqual(response_json.get('type1')[0], "This field is required.")

    def test_wrong_type(self):
        # Wrong type1
        payload = {
            "type1": "test",
            "legendary": True,
        }
        response = self.client.post(f'{BASE_URL}api/pokemon/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('type1' in response_json)
        self.assertEqual(response_json.get('type1')[0], '"test" is not a valid choice.')

        # Wrong type2
        payload = {
            "type1": "Water",
            "type2": "test",
            "legendary": True,
        }
        response = self.client.post(f'{BASE_URL}api/pokemon/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('type2' in response_json)
        self.assertEqual(response_json.get('type2')[0], '"test" is not a valid choice.')

        # Wrong type1 and type2
        payload = {
            "type1": "test",
            "type2": "test",
            "legendary": True,
        }
        response = self.client.post(f'{BASE_URL}api/pokemon/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('type1' in response_json)
        self.assertTrue('type2' in response_json)
        self.assertEqual(response_json.get('type1')[0], '"test" is not a valid choice.')
        self.assertEqual(response_json.get('type2')[0], '"test" is not a valid choice.')


class TestUpdatePokemon(APITestCase):
    fixtures = ['test_fixtures.json']
    default_payload = {
        "name": "TestPokemon",
        "type1": "Fire",
        "generation": 1,
        "legendary": True,
        "hp": 150,
        "attack": 10,
        "special_defense": 30,
        "speed": 40
    }
    user = User.objects.get(username='admin')

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_correct_status_code(self):
        response = self.client.put(f'{BASE_URL}api/pokemon/5/', data=self.default_payload)
        self.assertEqual(response.status_code, 200)

    def test_pokemon_was_updated(self):
        response = self.client.put(f'{BASE_URL}api/pokemon/5/', data=self.default_payload)
        response_json = response.json()
        self.assertEqual(response_json.get('name'), 'TestPokemon')
        self.assertEqual(response_json.get('type1'), 'Fire')
        self.assertEqual(response_json.get('generation'), 1)
        self.assertEqual(response_json.get('legendary'), True)
        self.assertEqual(response_json.get('hp'), 150)
        self.assertEqual(response_json.get('attack'), 10)
        self.assertEqual(response_json.get('special_defense'), 30)
        self.assertEqual(response_json.get('speed'), 40)

    def test_total_is_calculated_correctly(self):
        response = self.client.get(f'{BASE_URL}api/pokemon/1/')
        response_json = response.json()
        total_before_update = response_json.get('total')
        payload = {
            "name": "TestPokemon",
            "type1": "Fire",
            "legendary": True,
            "hp": response_json.get('hp') - 20,
        }
        response = self.client.put(f'{BASE_URL}api/pokemon/1/', data=payload)
        self.assertEqual(response.json().get('total'), total_before_update - 20)

    def test_required_parameter_missing(self):
        payload = {
            "type1": "Fire",
            "legendary": True,
        }
        response = self.client.put(f'{BASE_URL}api/pokemon/5/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('name' in response_json)
        self.assertEqual(response_json.get('name')[0], "This field is required.")

        payload = {
            "name": "TestPokemon",
            "legendary": True,
        }
        response = self.client.put(f'{BASE_URL}api/pokemon/6/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('type1' in response_json)
        self.assertEqual(response_json.get('type1')[0], "This field is required.")

    def test_wrong_type(self):
        # Wrong type1
        payload = {
            "type1": "test",
            "legendary": True,
        }
        response = self.client.put(f'{BASE_URL}api/pokemon/4/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('type1' in response_json)
        self.assertEqual(response_json.get('type1')[0], '"test" is not a valid choice.')

        # Wrong type2
        payload = {
            "type1": "Water",
            "type2": "test",
            "legendary": True,
        }
        response = self.client.put(f'{BASE_URL}api/pokemon/5/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('type2' in response_json)
        self.assertEqual(response_json.get('type2')[0], '"test" is not a valid choice.')

        # Wrong type1 and type2
        payload = {
            "type1": "test",
            "type2": "test",
            "legendary": True,
        }
        response = self.client.put(f'{BASE_URL}api/pokemon/6/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('type1' in response_json)
        self.assertTrue('type2' in response_json)
        self.assertEqual(response_json.get('type1')[0], '"test" is not a valid choice.')
        self.assertEqual(response_json.get('type2')[0], '"test" is not a valid choice.')


class TestPartiallyUpdatePokemon(APITestCase):
    fixtures = ['test_fixtures.json']
    user = User.objects.get(username='admin')

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_correct_status_code(self):
        payload = {
            "name": "TestPokemon"
        }
        response = self.client.patch(f'{BASE_URL}api/pokemon/5/', data=payload)
        self.assertEqual(response.status_code, 200)

    def test_total_is_calculated_correctly(self):
        response = self.client.get(f'{BASE_URL}api/pokemon/1/')
        response_json = response.json()
        total_before_update = response_json.get('total')
        payload = {
            "speed": response_json.get('speed') - 20,
        }
        response = self.client.patch(f'{BASE_URL}api/pokemon/1/', data=payload)
        self.assertEqual(response.json().get('total'), total_before_update - 20)

    def test_update_multiple_parameters(self):
        payload = {
            "type1": "Fire",
            "legendary": False,
            "special_defense": 42,
        }
        response = self.client.patch(f'{BASE_URL}api/pokemon/5/', data=payload)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue('name' in response_json)
        self.assertEqual(response_json.get('type1'), "Fire")
        self.assertEqual(response_json.get('legendary'), False)
        self.assertEqual(response_json.get('special_defense'), 42)

    def test_wrong_type(self):
        # Wrong type1
        payload = {
            "type1": "test",
            "legendary": True,
        }
        response = self.client.patch(f'{BASE_URL}api/pokemon/4/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('type1' in response_json)
        self.assertEqual(response_json.get('type1')[0], '"test" is not a valid choice.')

        # Wrong type2
        payload = {
            "type1": "Water",
            "type2": "test",
            "legendary": True,
        }
        response = self.client.patch(f'{BASE_URL}api/pokemon/5/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('type2' in response_json)
        self.assertEqual(response_json.get('type2')[0], '"test" is not a valid choice.')

        # Wrong type1 and type2
        payload = {
            "type1": "test",
            "type2": "test",
            "legendary": True,
        }
        response = self.client.patch(f'{BASE_URL}api/pokemon/6/', data=payload)
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue('type1' in response_json)
        self.assertTrue('type2' in response_json)
        self.assertEqual(response_json.get('type1')[0], '"test" is not a valid choice.')
        self.assertEqual(response_json.get('type2')[0], '"test" is not a valid choice.')


class TestFiltering(APITestCase):
    fixtures = ['test_fixtures.json']
    user = User.objects.get(username='admin')

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_filtering_by_type1(self):
        query_params = {'type1': 'Water'}
        response = self.client.get(f'{BASE_URL}api/pokemon/', data=query_params)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json.get('count'), 6)
        self.assertEqual(len(response_json.get('results')), 6)

        received_names = [i['name'] for i in response_json['results']]
        self.assertEqual(received_names,
                         ['Golduck', 'Gyarados', 'Corsola',
                          'Mudkip', 'Empoleon', 'Oshawott'])

    def test_filtering_by_type2(self):
        query_params = {'type2': 'Flying'}
        response = self.client.get(f'{BASE_URL}api/pokemon/', data=query_params)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json.get('count'), 6)
        self.assertEqual(len(response_json.get('results')), 6)

        received_names = [i['name'] for i in response_json['results']]
        self.assertEqual(received_names,
                         ['Pidgey', 'Gyarados', 'Ledian',
                          'Swellow', 'Yanmega', 'Unfezant'])

    def test_filtering_by_type1_and_type2(self):
        query_params = {'type1': 'Bug', 'type2': 'Steel'}
        response = self.client.get(f'{BASE_URL}api/pokemon/', data=query_params)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json.get('count'), 2)
        self.assertEqual(len(response_json.get('results')), 2)

        received_names = [i['name'] for i in response_json['results']]
        self.assertEqual(received_names, ['Forretress', 'WormadamTrash Cloak'])

    def test_filtering_by_name(self):
        query_params = {'name': 'Bulbasaur'}
        response = self.client.get(f'{BASE_URL}api/pokemon/', data=query_params)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json.get('count'), 1)
        self.assertEqual(len(response_json.get('results')), 1)
        self.assertEqual(response_json.get('results')[0]['name'], 'Bulbasaur')


class TestSearching(APITestCase):
    fixtures = ['test_fixtures.json']

    def test_searching(self):
        query_params = {'search': 'dr'}
        response = self.client.get(f'{BASE_URL}api/pokemon/', data=query_params)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json.get('count'), 4)
        received_names = [i['name'] for i in response_json['results']]
        self.assertTrue('Dragonair' in received_names)


class TestPagination(APITestCase):
    fixtures = ['test_fixtures_pagination.json']

    def test_pagination_is_50(self):
        query_params = {'page': 1}
        response = self.client.get(f'{BASE_URL}api/pokemon/', data=query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('results')), 50)

    def test_last_page(self):
        query_params = {'page': 2}
        response = self.client.get(f'{BASE_URL}api/pokemon/', data=query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('results')), 30)


