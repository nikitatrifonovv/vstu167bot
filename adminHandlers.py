from telebot import types, TeleBot
import userService
import scheduleService


def say_welcome_to_admin(message: types.Message, bot: TeleBot):
    if userService.is_admin(message.from_user.id):
        bot.send_message(message.chat.id, 'Режим администратора доступен.')
        bot.send_message(message.chat.id, 'Вам доступны следующие команды:\n\n'
                                          '/addlesson - добавить записи в расписание.\n\t'
                                          'Дата(Формат YYYY-MM-DD);Название;Начало;Конец;Аудитория;Преподаватель\n'
                                          'Дата(Формат YYYY-MM-DD);Название;Начало;Конец;Аудитория;Преподаватель\n'
                                          '...\n'
                                          '⚠️ Формат даты: YYYY-MM-DD'
                                          'Каждая новая запись с новой строки.\n\n'
                                          '/showlessons - показать полное расписание с id\n\n'
                                          '/deletelesson <id> - удалить запись по id.\n\n'
                                          '/multideletelesson - удалить несколько записей по id\n'
                                          '<id>\n'
                                          '<id>\n'
                                          '...\n\n')
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
        lessons = message.text.splitlines()[1:]
        try:
            for l in lessons:
                items = l.split(';')
                scheduleService.save_lesson(items[0], items[2], items[3], items[1], items[4], items[5])
        except Exception as e:
            bot.send_message(message.chat.id, f'Ошибка: {e}')

        bot.send_message(message.chat.id, 'Успешно!')
    else:
        bot.reply_to(message, 'Извините, но у вас нет доступа к данной функции.')


def show_lessons(message: types.Message, bot: TeleBot):
    if userService.is_admin(message.from_user.id):
        lessons = scheduleService.load_all()
        msg = ''
        for l in lessons:
            print(l)
            msg += (f"{l['id']}\n"
                    f"{l['date']}\n"
                    f"{l['lesson_name']} с {l['interval_start']} по {l['interval_stop']} в аудитории {l['auditory']}\n"
                    f"Преподаватель: {l['teacher_name']}\n\n")
        bot.send_message(message.chat.id, msg)
    else:
        bot.reply_to(message, 'Извините, но у вас нет доступа к данной функции.')


def delete_lessons(message: types.Message, bot: TeleBot):
    if userService.is_admin(message.from_user.id):
        id = message.text.split(' ')[1:]
        scheduleService.delete_lesson(id)
    else:
        bot.reply_to(message, 'Извините, но у вас нет доступа к данной функции.')

def multi_delete_lessons(message: types.Message, bot: TeleBot):
    if userService.is_admin(message.from_user.id):
        ids = message.text.splitlines()[1:]
        for i in ids:
            scheduleService.delete_lesson(i)
    else:
        bot.reply_to(message, 'Извините, но у вас нет доступа к данной функции.')

def register_handlers(bot: TeleBot):
    bot.register_message_handler(say_welcome_to_admin, commands=['admin'], pass_bot=True)
    bot.register_message_handler(add_lessons, commands=['addlesson'], chat_types=['private'], pass_bot=True)
    bot.register_message_handler(add_admin, commands=['addadmin'], chat_types=['private'], pass_bot=True)
    bot.register_message_handler(show_lessons, commands=['showlessons'], chat_types=['private'], pass_bot=True)
    bot.register_message_handler(delete_lessons, commands=['deletelesson'], chat_types=['private'], pass_bot=True)
    bot.register_message_handler(multi_delete_lessons, commands=['multideletelesson'], chat_types=['private'], pass_bot=True)