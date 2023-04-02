import telebot
import os


bot = telebot.TeleBot(token=os.getenv("TOKEN"))


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, text="start")


@bot.message_handler(content_types=["text"])
def text_message(message):
    if message == "Выбрать часовой пояс":
        pass
    else:
        bot.send_message(message.chat.id, "Бот работает!")


bot.polling()
