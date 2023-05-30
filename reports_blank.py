import logging

from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from keyboards import name_brew_keyboard, stat_keyboard, yeats_choice_keyboard
from protocol.protocol import create_blank_protocol


async def start_protocol(update, context):
    logging.info('Use start_protocol')
    command = update.message.text
    context.user_data['blank'] = command
    await update.message.reply_text(
        'Введите номер ЦКТ',
        reply_markup=ReplyKeyboardRemove())
    return 'num_tank_protocol'


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
                'Выберите сорт пива',
                reply_markup=name_brew_keyboard())
            return 'name_brew'
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
    create_blank_protocol([context.user_data[i] for i in context.user_data])
    chat_id = update.message.chat_id
    await context.bot.send_document(
        chat_id=chat_id,
        document=open('protocol\protocol.xlsx', 'rb'),   # -- сделать inlain кнопки для добавления отчета в основной файл
        reply_markup=stat_keyboard()
    )
    return ConversationHandler.END
