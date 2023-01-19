import random
import logging
import emoji


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

candies = 0

reply_keyboard = [['/rules', '/game'],
                  ['/exit']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5930789314:AAE6ZFjZeelRgPrEFiHAYjvWMVQ862gfJxA'


def start(update, context):
    update.message.reply_text(f"Привет, давай поиграем, \n"
        "/game - Начать игру \n"
        "/rules - Правила игры \n"
        "/exit - Выйти \n",
        reply_markup=markup)


def game(update, context):
    update.message.reply_text(
        "Введите количество конфет для игры",
        reply_markup=ReplyKeyboardRemove()
    )
    print(emoji.emojize('Python is :thumbs_up:', language = 'alias'))
    return 1

def rules(update, context):
    update.message.reply_text(
        """Игроки ходят по очереди. Каждый игрок может взять не более 28 конфет.
        Выигрывает тот, кто заберет последние конфеты""")


def exit(update, context):
    update.message.reply_text(
        "До свидания!", reply_markup=ReplyKeyboardRemove())


def stop(update, context):
    update.message.reply_text("Всего доброго!", reply_markup=markup)
    return ConversationHandler.END


def init_game(update, context):
    global candies
    try:
        candies = int(update.message.text)
        update.message.reply_text(f"На кону {candies} конфет.")
        update.message.reply_text("Ваш ход! Сколько хотите взять конфет?")
        return 2
    except:
        update.message.reply_text("Введите число")


def level_game(update, context):
    global candies
    candies1 = int(update.message.text)
    candies = candies - candies1
    if candies >=29:
        update.message.reply_text(f"На кону осталось {candies} конфет. Мой ход")
        candies2 = random.randint(1, 28)
        update.message.reply_text(f"Я беру {candies2} конфет")
        candies = candies - candies2
        if candies >= 29:
            update.message.reply_text(f"На кону {candies} конфет.")
            update.message.reply_text("Ваш ход! Сколько хотите взять конфет?")
            return 2
        else:
            update.message.reply_text("Ты победил!", reply_markup=markup)
    else:
        update.message.reply_text("Победил я!", reply_markup=markup)
    return ConversationHandler.END


game_handler = ConversationHandler(
entry_points=[CommandHandler('game', game)],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, init_game)],
        2: [MessageHandler(Filters.text & ~Filters.command, level_game)],
    },
    fallbacks=[CommandHandler('stop', stop)]
)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(game_handler)
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("exit", exit))
    

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()