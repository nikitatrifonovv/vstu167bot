from telebot import types, TeleBot
import userService
import scheduleService


def say_welcome_to_admin(message: types.Message, bot: TeleBot):
    if userService.is_admin(message.from_user.id):
        bot.send_message(message.chat.id, 'Режим администратора доступен.')
        bot.send_message(message.chat.id, 'Вам доступны следующие команды:\n'
                                          '/addlesson - добавить записи в расписание\n\n'
                                          'Функции редактирования будут позже\n')
    else: bot.reply_to(message, 'Вам недоступен режим администратора.')


def add_admin(message: types.Message, bot: TeleBot):
    bot.send_message(message.chat.id, 'Перешлите сообщение от пользователя которого хотите добавить.')
    bot.register_next_step_handler(message, add_admin_step_2, bot=bot)


def add_admin_step_2(message: types.Message, bot: TeleBot):
    if message.forward_from is not None:
        id = message.forward_from.id
        username = message.forward_from.username
        if not userService.contains(message.forward_from.id):
            userService.save_user(id,username, 'admin')
            bot.reply_to(message, 'Готово!')
        else:
            bot.reply_to(message, 'Этот пользователь уже существует')
    else:
        bot.reply_to(message, 'Неизвестная ошибка. Добавить пользователя не получилось.')


def add_lessons(message: types.Message, bot: TeleBot):
    if userService.is_admin(message.from_user.id):
        bot.send_message(message.chat.id, 'Следующим сообщением напишите строки в формате: '
                                          '\nДата;Название;Начало;Конец;Аудитория;Преподаватель')
        bot.register_next_step_handler(message, add_lessons_step_2, bot=bot)
    else:
        bot.reply_to(message, 'Извините, но у вас нет доступа к данной функции.')


def add_lessons_step_2(message: types.Message, bot: TeleBot):
    lines = str.splitlines(message.text)
    try:
        for l in lines:
            items = l.split(';')
            scheduleService.save_lesson(items[0], items[2], items[3], items[1], items[4], items[5])
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

    bot.send_message(message.chat.id, 'Успешно!')



def register_handlers(bot: TeleBot):
    bot.register_message_handler(say_welcome_to_admin, commands=['admin'], pass_bot=True)
    bot.register_message_handler(add_lessons, commands=['addlesson'], chat_types=['private'], pass_bot=True)
    bot.register_message_handler(add_admin, commands=['addadmin'], chat_types=['private'], pass_bot=True)