from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Pokemon
        fields = '__all__'

    def get_total(self, obj):
        return (obj.hp + obj.attack + obj.defense + obj.special_attack
                + obj.special_defense + obj.speed)


class UserSerializer(serializers.ModelSerializer):
    pokemons = serializers.PrimaryKeyRelatedField(many=True,
                                                  queryset=Pokemon.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'pokemons']
