import telebot
import sys
import os

import commands.jrrp
import commands.handle

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
    bot.reply_to(message, commands.jrrp.main(message.from_user.id))


@bot.message_handler(func=lambda message: True)
def handle_text_message(message) -> None:
    if commands.handle.main(message) != None:
        bot.reply_to(message, commands.handle.main(message))


if __name__ == "__main__":
    print("Booting...")
    bot.polling()
