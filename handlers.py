import logging

from telegram import ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import ConversationHandler

from utils import stat_keyboard, name_brew_keyboard
from recipes import count_materials, get_beer_info


async def info_bot(update, context):
    logging.info('Use info_bot')
    await update.message.reply_text(
        'Бот для подсчета сырья на варку',
        reply_markup=stat_keyboard()
        )


async def start_counts(update, context):
    logging.info('Use info_bot')
    await update.message.reply_text(
        'Введите название сорта',
        reply_markup=name_brew_keyboard())
    return 'name_brew'


async def name_brew(update, context):
    logging.info('Use name_brew')
    beer_name = update.message.text
    logging.info(f'{beer_name}')
    context.user_data['beer_name'] = beer_name
    await update.message.reply_text(
        'Введите номер ЦКТ',
        reply_markup=ReplyKeyboardRemove())
    return 'num_tank'


async def num_tank(update, context):
    logging.info('Use num_tank')
    num_tank = int(update.message.text)
    beer_name = context.user_data['beer_name']
    answer = count_materials(beer_name, num_tank)
    await update.message.reply_text(
        f'{answer}',
        reply_markup=stat_keyboard(),
        parse_mode=ParseMode.HTML
        )
    return ConversationHandler.END


async def brew_dontknow(update, context):
    logging.info('Use brew_dontknow')
    await update.message.reply_text('Я вас не понимаю')


async def start_beer_info(update, context):
    logging.info('Use beer_info')
    await update.message.reply_text(
        'Введите название сорта',
        reply_markup=name_brew_keyboard())
    return 'recipes_brew'


async def recipes_brew(update, context):
    logging.info('Use recipes_brew')
    beer_name = update.message.text
    beer_info = get_beer_info(beer_name)
    await update.message.reply_text(
        beer_info,
        reply_markup=stat_keyboard(),
        parse_mode=ParseMode.HTML)
    return ConversationHandler.END
