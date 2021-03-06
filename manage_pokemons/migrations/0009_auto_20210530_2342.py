# Generated by Django 3.2.3 on 2021-05-30 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_pokemons', '0008_remove_pokemon_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='type1',
            field=models.CharField(choices=[('bug', 'Bug'), ('dark', 'Dark'), ('Dragon', 'dragon'), ('electric', 'Electric'), ('fairy', 'Fairy'), ('fighting', 'Fighting'), ('fire', 'Fire'), ('flying', 'Flying'), ('ghost', 'Ghost'), ('grass', 'Grass'), ('ground', 'Ground'), ('ice', 'Ice'), ('normal', 'Normal'), ('poison', 'Poison'), ('psychic', 'Psychic'), ('rock', 'Rock'), ('steel', 'Steel'), ('water', 'Water')], max_length=30),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='type2',
            field=models.CharField(blank=True, choices=[('bug', 'Bug'), ('dark', 'Dark'), ('Dragon', 'dragon'), ('electric', 'Electric'), ('fairy', 'Fairy'), ('fighting', 'Fighting'), ('fire', 'Fire'), ('flying', 'Flying'), ('ghost', 'Ghost'), ('grass', 'Grass'), ('ground', 'Ground'), ('ice', 'Ice'), ('normal', 'Normal'), ('poison', 'Poison'), ('psychic', 'Psychic'), ('rock', 'Rock'), ('steel', 'Steel'), ('water', 'Water'), ('no type', '')], max_length=30, null=True),
        ),
    ]
