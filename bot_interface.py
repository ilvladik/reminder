import telebot
from telebot import types

from common_data import token

# Общий интерфейс для бота

# Токен и текущий часовой пояс
bot = telebot.TeleBot(token)
current_timezone = "+03:00(MCK)"


# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Приветствую! Бот предназначен для работы с различными календарями.\n"
                                      "Чтобы узнать как работать с ботом используйте команду /help"
                     )


# Команда /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "С помощью команды /help вы сможете получить справочную информацию.\n"
                                      "С помощью команды /add вы сможете добавить новый календарь.\n"
                                      "С помощью команды /del вы сможете удалить календарь из списка.\n"
                                      "С помощью команды /list вы можете получить полный список календарей.\n"
                                      "Сейчас установлен часовой пояс " + current_timezone + '.' +
                     " Если вы хотите изменить часовой пояс используйте команду /offset"
                     )


# Команда /offset
@bot.message_handler(commands=['offset'])
def offset(message):
    markup = types.ReplyKeyboardMarkup()
    t00 = types.KeyboardButton("00:00")
    t0 = types.KeyboardButton("+01:00")
    t1 = types.KeyboardButton("+02:00")
    t2 = types.KeyboardButton("+03:00")
    t2_5 = types.KeyboardButton("+03:30")
    t3 = types.KeyboardButton("+04:00")
    t3_5 = types.KeyboardButton("+04:30")
    t4 = types.KeyboardButton("+05:00")
    t4_5 = types.KeyboardButton("+05:30")
    t4_6 = types.KeyboardButton("+05:45")
    t5 = types.KeyboardButton("+06:00")
    t5_5 = types.KeyboardButton("+06:30")
    t6 = types.KeyboardButton("+07:00")
    t7 = types.KeyboardButton("+08:00")
    t7_6 = types.KeyboardButton("+08:45")
    t8 = types.KeyboardButton("+09:00")
    t8_5 = types.KeyboardButton("+09:30")
    t9 = types.KeyboardButton("+10:00")
    t9_5 = types.KeyboardButton("+10:30")
    t10 = types.KeyboardButton("+11:00")
    t11 = types.KeyboardButton("+12:00")
    t11_5 = types.KeyboardButton("+12:45")
    t12 = types.KeyboardButton("+13:00")
    t13 = types.KeyboardButton("+14:00")
    t14 = types.KeyboardButton("-01:00")
    t15 = types.KeyboardButton("-02:00")
    t16 = types.KeyboardButton("-03:00")
    t16_5 = types.KeyboardButton("-03:30")
    t17 = types.KeyboardButton("-04:00")
    t18 = types.KeyboardButton("-05:00")
    t19 = types.KeyboardButton("-06:00")
    t20 = types.KeyboardButton("-07:00")
    t21 = types.KeyboardButton("-08:00")
    t22 = types.KeyboardButton("-09:00")
    t23 = types.KeyboardButton("-09:30")
    t24 = types.KeyboardButton("-10:00")
    t25 = types.KeyboardButton("-11:00")
    t26 = types.KeyboardButton("-12:00")
    markup.add(t1, t2, t2_5)
    markup.add(t3, t3_5, t4)
    markup.add(t4_5, t4_6, t5)
    markup.add(t5_5, t6, t7)
    markup.add(t7_6, t8, t8_5)
    markup.add(t9, t9_5, t10)
    markup.add(t11, t11_5, t12)
    markup.add(t13, t14, t15)
    markup.add(t16, t16_5, t17)
    markup.add(t18, t19, t20)
    markup.add(t21, t22, t23)
    markup.add(t24, t25, t26)
    markup.add(t00, t0)
    bot.send_message(message.chat.id, "Выберите пояс", reply_markup=markup)


# Команда /add
@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, "Добавить календарь")


# Команда /del
@bot.message_handler(commands=['del'])
def rm(message):
    bot.send_message(message.chat.id,
                     "Список календарей: \n1)\n2)\n3)\n...\n"
                     "Введите номер календаря, который нужно удалить")


# Команда /list
@bot.message_handler(commands=['list'])
def list(message):
    bot.send_message(message.chat.id, "Список календарей: \n1)\n2)\n3)\n...\n")


# Работа бота нон-стоп
bot.polling(none_stop=True)