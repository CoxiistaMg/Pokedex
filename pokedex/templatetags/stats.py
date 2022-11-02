from django.template.defaultfilters import register


@register.filter 
def stats(stats):
    stat_return = [
        {'name': 'Hp', 'color_bar': '228B22', 'color_stat': '6eaa5e'},
        {'name': 'Atk', 'color_bar': 'B22222', 'color_stat': 'ff4040'},
        {'name': 'Def', 'color_bar': '8B4513', 'color_stat': 'CD853F'},
        {'name': 'SpAtk  ', 'color_bar': 'ff8c00', 'color_stat': 'f0ac47'},
        {'name': 'SpDef  ', 'color_bar': '686868', 'color_stat': 'a9a9a9'},
        {'name': 'Speed  ', 'color_bar': '191970', 'color_stat': '5d46e2'},
    ]

    for pos, stat in enumerate(stats):
        value = stat['base_stat']
        sr = stat_return[pos]
        sr['value'] = value
        sr['width'] = value * 100 / 255
        sr['max'] = int(((( 31 + (252/4) + 2* value + 5))* 1.1) // 1)
        sr['min'] = int((((2* value + 5))* 0.9) // 1)   

        if sr['name'] == 'Hp':
            sr['max'] = int(( 31 + (252/4) + 2 * value)) + 10 + 100
            sr['min'] = int(((2 * value)) + 10 + 100)        

    return stat_return

@register.filter
def result_stats(stats):
    value = 0
    for stat in stats:
        value += stat['base_stat']
    return value
