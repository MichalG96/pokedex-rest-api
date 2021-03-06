from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Pokemon(models.Model):
    TYPE_CHOICES = [
        ('Bug', 'Bug'),
        ('Dark', 'Dark'),
        ('Dragon', 'Dragon'),
        ('Electric', 'Electric'),
        ('Fairy', 'Fairy'),
        ('Fighting', 'Fighting'),
        ('Fire', 'Fire'),
        ('Flying', 'Flying'),
        ('Ghost', 'Ghost'),
        ('Grass', 'Grass'),
        ('Ground', 'Ground'),
        ('Ice', 'Ice'),
        ('Normal', 'Normal'),
        ('Poison', 'Poison'),
        ('Psychic', 'Psychic'),
        ('Rock', 'Rock'),
        ('Steel', 'Steel'),
        ('Water', 'Water'),
        ('', 'no type')
    ]
    creator = models.ForeignKey(User, related_name='pokemons',
                                default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    type1 = models.CharField(max_length=30, choices=TYPE_CHOICES[:-1])
    type2 = models.CharField(max_length=30, choices=TYPE_CHOICES, null=True, blank=True)
    generation = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)],
                                                  default=1)
    legendary = models.BooleanField()
    hp = models.PositiveSmallIntegerField(default=50)
    attack = models.PositiveSmallIntegerField(default=50)
    defense = models.PositiveSmallIntegerField(default=50)
    special_attack = models.PositiveSmallIntegerField(default=50)
    special_defense = models.PositiveSmallIntegerField(default=50)
    speed = models.PositiveSmallIntegerField(default=50)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
