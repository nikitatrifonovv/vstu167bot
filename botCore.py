import telebot
from telebot import types
import secrets
import adminHandlers
import baseHandlers


bot = telebot.TeleBot(secrets.TG_TOKEN)


adminHandlers.register_handlers(bot)
baseHandlers.register_handlers(bot)


@bot.message_handler(commands=['start', 'help'])
def say_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Привет. Я персональный помощник вашей группы. Смотри в меню, что я могу.')
    bot.set_my_commands([
        types.BotCommand('/drive', 'Ссылка на диск'),
        types.BotCommand('/scheduleweek', 'Расписание на неделею'),
        types.BotCommand('/scheduleall', 'Полное расписание')

    ])


if __name__ == '__main__':
    bot.infinity_polling()
