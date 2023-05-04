from telegram import ReplyKeyboardMarkup


def name_brew_keyboard():
    return ReplyKeyboardMarkup([
        ['Keller', 'Dunkel', 'BroFoot'],
        ['Kölsch', 'Wheat']], resize_keyboard=True)


def stat_keyboard():
    return ReplyKeyboardMarkup(
        [["Рассчитать колличество", "Посмотоеть рецепт"],
         ["Отчеты"]],
        resize_keyboard=True,
    )


def report_keyboard():
    return ReplyKeyboardMarkup(
        [["Протокол", "Розлив"], ["Перекачка", "Фильтрация"]],
        resize_keyboard=True)


def yeats_gen_keyboard():
    return ReplyKeyboardMarkup(
        [['1', '2', '3'], ['4', '5', '6'], ['0']],resize_keyboard=True)


def yeats_choice_keyboard():
    return ReplyKeyboardMarkup(
        [['W34/70', 'K-97', 'US-05']], resize_keyboard=True)
