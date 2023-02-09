import telebot
import logging

import schedule

from telebot import types

bot = telebot.TeleBot("5832600016:AAExkWpia4BGgTRTRUvFqq7R3bcQ7o-sttI")

file_schedule = open('schedule.csv')


@bot.message_handler(commands=['start', 'help'])
def say_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Привет. Я персональный помощник вашей группы. Смотри в меню, что я могу.')
    bot.set_my_commands([
        types.BotCommand('/drive', 'Ссылка на диск'),
        types.BotCommand('/scheduleweek', 'Расписание на неделею'),
        types.BotCommand('/scheduleall', 'Полное расписание')

    ])


@bot.message_handler(commands=['drive'])
def week(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     'https://drive.google.com/drive/folders/1JzJN_6DkW6O84QmlJ362W-hpORhWGDh8?usp=share_link')


@bot.message_handler(commands=['scheduleweek'])
def week(message: telebot.types.Message):
    msg = "Пары на этой неделе:\n\n"
    for l in schedule.getSchedule('schedule.csv', True):
        msg += format_sch_lesson(l) + "\n\n"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['scheduleall'])
def week(message: telebot.types.Message):
    msg = "Расписание в этом семестре:\n\n"
    for l in schedule.getSchedule('schedule.csv'):
        msg += format_sch_lesson(l) + "\n\n"
    bot.send_message(message.chat.id, msg)


def format_sch_lesson(lesson_line):
    return f'{lesson_line[0]}\n{lesson_line[1]} с {lesson_line[4]} по {lesson_line[5]} в аудитории {lesson_line[3]}\nПреподаватель: {lesson_line[2]}'


if __name__ == '__main__':
    bot.infinity_polling()
