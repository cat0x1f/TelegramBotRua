import re
import commands.aichat
import commands.yes

# TODO
MAX_REPEAT_MESSAGE_LENGTH = 50
MAX_YES_MESSAGE_LENGTH = 20
MAX_CALL_MESSAGE_LENGTH = 50
MAX_AI_CHAT_MESSAGE_LENGTH = 50


# def main(message) -> str:
#     if len(message.text) < MAX_REPEAT_MESSAGE_LENGTH:  # 重复
#         if message.text.endswith("!") or message.text.endswith("！"):
#             return repeat(message)
#     elif len(message.text) < MAX_CALL_MESSAGE_LENGTH:  # Call 回复
#         if message.text.startswith("/"):
#             return call(message)
#     elif len(message.text) < MAX_AI_CHAT_MESSAGE_LENGTH:  # TODO 被 at 后回复
#         if "@cat0x1f_bot" in message.text:
#             return commands.aichat.main(message)
#     elif len(message.text) < MAX_YES_MESSAGE_LENGTH:  # YES 回复
#         return yes(message)


def main(message) -> str:
    if message.text.endswith("!") or message.text.endswith("！"):
        return repeat(message)
    elif message.text.startswith("/"):
        return call(message)
    elif "@cat0x1f_bot" in message.text:
        return commands.aichat.main(message)
    elif len(message.text) < MAX_YES_MESSAGE_LENGTH:  # YES 回复
        return yes(message)


def repeat(message):
    if len(message.text) < MAX_REPEAT_MESSAGE_LENGTH:
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
    return (
        commands.yes.handle_is(message.text)
        or commands.yes.handle_right(message.text)
        or commands.yes.handle_can(message.text)
    )
