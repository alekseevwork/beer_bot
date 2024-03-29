import logging

from telegram.ext import Application, filters, CommandHandler, ConversationHandler, MessageHandler

import settings
from handlers import (info_bot, num_tank, start_counts, name_brew, brew_dontknow,
                      recipes_brew, start_beer_info, start_reports, sorry)
from reports_blank import start_protocol, choice_yeats_gen, num_tank_protocol, from_tank
from utils import start_timing, time_start_brew, out_answer


logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():

    bot = Application.builder().token(settings.BOT_API).build()

    materials_for_brew = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^(Рассчитать колличество)$'), start_counts)
            ],
        states={
            "name_brew": [MessageHandler(filters.Regex('^(Keller|Dunkel|BroFoot|Kölsch|Wheat)$'), name_brew)],
            "num_tank": [MessageHandler(filters.TEXT, num_tank)],
            },
        fallbacks=[
            MessageHandler(
                filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.LOCATION, brew_dontknow)
            ]
        )
    beer_info = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^(Посмотоеть рецепт)$'), start_beer_info)
            ],
        states={
            "recipes_brew": [MessageHandler(filters.Regex('^(Keller|Dunkel|BroFoot|Kölsch|Wheat)$'), recipes_brew)],
            },
        fallbacks=[
            MessageHandler(
                filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.LOCATION, brew_dontknow)
            ]
        )
    protocol_blank = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^(Протокол)$'), start_protocol)
            ],
        states={
            "num_tank_protocol": [MessageHandler(filters.TEXT, num_tank_protocol)],
            "name_brew": [MessageHandler(filters.Regex('^(Keller|Dunkel|BroFoot|Kölsch|Wheat)$'), name_brew)],
            "choice_yeats_gen": [MessageHandler(filters.TEXT, choice_yeats_gen)],
            "from_tank": [MessageHandler(filters.TEXT, from_tank)],
            },
        fallbacks=[
            MessageHandler(
                filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.LOCATION, brew_dontknow)
            ]
    )
    timing_brew = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^(Время варки)$'), start_timing)
        ],
        states={
            "time_brew": [MessageHandler(filters.TEXT, time_start_brew)],
            "nums_brew": [MessageHandler(filters.TEXT, out_answer)]
            },
        fallbacks=[
            MessageHandler(
                filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.LOCATION, brew_dontknow)
            ]
    )
    pumping_blank = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^(Перекачка)$'), sorry)
        ],
        states={
            },
        fallbacks=[
            MessageHandler(
                filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.LOCATION, brew_dontknow)
            ]
    )
    filtration_blank = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^(Фильтрация)$'), sorry)
        ],
        states={
            },
        fallbacks=[
            MessageHandler(
                filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.LOCATION, brew_dontknow)
            ]
    )
    bot.add_handler(CommandHandler("start", info_bot))
    bot.add_handler(MessageHandler(filters.Regex('^(Отчеты)$'), start_reports))
    bot.add_handler(beer_info)
    bot.add_handler(materials_for_brew)
    bot.add_handler(protocol_blank)
    bot.add_handler(timing_brew)
    bot.add_handler(pumping_blank)
    bot.add_handler(filtration_blank)
    bot.add_handler(MessageHandler(filters.TEXT, info_bot))

    logging.info('Bot started')
    bot.run_polling()


if __name__ == '__main__':
    main()
