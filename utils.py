from telegram import ReplyKeyboardMarkup


def name_brew_keyboard():
    return ReplyKeyboardMarkup([
        ['Keller', 'Dunkel', 'BroFoot'],
        ['Kölsch', 'Wheat']], resize_keyboard=True)


def stat_keyboard():
    return ReplyKeyboardMarkup(
        [["Рассчитать колличество"], ["Посмотоеть рецепт"]],
        resize_keyboard=True,
    )
