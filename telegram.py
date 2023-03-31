# Для установки telebot:
# 1) pip install pytelegrambotapi
# 2) ALT + ENTER (Возможно неправильная установка)
import telebot

from common_data import token

bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, text="start")


@bot.message_handler(content_types=['text'])
def text_message(message):
    if (message == 'Выбрать часовой пояс'):
        pass
    else:
        bot.send_message(message.chat.id, "Бот работает!")


bot.polling()
