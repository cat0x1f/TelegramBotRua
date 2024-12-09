import re
import commands.yes

REPEAT_MAX_MESSAGE_LENGTH = 30


def main(message) -> str:
    if message.text.endswith("!") or message.text.endswith("！"):
        return repeat(message)
    elif message.text.startswith("/"):
        return call(message)
    else:
        return yes(message)


def repeat(message):
    if len(message.text) < REPEAT_MAX_MESSAGE_LENGTH:
        repeat_text = re.sub(r"[!！]+", "！", message.html_text)
        if "我" in repeat_text or "你" in repeat_text:
            translation_table = str.maketrans("你我", "我你")
            repeat_text = repeat_text.translate(translation_table)
        if "\n" in message.text:
            repeat_text = repeat_text + "\n" + repeat_text + "\n" + repeat_text
        else:
            repeat_text *= 3

        return repeat_text


def call(message):
    splited_message = message.text.lstrip("/").split()  # 做的事
    if len(splited_message) <= 2:
        sender_name = message.from_user.full_name  # 发送的人
        if message.reply_to_message != None:
            reply_to_user_name = (
                message.reply_to_message.from_user.full_name
            )  # 回复的人
        else:
            reply_to_user_name = "自己"

        if len(splited_message) == 2:
            return f"{sender_name}{splited_message[0]}了{reply_to_user_name}{splited_message[1]}! "
        elif len(splited_message) == 1:
            return f"{sender_name}{splited_message[0]}了{reply_to_user_name}! "


def yes(message):
    if len(message.text) <= 20:
        return (
            commands.yes.handle_is(message.text)
            or commands.yes.handle_right(message.text)
            or commands.yes.handle_can(message.text)
        )
