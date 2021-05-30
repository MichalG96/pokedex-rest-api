from rest_framework import serializers

from .models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = Pokemon
        # exclude = ['total']
        fields = '__all__'

    def get_total(self, obj):
        return (obj.hp + obj.attack + obj.defense + obj.special_attack
                + obj.special_defense + obj.speed)
