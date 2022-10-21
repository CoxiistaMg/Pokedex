import requests 
import json
from pathlib import Path


pokenum = 890
tms_number = 1688
tm_valid_number = 778
abilitynum = 267
abilitylist = {}
pokelist = []
forms = []
tms = []
formslist = []
moveslist = []

img_error = {
    774: 'minior-meteor',
    778: 'mimikyu',
}
trade_points = {32: 'nidoran♂', 678: 'meowstic♂', 876:'indeedee♂', 29: 'nidoran♀', 122: "mr Mine"}

poke_var_name = [
    'galar',
    'alola',
    'mega',
    'hisui',
    'gmax',

]

pokesearch = []
gens = ['yellow', 'crystal', 'firered-leafgreen', 'heartgold-soulsilver', 
        'black-2-white-2', "omega-ruby-alpha-sapphire", 'ultra-sun-ultra-moon', 'sword-shield']

BASE_DIR = Path(__file__).resolve().parent.parent
pokenum = 890
movesnum = 826
tms_number = 1688
tm_valid_number = 778
abilitynum = 267
abilitylist = {}
pokelist = []
forms = []
tms = []
formslist = []
moveslist = []
learn_groups = [
    'egg',
    'level-up',
    'tutor',
    'machine',
]

contador = 0
try:
    with open(BASE_DIR /"moves.json", "r") as outfile:
        moveslist = outfile.read()
        moveslist = json.loads(moveslist)
        contador = len(moveslist)

        if contador != 826:
            raise ValueError()

except:
    for each in range(1, movesnum+1):
        moves = requests.get(f'https://pokeapi.co/api/v2/move/{contador}/').json()
        

        name = moves['name']
        accuracy = moves['accuracy'] 
        power = moves['power']
        pp = moves['pp']
        dg_class = moves['damage_class']['name']
        priority = moves['priority']
        moves_type = moves['type']['name']
        try:
            effect = moves['effect_entries'][0]['short_effect']
                
        except:
            effect = moves['flavor_text_entries'][7]['flavor_text']
                

        print('moves\n', name)
        print(contador)

        moveslist.append((
            name,
            accuracy,
            power,
            pp,
            dg_class,
            priority,
            moves_type,
            effect
            ))

    with open(BASE_DIR /"moves.json", "w") as outfile:
        outfile.write(json.dumps(moveslist, indent=3))




try:
    with open(BASE_DIR /"tms.json", "r") as outfile:
        tms = outfile.read()
        tms = json.loads(tms)
        contador = len(tms)

        if len(tms) != 778:
            raise ValueError('')

except:
    with open(BASE_DIR /"tms.json", "w") as outfile:
        count = 1
        for contador in range(1, tms_number+1):
            if type(tms) != list:
                tms = []
        
            tm = requests.get(f'https://pokeapi.co/api/v2/machine/{contador}/').json()

            try:
                name = tm['item']['name']
                move = tm['move']['url'].split('/')[-2]
                version = tm['version_group']['name']
                if version in gens:
                    tms.append((
                        name,
                        move,
                        gens.index(version)
                    ))
                    
                    print('tms')
                    print(f'{count} / {tm_valid_number}')
                    count += 1
                      
                    
                if contador == 1689:
                    raise ValueError('')

            except:
                outfile.write(json.dumps(tms, indent=3))
        
def ability_start():
    contador = 1

    for number in range(1, abilitynum+1):
        ability = requests.get(f'https://pokeapi.co/api/v2/ability/{number}').json()
            
        for element in ability['effect_entries']:
            if element['language']['name'] == 'en':
                abilitylist[ability['name']] = element['effect']
                
        if not ability['effect_entries']:
            text = ability['flavor_text_entries'][7]['flavor_text']
            abilitylist[ability['name']] = text

        print('ability')
        print(f'{contador} / {abilitynum}' )
        contador += 1

def pokemon_start(list_poke, form=False, list_ =pokelist):
    global pokelist
    contador = 1

    for number in list_poke:
        gen_moves = {}
        pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{number}').json()

        for each in pokemon['moves']:
            num = each['move']['url'].split('/')[-2]
            for version in each['version_group_details']:
                if version['version_group']['name'] in gens:
                    if version['move_learn_method']['name'] in learn_groups:
                        i = gens.index(version['version_group']['name'])
                        method = learn_groups.index(version['move_learn_method']['name'])
                        level = version['level_learned_at']
                        if i not in gen_moves:
                            gen_moves[i] = []

                        gen_moves[i].append((int(method), level, int(num)))

        del pokemon['sprites']
        pokemon['moves'] = gen_moves.copy()
        del pokemon['game_indices']
        del pokemon['species']
        del pokemon['forms']

        
        if not form:
            specie = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{number}/').json()
            chain_number = specie['evolution_chain']['url'].split('/')[-2]
            chain = requests.get(f'https://pokeapi.co/api/v2/evolution-chain/{chain_number}/').json()
            pokemon['evolution_to'] = chain['chain']['evolves_to']
            pokemon['evolution_base'] = chain['chain']['species']['name']
            pokemon['capture_rate'] = specie['capture_rate']
            pokemon['gender_rate'] = specie['gender_rate']
            pokemon['egg_groups'] = [specie['egg_groups']]
            pokemon['growth_rate'] = specie['growth_rate']['name']
            pokemon['color'] = specie['color']


            if len(specie['varieties']) > 1:
                varieties = {}
                for each in specie['varieties']:
                    relative = each['pokemon']["name"].split("-").copy()
                    name = list(filter(lambda x: x in poke_var_name, relative))
                    name_ = list(filter(lambda x: x not in poke_var_name, relative))
                    varieties[each['pokemon']['name']] =  ' '.join(name) + ' ' + ' '.join(name_)

                pokemon['varieties'] = varieties
    
        for ability in pokemon["abilities"]:
            del ability['ability']['url']
                
        if type(list_) != list:
            list_ = []

        list_.append(pokemon)
        print('pokemon')
        print(f'{contador} / {len(list_poke)}' )
        
        contador += 1
    return list_

try:
    with open(BASE_DIR /"ability.json", "r") as outfile:
        abilitylist = outfile.read()
        abilitylist = json.loads(abilitylist)

        if len(abilitylist) != abilitynum:
            raise FileNotFoundError("!")
        
except:
    with open(BASE_DIR /"ability.json", 'w') as outfile:
        ability_start()
        outfile.write(json.dumps(abilitylist, indent=3))

try:
    with open(BASE_DIR /"pokemons.json", "r") as outfile:
        pokelist = outfile.read()
        pokelist = json.loads(pokelist)
        
        if len(pokelist) < pokenum:
            raise FileNotFoundError("!")
        
except:
    with open(BASE_DIR /"pokemons.json", 'w') as outfile:
        pokelist = pokemon_start(range(1, pokenum+1), False) 
        outfile.write(json.dumps(pokelist, indent=3))

try:
    with open(BASE_DIR /"forms.json", "r") as outfile:
        for pokemon in pokelist:
            if 'varieties' in pokemon:
                poke_var = pokemon['varieties'].copy()
              
                for pos, var in enumerate(poke_var):
                    if pos > 0:
                        forms.append(var)
        
        formslist = outfile.read()
        formslist = json.loads(formslist)
        if len(formslist) != len(forms):
            raise FileNotFoundError("!")
               
except:
    with open(BASE_DIR /"forms.json", 'w') as outfile:
        formslist = pokemon_start(forms, True, formslist)
        outfile.write(json.dumps(formslist, indent=3))

dict_tms = {}
for each in tms:

    if each[2] not in dict_tms:

        dict_tms[each[2]] = {}
    
    dict_tms[each[2]][each[1]] = each[0]
    

map_varieties = {}
for pokemons in formslist:
    for ability in pokemons["abilities"]:
        name = ability['ability']['name']
        ability['ability']['text'] = abilitylist[name]
        

for pokemons in pokelist:
    relative = pokemons["name"].split("-")[0]
    pokemons['relative_name'] = relative
    pokemon = {'id': pokemons['id'], 'name': pokemons['name'], 'types': [x['type']['name'] for x in pokemons['types']], "relative_name": relative}
    pokesearch.append(pokemon)

    for ability in pokemons["abilities"]:
        name = ability['ability']['name']
        ability['ability']['text'] = abilitylist[name]
    

for id_ in trade_points:
    pokelist[id_-1]['relative_name'] = trade_points[id_]
    pokesearch[id_-1]['relative_name'] = trade_points[id_]

for id_ in img_error:
    pokesearch[id_-1]["name"] = img_error[id_]


