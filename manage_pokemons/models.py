from django.db import models
from django.core.validators import MinValueValidator


class Pokemon(models.Model):
    name = models.CharField(max_length=60)
    type1 = models.CharField(max_length=30)
    type2 = models.CharField(max_length=30)
    # Currently, there are
    generation = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    legendary = models.BooleanField()
    stats = models.ForeignKey('Stats', on_delete=models.CASCADE)



class Stats(models.Model):
    total = models.PositiveSmallIntegerField()
    hp = models.PositiveSmallIntegerField()
    attack = models.PositiveSmallIntegerField()
    defense = models.PositiveSmallIntegerField()
    special_attack = models.PositiveSmallIntegerField()
    special_defense = models.PositiveSmallIntegerField()
    speed = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "Stats"