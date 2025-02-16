import telebot
import os

import commands.jrrp
import commands.handle


try:
    BOT_TOKEN = os.getenv("BOTTOKEN")
except:
    print("Bad bot token!")
    exit(1)

# 不想手写 args 解析了，先只允许在一个 chat 里使用
# ALLOW_GROUPS=-1145141919
try:
    ALLOW_GROUPS = os.getenv("ALLOW_GROUPS")
except:
    ALLOW_GROUPS = "-1145141919"


bot = telebot.TeleBot(token=BOT_TOKEN, parse_mode="HTML")


@bot.message_handler(commands=["jrrp"])
def send_jrrp(message) -> None:
    if ALLOW_GROUPS == "-1145141919" or str(message.chat.id) == ALLOW_GROUPS:
        bot.reply_to(message, commands.jrrp.main(message.from_user.id))


@bot.message_handler(func=lambda message: True)
def handle_text_message(message) -> None:
    if ALLOW_GROUPS == "-1145141919" or str(message.chat.id) == ALLOW_GROUPS:
        if commands.handle.main(message) != None:
            bot.reply_to(message, commands.handle.main(message))


if __name__ == "__main__":
    print("I'm Working!")
    bot.polling()
