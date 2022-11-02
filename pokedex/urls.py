from django.urls import path
from .views import pokedexview, pokemondetail, movesdetail

urlpatterns = [
    path("", pokedexview, name="pokedex"),
    path("pokemon/<str:p>", pokemondetail, name='pokemon'),
    path("moves/<str:name>", movesdetail, name='pokemon'),

]