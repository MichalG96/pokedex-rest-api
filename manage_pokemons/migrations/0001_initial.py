# Generated by Django 3.2.3 on 2021-05-28 12:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveSmallIntegerField()),
                ('hp', models.PositiveSmallIntegerField()),
                ('attack', models.PositiveSmallIntegerField()),
                ('defense', models.PositiveSmallIntegerField()),
                ('special_attack', models.PositiveSmallIntegerField()),
                ('special_defense', models.PositiveSmallIntegerField()),
                ('speed', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('type1', models.CharField(max_length=30)),
                ('type2', models.CharField(max_length=30)),
                ('generation', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('legendary', models.BooleanField()),
                ('stats', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manage_pokemons.stats')),
            ],
        ),
    ]