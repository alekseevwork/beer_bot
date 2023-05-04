import logging
from datetime import datetime

from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from utils import name_brew_keyboard, yeats_gen_keyboard, stat_keyboard, yeats_choice_keyboard


async def start_protocol(update, context):
    logging.info('Use start_protocol')
    command = update.message.text
    context.user_data['blank'] = command
    await update.message.reply_text(
        'Введите название сорта',
        reply_markup=name_brew_keyboard())
    return 'name_brew'


async def num_tank_protocol(update, context):
    logging.info('Use num_tank_protocol')
    try:
        if int(update.message.text) not in range(1, 26):
            await update.message.reply_text('Нет ЦКТ с таким номером, попробуйте еще')
            return 'num_tank_protocol'
        else:
            num_tank = int(update.message.text)
            context.user_data['num_tank'] = num_tank
            await update.message.reply_text(
                'Введите генерацию дрожжей',
                reply_markup=yeats_gen_keyboard())
            return 'choice_yeats_gen'
    except ValueError:
        await update.message.reply_text('Номер ЦКТ должен быть числом, попробуйте еще')
        return 'num_tank_protocol'


async def choice_yeats_gen(update, context):
    logging.info('Use choice_yeats_gen')
    gen_yeats = int(update.message.text)
    context.user_data['gen_yeats'] = [gen_yeats]
    if gen_yeats == 0:
        await update.message.reply_text(
            'Какие дрожжи?',
            reply_markup=yeats_choice_keyboard()
        )
        return 'from_tank'
    await update.message.reply_text(
        'Из какой ЦКТ?',
        reply_markup=ReplyKeyboardRemove())
    return 'from_tank'


async def from_tank(update, context):
    logging.info('Use from_tank')
    from_tank = update.message.text
    context.user_data['gen_yeats'].append(from_tank)
    context.user_data['date_brew'] = datetime.now().strftime('%d.%m.%y')
    for k, v in context.user_data.items():
        print(k, v)
    await update.message.reply_text(
        'Готово',
        reply_markup=stat_keyboard())
    return ConversationHandler.END