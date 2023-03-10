import logging

from telegram.ext import Application, filters, CommandHandler, ConversationHandler, MessageHandler

import settings
from handlers import info_bot, num_tank, start_counts, name_brew, brew_dontknow, recipes_brew, start_beer_info

logging.basicConfig(filename='bot.log', level=logging.INFO)


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
    bot.add_handler(CommandHandler("start", info_bot))
    bot.add_handler(beer_info)
    bot.add_handler(materials_for_brew)

    logging.info('Bot started')
    bot.run_polling()


if __name__ == '__main__':
    main()
