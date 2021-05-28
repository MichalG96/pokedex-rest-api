from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import F


class Pokemon(models.Model):
    name = models.CharField(max_length=60)
    type1 = models.CharField(max_length=30)
    type2 = models.CharField(max_length=30, null=True, blank=True)
    generation = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)],
                                                  default=1)
    legendary = models.BooleanField()
    hp = models.PositiveSmallIntegerField(default=50)
    attack = models.PositiveSmallIntegerField(default=50)
    defense = models.PositiveSmallIntegerField(default=50)
    special_attack = models.PositiveSmallIntegerField(default=50)
    special_defense = models.PositiveSmallIntegerField(default=50)
    speed = models.PositiveSmallIntegerField(default=50)
    total = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        stats_sum = (self.hp + self.attack + self.defense + self.special_attack
        + self.special_defense + self.speed)
        self.total = stats_sum
        super(Pokemon, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
