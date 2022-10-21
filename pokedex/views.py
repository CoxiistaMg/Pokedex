from django.shortcuts import render
from django.http import Http404, JsonResponse
from api.request import pokelist, formslist, moveslist, dict_tms
from .data_processing import *
import json

with open("pokemons.json", "r") as outfile:
    request = outfile.read()
    lista_pokemon = json.loads(request)
    for _id, pokemon in enumerate(lista_pokemon):
        lista_pokemon[_id] = pokemon["name"]

def pokedexview(request):
    search = ''
    if (request.method == 'POST'):
        if (request.POST.get('search')):
            search = request.POST.get('search')

    return render(request, "index.html", {'search': search})

def pokemondetail(request, p):
    effect = {
        'super effective': {},
        'ineffective': {},
        'immune': {}
    }

    if p.lower() in lista_pokemon:
        i = lista_pokemon.index(p.lower())
        copy = pokelist[i].copy()
        copy['weight'] = pokelist[i]['weight'] / 10
        copy['height'] = pokelist[i]['height'] / 10
        copy['url_image'] = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{copy["id"]}.png'
        copy['url_pokemon'] = f'https://pokeapi.co/api/v2/pokemon/{copy["id"]}/'
        later = i + 1

        if later == len(pokelist):
            later = 0
        
        if request.method == "POST":
            change = request.POST['variables']
        
            if change.title() != copy['name'].title():
                for each in formslist:
                    if each['name'] == change:
                        change = each
                        break 
                
                copy['moves'] = change['moves']
                copy['name'] = change['name']
                copy['relative_name'] = copy['varieties'][change['name']]
                copy["stats"] = change['stats'] 
                copy["abilities"] = change["abilities"]
                copy['types'] = change["types"]
                copy['height'] = change['height'] / 10
                copy['url_image'] = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{change["id"]}.png'
                copy['url_pokemon'] = f'https://pokeapi.co/api/v2/pokemon/{change["id"]}/'
        
        key_value = {
            'super effective': 2,
            'ineffective': 0.5,
            'immune': 0
        }
        types = [type_['type']['name'] for type_ in copy['types']]
        types_value = {}

        for each in types:
            for info in change_effect[each]:
                num = key_value[info]
                for typ in change_effect[each][info]:
                    if typ not in types_value:
                        types_value[typ] = num

                    else:
                        types_value[typ] *= num
        
        key_value = {
            'super effective': {},
            'ineffective': {},
            'immune': {}
        }

        for each in types_value:
            if types_value[each] == 0:
                key_value['immune'][each] = types_value[each]
            
            if types_value[each] > 1:
                key_value['super effective'][each] = types_value[each]
            
            if 1 > types_value[each] > 0:
                 key_value['ineffective'][each] = int(1 / types_value[each])

        return render(request,'detail.html', {
            'pokemon': copy,
            'before': pokelist[i-1],
            'later': pokelist[later],
            'moves': moveslist,
            'super_effective': key_value['super effective'],
            'ineffective': key_value['ineffective'],
            'immune': key_value['immune'],
            'tms': dict_tms
        })

    raise Http404

def movesdetail(request, name):
    for each in moveslist:
        if each[0] == name:
            return render(request, 'move_detail.html', {
                'move': each
            } )

    raise Http404