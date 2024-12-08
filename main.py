# 使用 python3 main.py yourtoken 来启动，比如 python3 main.py 114514:ABCDEFGO_HIJKLMNOxE
from telebot.async_telebot import AsyncTeleBot
from datetime import datetime, timedelta
import asyncio
import random
import sys
import re

JRRP_GOOD_DAYS = []
TEMP_PLACEHOLDER = "TEMP_PLACEHOLDER"
bot = AsyncTeleBot(token=str(sys.argv[1]), parse_mode="HTML")


@bot.message_handler(commands=["jrrp"])
async def send_jrrp(message) -> None:
    score = await from_input_get_score(message.from_user.id)
    reply = await jrrp_text_init(score)
    await bot.reply_to(message, reply)


@bot.message_handler(func=lambda message: True)
async def repeat_repeat_repeat(message) -> None:
    if message.text.endswith("!") or message.text.endswith("！"):
        repeat_text = re.sub(r"[!！]+", "！", message.html_text)
        if "我" in repeat_text or "你" in repeat_text:
            repeat_text = repeat_text.replace("我", TEMP_PLACEHOLDER)
            repeat_text = repeat_text.replace("你", "我")
            repeat_text = repeat_text.replace(TEMP_PLACEHOLDER, "你")
        if "\n" in message.text:
            repeat_text = repeat_text + "\n" + repeat_text + "\n" + repeat_text
        else:
            repeat_text *= 3

        await bot.reply_to(message, repeat_text)


async def jrrp_text_init(nub_in) -> str:
    nub = int(nub_in)
    if nub == 100:
        return f"今天的人品是：{nub}\n人品超棒！🎉"
    elif nub >= 90:
        return f"今天的人品是：{nub}\n今天的人品非常不错呢！🤗"
    elif nub >= 70:
        return f"今天的人品是：{nub}\n哇，人品还挺好的！😊"
    elif nub >= 60:
        return f"今天的人品是：{nub}\n今天是 非常¿ 不错的一天呢！✨"
    elif nub > 50:
        return f"今天的人品是：{nub}\n你的人品还不错呢！🤔"
    elif nub == 50:
        return f"今天的人品是：{nub}\n五五开！😬"
    elif nub >= 40:
        return f"今天的人品是：{nub}\n还好还好有 {nub}😐"
    elif nub >= 20:
        return f"今天的人品是：{nub}\n{nub} 这数字太...要命了💀"
    elif nub >= 0:
        return f"今天的人品是：{nub}\n抽大奖¿🎁"


async def from_input_get_score(user_id) -> int:
    today_date = int(await when_is_now_in_utc_plus_8())
    random.seed(today_date + int(user_id))
    score = random.randint(0, 100)
    # 给那些运气烂的家伙
    if score < 35:
        score += random.randint(23, 31)
    if today_date in JRRP_GOOD_DAYS:
        score += 100
    return score


async def when_is_now_in_utc_plus_8() -> int:
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
