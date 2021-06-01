from django.contrib.auth.models import User

from rest_framework import viewsets, permissions

from .models import Pokemon
from .serializers import PokemonSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


class PokemonViewSet(viewsets.ModelViewSet):
    serializer_class = PokemonSerializer
    queryset = Pokemon.objects.all()
    filterset_fields = ['type1', 'type2', 'name']
    search_fields = ['type1', 'type2', 'name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
