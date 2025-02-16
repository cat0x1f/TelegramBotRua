import re
import logging
import commands.yes

MAX_REPEAT_MESSAGE_LENGTH = 30
MAX_YES_MESSAGE_LENGTH = 30
MAX_CALL_MESSAGE_LENGTH = 30

logger = logging.getLogger()


def main(message) -> str:
    message_length = len(message.text)

    if (
        message.text.endswith(("!", "！"))
        and message_length < MAX_REPEAT_MESSAGE_LENGTH
    ):
        return repeat(message)

    elif message.text.startswith("/") and message_length < MAX_CALL_MESSAGE_LENGTH:
        return call(message)

    elif message_length < MAX_YES_MESSAGE_LENGTH:
        return yes(message)


def repeat(message) -> str:
    repeat_text = re.sub(r"[!！]+", "！", message.html_text)

    if "我" in repeat_text or "你" in repeat_text:
        repeat_text = repeat_text.translate(str.maketrans("你我", "我你"))

    if "\n" in message.text:
        repeat_text = f"{repeat_text}\n{repeat_text}\n{repeat_text}"
    else:
        repeat_text *= 3

    logger.debug(f"OH REPEAT - {repeat_text}")
    return repeat_text


def call(message) -> str:
    splited_message = message.text.lstrip("/").split()
    sender_name = message.from_user.full_name
    reply_to_user_name = message.reply_to_message.from_user.full_name

    if len(splited_message) == 2:
        response = f"{sender_name}{splited_message[0]}了{reply_to_user_name}{splited_message[1]}!"
    elif len(splited_message) == 1:
        response = f"{sender_name}{splited_message[0]}了{reply_to_user_name}!"

    logger.debug(f"OH CALL - {response}")
    return response


def yes(message):
    response = (
        commands.yes.handle_is(message.text)
        or commands.yes.handle_right(message.text)
        or commands.yes.handle_can(message.text)
    )
    logger.debug(f"OH YES - {response}")
    return response
