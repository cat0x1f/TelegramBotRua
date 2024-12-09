import re

MAX_MESSAGE_LENGTH = 30


def main(message) -> str:
    if len(message.text) < MAX_MESSAGE_LENGTH:
        if message.text.endswith("!") or message.text.endswith("！"):
            repeat_text = re.sub(r"[!！]+", "！", message.html_text)
            if "我" in repeat_text or "你" in repeat_text:
                translation_table = str.maketrans("你我", "我你")
                repeat_text = repeat_text.translate(translation_table)
            if "\n" in message.text:
                repeat_text = repeat_text + "\n" + repeat_text + "\n" + repeat_text
            else:
                repeat_text *= 3

            return repeat_text
