import telebot
import sys
import os

import commands.jrrp
import commands.repeat

try:
    BOT_TOKEN = sys.argv[1]
except IndexError:
    BOT_TOKEN = os.getenv("BOTTOKEN")

if not BOT_TOKEN:
    print("No bot token!")
    exit(1)

bot = telebot.TeleBot(token=BOT_TOKEN, parse_mode="HTML")


@bot.message_handler(commands=["jrrp"])
def send_jrrp(message) -> None:
    response = commands.jrrp.main(message.from_user.id)
    bot.reply_to(message, response)


@bot.message_handler(func=lambda message: True)
def repeat_repeat_repeat(message) -> None:
    response = commands.repeat.main(message)
    bot.reply_to(message, response)


if __name__ == "__main__":
    print("Booting...")
    bot.polling()
