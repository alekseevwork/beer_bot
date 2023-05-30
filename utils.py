import datetime
from datetime import timedelta
import logging

from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardRemove

from protocol.protocol import start_ferments
from keyboards import nums_brew_keyboard, stat_keyboard


def actual_time(time, nums):
    time_start = datetime.datetime.strptime(time, '%H:%M')
    data_now = datetime.datetime.now().strftime('%d.%m %H:%M')
    actual_data = data_now[:6] + str(time_start.hour) + ':' + str(time_start.minute)
    time_start = datetime.datetime.strptime(actual_data, '%d.%m %H:%M')
    first_loading = time_start + timedelta(hours=6)
    end_brew = time_start + timedelta(hours=start_ferments(nums))
    next_time_start = end_brew - timedelta(hours=3)
    answer = f"""------------------------------------------------
Начало варки - {time_start.strftime('%H:%M / %d.%m')}
Первая перекачка - {first_loading.strftime('%H:%M / %d.%m')}
Конец варки - {end_brew.strftime('%H:%M / %d.%m')}
------------------------------------------------
Начало следуйщей варки: {next_time_start.strftime("%H:%M / %d.%m")}"""
    return answer


async def start_timing(update, context):
    logging.info('Use start_timing')
    await update.message.reply_text(
        'Введите время начала варки', reply_markup=ReplyKeyboardRemove())
    return "time_brew"


async def time_start_brew(update, context):
    logging.info('Use time_start_brew')
    start_brew = update.message.text
    try:
        time_start = datetime.datetime.strptime(start_brew, '%H:%M')
    except ValueError:
        await update.message.reply_text(
        'Введите время в формате 00:00', reply_markup=ReplyKeyboardRemove())
        return "time_brew"
    context.user_data['start_brew'] = start_brew
    await update.message.reply_text(
        'Введите колличество варок', reply_markup=nums_brew_keyboard())
    return "nums_brew"


async def out_answer(update, context):
    logging.info('Use out_answer')
    nums_brew = update.message.text
    answer = actual_time(context.user_data['start_brew'], int(nums_brew))
    await update.message.reply_text(text=answer, reply_markup=stat_keyboard())
    return ConversationHandler.END

# if __name__ == '__main__':
#     time_start = datetime.datetime.strptime(input('Время начала варки: '), '%H:%M')
#     data_now = datetime.datetime.now().strftime('%d.%m %H:%M')
#     actual_data = data_now[:6] + str(time_start.hour) + ':' + str(time_start.minute)
#     time_start = datetime.datetime.strptime(actual_data, '%d.%m %H:%M')
#     while True:
#         counts_brew = int(input('Колличество варок: '))
#         end_brew = time_start + timedelta(hours=start_ferments(counts_brew))
#         print(f"""--------------------------------------
#     Начало варки - {time_start.strftime('%H:%M %d.%m')}
#     Конец варки - {end_brew.strftime('%H:%M %d.%m')}
# --------------------------------------""")
#         time_start = end_brew - timedelta(hours=3)
#         print(f'Начало следуйщей варки: {time_start.strftime("%H:%M %d.%m")}')
