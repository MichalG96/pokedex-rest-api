import pandas as pd
import json

pokemon_df = pd.read_csv('pokemon.csv')
pokemon_df = pokemon_df.where(pd.notnull(pokemon_df), None)

full_fixtures = []
test_fixtures = []
test_fixtures_pagination = []

for i, row in pokemon_df.iterrows():
    if i % 20 == 0:
        test_fixtures.append({'model': 'manage_pokemons.Pokemon',
                              'pk': i // 20 + 1,
                              'fields': {
                                  'name': row['Name'],
                                  'type1': row['Type 1'],
                                  'type2': row['Type 2'],
                                  'generation': row['Generation'],
                                  'legendary': row['Legendary'],
                                  'hp': row['HP'],
                                  'attack': row['Attack'],
                                  'defense': row['Defense'],
                                  'special_attack': row['Sp. Atk'],
                                  'special_defense': row['Sp. Def'],
                                  'speed': row['Speed'],
                              }})
    if i % 10 == 0:
        test_fixtures_pagination.append({'model': 'manage_pokemons.Pokemon',
                                         'pk': i // 10 + 1,
                                         'fields': {
                                             'name': row['Name'],
                                             'type1': row['Type 1'],
                                             'type2': row['Type 2'],
                                             'generation': row['Generation'],
                                             'legendary': row['Legendary'],
                                             'hp': row['HP'],
                                             'attack': row['Attack'],
                                             'defense': row['Defense'],
                                             'special_attack': row['Sp. Atk'],
                                             'special_defense': row['Sp. Def'],
                                             'speed': row['Speed'],
                                         }})
    full_fixtures.append({'model': 'manage_pokemons.Pokemon',
                          'pk': i + 1,
                          'fields': {
                              'name': row['Name'],
                              'type1': row['Type 1'],
                              'type2': row['Type 2'],
                              'generation': row['Generation'],
                              'legendary': row['Legendary'],
                              'hp': row['HP'],
                              'attack': row['Attack'],
                              'defense': row['Defense'],
                              'special_attack': row['Sp. Atk'],
                              'special_defense': row['Sp. Def'],
                              'speed': row['Speed'],
                          }})

test_users = [
    {"model": "auth.user",
     "pk": 1,
     "fields": {
         "username": "admin",
         "password": "admin"
     }},
    {"model": "auth.user",
     "pk": 2,
     "fields": {
         "username": "testuser",
         "password": "test123"
     }}
]

test_fixtures += test_users
test_fixtures_pagination += test_users

with open('fixtures.json', 'w') as outfile:
    json.dump(full_fixtures, outfile)

with open('test_fixtures.json', 'w') as outfile:
    json.dump(test_fixtures, outfile)

with open('test_fixtures_pagination.json', 'w') as outfile:
    json.dump(test_fixtures_pagination, outfile)

# You can later install fixtures by running
# py manage.py loaddata fixtures.json
