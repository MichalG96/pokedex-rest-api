import pandas as pd
import json

pokemon_df = pd.read_csv('pokemon.csv')
pokemon_df = pokemon_df.where(pd.notnull(pokemon_df), None)

fixtures = []
for i, row in pokemon_df.iterrows():
    fixtures.append({'model': 'manage_pokemons.Pokemon',
                               'pk':i+1,
                               'fields':{
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
                                   'total': row['Total'],
                               }})

with open('pokemon_fixtures.json', 'w') as outfile:
    json.dump(fixtures, outfile)

# You can later install fixtures by running
# py manage.py loaddata pokemon_fixtures.json