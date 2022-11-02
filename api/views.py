from django.http import JsonResponse, Http404
from .request import *

def api_request_search(request):
    pokemons = pokesearch.copy()

    if str(request.method) == "POST":
        post = request.POST.get("search", "").lower()
        if post:
            pokemons = list(filter(lambda x: post.lower() in x['name'].lower(), pokemons))
        return JsonResponse(pokemons, safe=False)

    raise Http404


def api_request_found(request):
    if str(request.method) == "POST":
        post = request.POST.get("search", "")
        for pokemon in pokelist:
            input(pokemon['relative_name'])
       
            if pokemon["name"].lower() == post.lower():
                return JsonResponse(pokemon, safe=False)

    raise Http404

