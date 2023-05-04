import logging

ingredients = {
    'Keller': {
        'Солод': [['Pils', 220], ['Munhen 25', 25]],
        'Хмель': [['Perle', 0.35], ['Mandarina', 0.35], ['Mitlfruh', 0.5]]
        },
    'Dunkel': {
        'Солод': [['Pils', 205], ['Munhen 25', 25], ['Roasted', 15]],
        'Хмель': [['Perle', 0.35], ['Mandarina', 0.35], ['Mitlfruh', 0.5]]
    },
    'Dunkel_1-3': {
        'Солод': [['Pils', 185], ['Munhen 25', 20], ['Roasted', 10]],
        'Хмель': [['Perle', 0.35], ['Mandarina', 0.35], ['Mitlfruh', 0.5]]
    },
    'BroFoot': {
        'Солод': [['Pils Premium', 220], ['Cara Hell', 12.5]],
        'Хмель': [['Perle', 0.5], ['Select', 1]]
    },
    'Kölsch': {
        'Солод': [['Pils', 200], ['Munhen 15', 15], ['Wheat', 25]],
        'Хмель': [['Perle', 0.5], ['Select', 0.5]]
    },
    'Wheat': {
        'Солод': [['Pale Ale', 115], ['Wheat', 115]],
        'Хмель': [['Mandarina', 0.5], ['Cascade', 0.7]]
        },
}
solod_pack = {
    'Pils': 40,
    'Pils Premium': 25,
    'Pale Ale': 40,
    'Munhen 25': 40,
    'Munhen 15': 40,
    'Wheat': 40,
    'Cara Hell': 25,
    'Roasted': 25
}
beer_params = {
    'Keller': {
        '№ программы затирания': '1',
        'Количество воды для затирания': '750',
        '№ программы кипячения': '8',
        'Дрожжи': 'W-34/70',
        't° брожения': '11°C (на сухих дрожжах 13°C)',
        'Плотность закрытия шпунта': '7',
        'Плотность начала охлаждения': '4'
    },
    'Dunkel': {
        '№ программы затирания': '1',
        'Количество воды для затирания': '750',
        '№ программы кипячения': '8',
        'Дрожжи': 'W-34/70',
        't° брожения': '11°C (на сухих дрожжах 13°C)',
        'Плотность закрытия шпунта': '7',
        'Плотность начала охлаждения': '4,2'
        },
    'BroFoot': {
        '№ программы затирания': '10',
        'Количество воды для затирания': '700',
        '№ программы кипячения': '9',
        'Дрожжи': 'W-34/70',
        't° брожения': '11°C (на сухих дрожжах 13°C)',
        'Плотность закрытия шпунта': '6',
        'Плотность начала охлаждения': '3,5'
        },
    'Kölsch': {
        '№ программы затирания': '9',
        'Количество воды для затирания': '750',
        '№ программы кипячения': '8',
        'Дрожжи': 'K-97',
        't° брожения': '15°C (на сухих дрожжах 17°C)',
        'Плотность закрытия шпунта': '5,5',
        'Плотность начала охлаждения': '3,5'
        },
    'Wheat': {
        '№ программы затирания': '2',
        'Количество воды для затирания': '750',
        '№ программы кипячения': '8',
        'Дрожжи': 'K-97',
        't° брожения': '18°C (на сухих дрожжах 20°C)',
        'Плотность закрытия шпунта': '6',
        'Плотность начала охлаждения': '4'
        },
}


def count_bag_solod(solod_name, solod_kg):
    solod_bag = solod_pack[solod_name]
    if solod_kg % solod_bag == 0:
        return solod_kg
    return ((solod_kg // solod_bag) + 1) * solod_bag


def count_brew_for_tanks(number_tank):
    logging.info(f'Use count_brew_for_tanks {number_tank}')
    if number_tank > 19:
        return 8
    elif 20 > number_tank > 8:
        return 4
    elif number_tank == 19:
        return 1
    return 2


def count_materials(beer_name, number_tank,):
    logging.info(f'Use count_materials {beer_name} {number_tank}')
    if beer_name == 'Dunkel' and number_tank < 4:
        beer_name = 'Dunkel_1-3'
    logging.info(f'{beer_name}')
    nums = count_brew_for_tanks(number_tank)
    return format_result(beer_name, nums=nums, number_tank=number_tank)


def create_dict_ingridients(beer_name, nums=1):
    logging.info(f'Use create_dict_ingridients {beer_name} {nums}')
    result = {}
    for type_ingredient in ingredients[beer_name]:
        for ingredient in ingredients[beer_name][type_ingredient]:
            result[type_ingredient] = result.get(type_ingredient, []) + [[ingredient[0], ingredient[1] * nums]]
    return result


def count_ingridients_for_tank(beer_name, dict, number_tank):
    logging.info('Use count_ingridients_for_tank')
    answer = f"<b>Сырьё для {beer_name} в ЦКТ #{number_tank}:</b>\n"
    for type_ingredient in dict:
        answer += f'<b>{type_ingredient}</b>:\n'
        for ingredient in dict[type_ingredient]:
            if type_ingredient == 'Солод':
                solod = count_bag_solod(ingredient[0], ingredient[1])
                answer += f'{ingredient[0]} - {ingredient[1]} / в целых мешках - {solod}\n'
            else:
                answer += f'{ingredient[0]} - {ingredient[1]}\n'
    return answer


def format_result(beer_name, nums=1, number_tank=None):
    logging.info(f'Use format_result {nums}')
    dict_ingridients = create_dict_ingridients(beer_name, nums)
    if beer_name == 'Dunkel_1-3':
        beer_name = 'Dunkel'
    if nums > 1:
        answer = count_ingridients_for_tank(beer_name, dict_ingridients, number_tank)
    else:
        answer = f"<b>{beer_name}:</b>\n"
        for type_ingredient in dict_ingridients:
            answer += f'<b>{type_ingredient}</b>:\n'
            for ingredient in dict_ingridients[type_ingredient]:
                answer += f'{ingredient[0]} - {ingredient[1]}\n'
    return answer


def get_beer_info(beer_name):
    '''materials_for_brew'''
    logging.info('Use get_beer_info')
    answer = f'<b>{beer_name}:</b>\n'
    for description, value in beer_params[beer_name].items():
        answer += f'{description} - {value}\n'
    answer += format_result(beer_name)
    return answer
