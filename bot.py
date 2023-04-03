from telebot import TeleBot, types
import network
import sql
import os


TIMEZONES = """
UTC-12:00 UTC-11:00 UTC-10:00 UTC-09:30 UTC-09:00 UTC-08:00
UTC-07:00 UTC-06:00 UTC-05:00 UTC-04:00 UTC-03:30 UTC-03:00
UTC-02:00 UTC-01:00 UTC+00:00 UTC+01:00 UTC+02:00 UTC+03:00
UTC+03:30 UTC+04:00 UTC+04:30 UTC+05:00 UTC+05:30 UTC+05:45
UTC+06:00 UTC+06:30 UTC+07:00 UTC+08:00 UTC+08:45 UTC+09:00
UTC+09:30 UTC+10:00 UTC+10:30 UTC+11:00 UTC+12:00 UTC+12:45
UTC+13:00 UTC+14:00"""
TIMEZONE_BUTTONS = [types.KeyboardButton(tz) for tz in TIMEZONES.split()]
TIMEZONE_MARKUP = types.ReplyKeyboardMarkup()
for idx in range(0, len(TIMEZONE_BUTTONS), 3):
    TIMEZONE_MARKUP.add(*TIMEZONE_BUTTONS[idx : idx + 3])

DEFAULT_TZ = "UTC+03:00"

bot = TeleBot(token=os.getenv("TOKEN"))


@bot.message_handler(commands=["start"])
def start_message(message: types.Message):
    chat = message.chat.id
    message_text = """
Приветствую! Бот предназначен для работы с различными календарями.
Чтобы узнать как работать с ботом используйте команду /help
    """
    try:
        sql.add_chat(chat, DEFAULT_TZ)
    except ValueError:
        message_text = "Произошла ошибка в работе бота"
    bot.send_message(chat, message_text)


@bot.message_handler(commands=["help"])
def help_message(message: types.Message):
    chat = message.chat.id
    try:
        tz = sql.select_chat_tz(chat)
        message_text = f"""
С помощью команды /help вы сможете получить справочную информацию.
С помощью команды /add вы сможете добавить новый календарь: /add %ссылка%
С помощью команды /del вы сможете удалить календарь из списка: /del %ссылка%
С помощью команды /list вы можете получить полный список календарей.
Сейчас установлен часовой пояс {tz}.
Если вы хотите изменить часовой пояс используйте команду /offset
    """
    except ValueError:
        message_text = "Произошла ошибка в работе бота"

    bot.send_message(chat, message_text)


@bot.message_handler(commands=["offset"])
def offset_message(message: types.Message):
    bot.send_message(
        message.chat.id, "Выберите часовой пояс", reply_markup=TIMEZONE_MARKUP
    )


@bot.message_handler(commands=["add"])
def add_message(message: types.Message):
    chat = message.chat.id
    link = message.text[4:].strip()
    if len(link) == 0:
        return
    try:
        network.get_calendar_by_url(link)
        sql.add_cal(link)
        sql.add_chat_cal(chat, link)
        message_text = "Календарь добавлен"
    except ValueError:
        message_text = "Некорректная ссылка"
    bot.send_message(chat, message_text)


@bot.message_handler(commands=["del"])
def del_message(message):
    chat = message.chat.id
    link = message.text[4:].strip()
    if len(link) == 0:
        return
    try:
        sql.del_chat_cal(chat, link)
        message_text = "Календарь удалён или не был привязан"
    except ValueError:
        message_text = "Некорректная ссылка"
    bot.send_message(chat, message_text)


@bot.message_handler(commands=["list"])
def list_message(message: types.Message):
    chat = message.chat.id
    try:
        calendars = sql.select_chat_cal(chat)
        if len(calendars) == 0:
            message_text = """
На данный момент ни один календарь не добавлен
Чтобы это сделать напишите /add %ссылка%
"""
        else:
            message_text = "\n\n".join(calendars)
    except ValueError:
        message_text = "Произошла ошибка в работе бота"
    bot.send_message(chat, message_text)


@bot.message_handler(content_types=["text"])
def utc_message(message: types.Message):
    chat = message.chat.id
    text = message.text
    if text in TIMEZONES.split():
        try:
            sql.update_offset(chat, text)
            message_text = f"Часовой пояс успешно изменён на {text}"
        except ValueError:
            message_text = "Произошла ошибка при попытке изменить часовой пояс"
        bot.send_message(chat, message_text)


sql.create_db()
bot.polling()
