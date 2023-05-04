import datetime
from datetime import timedelta
import json

import openpyxl as op

from recipes import count_brew_for_tanks, beer_params

filename = 'blanks.xlsx'
respons_data = ['Протокол', 5, 'Dunkel', datetime.datetime(2023, 5, 4, 17, 55, 11, 291387), [3, '6']]


def num_tank_and_brews(num):
    nums_brew = count_brew_for_tanks(int(num))
    with open("db.json") as f:
        a = json.load(f)
    firs_brew = a["counts_brews"]
    last_brew = firs_brew + nums_brew - 1
    a["counts_brews"] += nums_brew
    with open("db.json", "w") as f:
        json.dump(a, f)
    return f'{num} ({firs_brew}-{last_brew})'


def format_yeats(list):
    return f'{list[0]}/{list[1]}'


def start_ferments(num):
    hours = num * 8 - 3
    return hours


def prepear(data):
    numbers = num_tank_and_brews(data[1])
    beer_name = data[2]
    date_brew = data[3].strftime('%d.%m.%y')
    yeats = format_yeats(data[-1])
    shpunt = beer_params[beer_name]['Плотность закрытия шпунта']
    cold = beer_params[beer_name]['Плотность начала охлаждения']
    start = (data[3] + timedelta(hours=start_ferments(data[1]))).strftime('%d.%m.%y')
    return [numbers, beer_name, date_brew, yeats, shpunt, cold, start]


data_ok = prepear(respons_data)

wb = op.load_workbook(filename)

ws = wb['Протоколы брож']

# -- номера ячеек для заполнения
fields_to_fill = [ws['A1'], ws['A3'], ws['F3'], ws['J3'], ws['A5'], ws['G5'], ws['B11']]

# -- шаблон записи в протокол
filling_pattern_protocol = [
    'Протокол брожения в ЦКТ № ',
    '   Сорт пива: ', '   Дата варки: ',
    '$-генерация из цкт №',
    '   Плотность для закрытия шпунта: ',
    '   Плотность для включения охлаждения: ', ''
    ]

# -- Протокол брожения --------------------------------------------------------------------


def filling_yeats(data, text):
    '''Заполнение поля дрожжей'''
    num = data.split('/')
    return text.replace('$', num[0]) + num[1]


def prepare_data_to_protocol(data, filling_pattern):
    '''Подготовка данных для внесения в протокол'''
    blank_protocol = []
    for index in range(len(filling_pattern)):
        print(filling_pattern[index] + data[index])
        if '$' in filling_pattern[index]:
            blank_protocol.append(filling_yeats(data[index], filling_pattern[index]))
        else:
            blank_protocol.append(filling_pattern[index] + data[index])
    return blank_protocol


def get_date_start_ferments(data):
    if int(data[0].split()[0]) >= 20:
        return datetime.now() + timedelta(days=1)
    else:
        return datetime.now()


def create_blank_protocol(wb, data):

    # -- получаем список готовых данных
    ready_data_for_protocol = prepare_data_to_protocol(data, filling_pattern_protocol)

    # -- записываем данные в протокол
    for index in range(len(ready_data_for_protocol)):
        fields_to_fill[index].value = ready_data_for_protocol[index]
    # -- заполняем даты брожения
    for day in range(1, 21):
        date = data[2] + timedelta(days=day)         #--------------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ws[f'B{11 + day}'] = date.strftime('%d.%m.%y')

    # -- продумать проверку перед сохранением файла(отправка в телеграм??)
    wb.save('blanks1.xlsx')
    # -- завернуть в функцию с проверкой


if __name__ == '__main__':
    create_blank_protocol(wb, data_ok)
