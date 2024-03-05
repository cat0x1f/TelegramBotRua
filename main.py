# 使用 python3 main.py yourtoken 来启动，比如 python3 main.py 114514:ABCDEFGO_HIJKLMNOxE
from telebot.async_telebot import AsyncTeleBot
from datetime import datetime, timedelta
import asyncio
import random
import sys
import re

JRRP_GOOD_DAYS = [
    202467,
    202468,
    202469,
]

bot = AsyncTeleBot(token=str(sys.argv[1]), parse_mode="MARKDOWN")


@bot.message_handler(commands=["jrrp"])
async def send_jrrp(message):
    score = await from_input_get_score(message.from_user.id)
    reply = await jrrp_text_init(score)
    await bot.reply_to(message, reply)


@bot.message_handler(func=lambda message: True)
async def repeat_repeat_repeat(message):
    if message.text.endswith("!") or message.text.endswith("！"):
        if len(message.text) < 30:
            if "\n" in message.text:
                reply = (
                    re.sub(r"[!！]+", "！", message.text)
                    + "\n"
                    + re.sub(r"[!！]+", "！", message.text)
                    + "\n"
                    + re.sub(r"[!！]+", "！", message.text)
                )

            else:
                reply = re.sub(r"[!！]+", "！", message.text) * 3
            await bot.reply_to(message, reply)


async def jrrp_text_init(nub_in):
    nub = int(nub_in)
    if nub == 100:
        return "今天的人品是：" + str(nub_in) + "\n" + "100 人品好评!!!"
    elif nub >= 90:
        return "今天的人品是：" + str(nub_in) + "\n" + "今天的人品非常不错呢"
    elif nub >= 70:
        return "今天的人品是：" + str(nub_in) + "\n" + "哇,人品还挺好的!"
    elif nub >= 60:
        return "今天的人品是：" + str(nub_in) + "\n" + "今天是 非常¿ 不错的一天呢!"
    elif nub > 50:
        return "今天的人品是：" + str(nub_in) + "\n" + "你的人品还不错呢"
    elif nub == 50:
        return "今天的人品是：" + str(nub_in) + "\n" + "五五开！"
    elif nub >= 40:
        return "今天的人品是：" + str(nub_in) + "\n" + f"还好还好只有 {nub}"
    elif nub >= 20:
        return "今天的人品是：" + str(nub_in) + "\n" + f"{nub} 这数字太....要命了"
    elif nub >= 0:
        return "今天的人品是：" + str(nub_in) + "\n" + "抽大奖¿"


async def from_input_get_score(user_id):
    today_date = int(await when_is_now_in_utc_plus_8())
    random.seed(today_date + int(user_id))
    score = random.randint(0, 100)

    # 给那些运气烂的家伙
    if score < 35:
        score += random.randint(23, 31)

    if today_date in JRRP_GOOD_DAYS:
        score += 100

    return score


async def when_is_now_in_utc_plus_8():
    # 获取当前时间
    current_time = datetime.utcnow()

    # 将当前时间调整为东八区时间
    eastern_eight_time = current_time + timedelta(hours=8)

    # 提取年月日
    year = eastern_eight_time.year
    month = eastern_eight_time.month
    day = eastern_eight_time.day

    return int(str(year) + str(month) + str(day))


if __name__ == "__main__":
    asyncio.run(bot.polling())
