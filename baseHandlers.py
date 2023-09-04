import datetime
from telebot import types, TeleBot
import schedule


def get_drive(message: types.Message, bot: TeleBot):
    bot.send_message(message.chat.id,
                     'https://drive.google.com/drive/folders/1JzJN_6DkW6O84QmlJ362W-hpORhWGDh8?usp=share_link')


def get_week_schedule(message: types.Message, bot: TeleBot):
    msg = "Пары на этой неделе:\n\n"
    for l in schedule.getThisWeekSchedule():
        msg += formal_lesson_item(l) + "\n\n"
    bot.send_message(message.chat.id, msg)


def get_full_schedule(message: types.Message, bot: TeleBot):
    msg = "Расписание в этом семестре:\n\n"
    for l in schedule.getAllSchedule():
        msg += formal_lesson_item(l) + "\n\n"
    bot.send_message(message.chat.id, msg)


def formal_lesson_item(lesson_item):
    date = datetime.datetime.strptime(lesson_item['date'], "%Y-%m-%d").date().strftime('%d.%m.%Y')
    lesson_name = lesson_item['lesson_name']
    start = lesson_item['interval_start']
    stop = lesson_item['interval_stop']
    auditory = lesson_item['auditory']
    teacher_name = lesson_item['teacher_name']
    return (f'{date}\n'
            f'{lesson_name} с {start} по {stop} в аудитории {auditory}\n'
            f'Преподаватель: {teacher_name}')


def register_handlers(bot: TeleBot):
    bot.register_message_handler(get_full_schedule, commands=['scheduleall'], pass_bot=True)
    bot.register_message_handler(get_week_schedule, commands=['scheduleweek'], pass_bot=True)
    bot.register_message_handler(get_drive, commands=['drive'], pass_bot=True)