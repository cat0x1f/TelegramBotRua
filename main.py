import time
import os
import telebot
import logging
import commands.jrrp
import commands.handle
import commands.aichat

BOT_TOKEN = os.getenv("BOT_TOKEN")
OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
ALLOWED_GROUPS = set(os.getenv("ALLOWED_GROUPS", "-1145141919810").split(","))

log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}
level = log_levels.get(LOG_LEVEL, logging.INFO)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=level,
)
logger = logging.getLogger()

if not BOT_TOKEN:
    logger.error("No BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(token=BOT_TOKEN, parse_mode="HTML")
commands.aichat.ChatConfig.OLLAMA_MODEL = OLLAMA_MODEL
commands.aichat.ChatConfig.OLLAMA_ENDPOINT = OLLAMA_ENDPOINT


def is_allowed_group(chat_id: int) -> bool:
    return str(chat_id) in ALLOWED_GROUPS or "-1145141919810" in ALLOWED_GROUPS


@bot.message_handler(commands=["jrrp"])
def command_jrrp(message) -> None:
    if is_allowed_group(message.chat.id):
        bot.reply_to(message, commands.jrrp.main(message.from_user.id))


@bot.message_handler(commands=["chat"])
def command_chat(message) -> None:
    if is_allowed_group(message.chat.id):
        logger.debug(f"YEAH AI INPUT - {message.text}")
        response = commands.aichat.main(message)
        logger.debug(f"YEAH AI OUTPUT - {response}")
        bot.reply_to(message, response)


@bot.message_handler(func=lambda message: True)
def handle_text_message(message) -> None:
    if is_allowed_group(message.chat.id):
        logger.debug(f"JUST TEXT HANDLE - {message}")
        if response := commands.handle.main(message):
            bot.reply_to(message, response)


def start_bot():
    while True:
        try:
            logger.info("I'm Running!")
            bot.polling(non_stop=True)
        except Exception as e:
            logger.error(f"Connection error: {e}")
            time.sleep(10)


if __name__ == "__main__":
    start_bot()
