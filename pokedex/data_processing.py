from distutils.command.build import build
from api.request import pokelist

change_effect = {
    'fire': {
        'super effective': ['water', 'ground', 'rock'],
        'ineffective': ['grass', 'bug',  'fairy', 'ice', 'steel', 'fire'],
        'immune': []
    },

    'normal': {
        'super effective': ['fighting'],
        'ineffective': [],
        'immune': ['ghost']
    },
    'steel': {
        'super effective': ['fire', 'fighting', 'ground'],
        'ineffective': ['normal', 'grass', 'ice', 'flying', 'psychic', 'bug', 'rock', 'dragon', 'steel', 'fairy'],
        'immune': ['poison']
    },
    'rock': {
        'super effective': ['grass', 'water', 'ground', 'fighting', 'steel'],
        'ineffective': ['normal', 'fire', 'poison', 'flying'],
        'immune': []
    },
    'ground': {
        'super effective': ['water', 'grass', 'ice'],
        'ineffective': ['poison', 'rock'],
        'immune': ['electric']
    },
    'flying': {
        'super effective': ['electric', 'ice', 'rock'],
        'ineffective': ['grass', 'fighting', 'bug'],
        'immune': ['ground']
    },
    'fighting': {
        'super effective': ['flying', 'psychic', 'fairy'],
        'ineffective': ['bug', 'rock', 'dark'],
        'immune': []
    },
    'fairy': {
        'super effective': ['steel', 'poison'],
        'ineffective': ['fighting', 'bug', 'dark'],
        'immune': ['dragon']
    },
   'water': {
        'super effective': ['grass', 'electric'],
        'ineffective': ['water', 'fire', 'ice', 'steel'],
        'immune': []
    },
    'grass': {
        'super effective': ['flying', 'fire', 'bug', 'poison', 'ice'],
        'ineffective': ['water', 'electric', 'grass', 'ground'],
        'immune': []
    },
    'electric': {
        'super effective': ['ground'],
        'ineffective': ['electric', 'flying', 'steel'],
        'immune': []
    },
    'ice': {
        'super effective': ['fire', 'fighting', 'rock', 'steel'],
        'ineffective': ['ice'],
        'immune': []
    },
    'poison': {
        'super effective': ['psychic', 'ground'],
        'ineffective': ['fighting', 'poison', 'grass', 'bug'],
        'immune': []
    },
    'psychic': {
        'super effective': ['dark', 'ghost', 'bug'],
        'ineffective': ['fighting', 'psychic'],
        'immune': []
    },
    'bug': {
        'super effective': ['fire', 'flying', 'rock'],
        'ineffective': ['grass', 'fighting', 'ground'],
        'immune': []
    },
    'ghost': {
        'super effective': ['ghost', 'dark'],
        'ineffective': ['poison', 'bug'],
        'immune': ['normal', 'fighting']
    },
    'dragon': {
        'super effective': ['ice', 'fairy', 'dragon'],
        'ineffective': ['fire', 'water', 'grass', 'electric'],
        'immune': []
    },
    'dark': {
        'super effective': ['fighting', 'bug', 'fairy'],
        'ineffective': ['ghost', 'dark'],
        'immune': ['psychic']
    },
}


trade_strings = {
    'held_item': 'Hold ...',
    'item': 'Use ...',
    'known_move': 'after ... learned',
    'known_move_type': 'after ... type learned',
    'min_affection': '',
    'min_happiness': 'high Friendship',
    'location': 'level up near a ...',
    'min_level': 'Level ...',
    'party_species': '>',
    'party_type': '>',
    'trade_species': 'Trade',
    'min_beauty': '>>>>',
    'turn_upside_down': 'turn upside'
}

trade_maps = {
'gender' : {
    1: 'female',
    2: 'male'
},

'relative_physical_stats': {
    1: 'Attack > Defense',
    0: 'Attack = Defense',
    -1: 'Attack < Defense'
},
'needs_overworld_rain': {
    True: 'during rain'
},
'time_of_day': {
    'day': 'Daytime',
    'night': 'Nighttime'
},
'trigger': {
    'level-up': '',
    'trade': 'Trade',
    'use-item': '',
    'shed': 'empty spot in party, Pokéball in bag',
    'spin': 'spin around holding Sweet',
    'tower-of-darkness': '',
    "tower-of-waters": '',
    "three-critical-hits": 'achieve 3 critical hits in one battle',
    'runerigus': 'near Dusty Bowl',
    'take-damage': 'take damage'

}
}

def return_chain_evolution(pokemon):
    def return_evolution_method_to_string(method):
        elements = []
        for name in method:
            if name in trade_maps:
                elements.append(trade_maps[name][method[name]])

            else:
                elements.append(trade_strings[name].replace('...', str(method[name]).replace('-', ' ')))

        elements = list(filter(lambda x: x != '', elements))
        return ', '.join(elements)
    if pokemon:
        chain = pokemon['evolution_to']
        invalid_values = [False, None, '']
        evolution_chain = {}
        base = pokelist[int(pokemon['evolution_base']) - 1]
        final_evolution_chain = [{'base': [{'name': base['name'], 'types': base['types'], 'id': base['id'], 'id_url': int(base['id']), 'relative_name': base['relative_name']}]}]

        for pos, evolution in enumerate(chain):
            methods_valids = {}
            evolution_chain[pos] = []
            if evolution['evolution_details']:
                poke_details = evolution['evolution_details'][0].copy()
                evolution_name = evolution['species']['name']

                evolution_id = evolution['species']['url'].split('/')[-2]
                evolution_to = evolution['evolves_to']
                for topics in poke_details:
                    if poke_details[topics] not in invalid_values:
                        methods_valids[topics] = poke_details[topics]

                        if type(methods_valids[topics]) == dict and 'name' in methods_valids[topics]:
                            methods_valids[topics] = methods_valids[topics]['name']

                evolution_chain[pos].append({'name': evolution_name,'method': return_evolution_method_to_string(methods_valids), 'types': pokelist[int(evolution_id) - 1]['types'], 'id': pokelist[int(evolution_id) - 1]['id'], 'id_url': int(pokelist[int(evolution_id) - 1]['id']), 'relative_name': pokelist[int(evolution_id) - 1]['relative_name']})
                if evolution_to:
                    evolution_to = evolution['evolves_to']
                    evolution_chain[pos].append([])
    
                    for evolution in evolution_to:
                        methods_valids = {}
                        poke_details = evolution['evolution_details'][0].copy()
                        evolution_name = evolution['species']['name']
                        evolution_id = evolution['species']['url'].split('/')[-2]
                        evolution_to = evolution['evolves_to']
                    
                        for topics in poke_details:
                            if poke_details[topics] not in invalid_values:
                                methods_valids[topics] = poke_details[topics]

                                if type(methods_valids[topics]) == dict and 'name' in methods_valids[topics]:
                                    methods_valids[topics] = methods_valids[topics]['name']
                        evolution_chain[pos][-1].append({'name': evolution_name,'method': return_evolution_method_to_string(methods_valids), 'types': pokelist[int(evolution_id) - 1]['types'], 'id': pokelist[int(evolution_id) - 1]['id'], 'id_url': int(pokelist[int(evolution_id) - 1]['id']), 'relative_name': pokelist[int(evolution_id) - 1]['relative_name'] })

        if not evolution_chain:
            return []

        final_evolution_chain[0]['base'][0]['chain'] = evolution_chain             
        return final_evolution_chain

         
    else:
        return []


for pokemon in pokelist:
    pokemon['evolution_to'] = return_chain_evolution(pokemon)
