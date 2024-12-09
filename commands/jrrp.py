import random
from datetime import datetime, timedelta

JRRP_GOOD_DAYS = []


def main(user_id: int) -> str:
    score = from_input_get_score(user_id)
    if score == 100:
        return f"今天的人品是: {score}\n人品超棒! 🎉"
    elif score >= 90:
        return f"今天的人品是: {score}\n今天的人品非常不错呢! 🤗"
    elif score >= 70:
        return f"今天的人品是: {score}\n哇，人品还挺好的! 😊"
    elif score >= 60:
        return f"今天的人品是: {score}\n今天是 非常¿ 不错的一天呢! ✨"
    elif score > 50:
        return f"今天的人品是: {score}\n你的人品还不错呢! 🤔"
    elif score == 50:
        return f"今天的人品是: {score}\n五五开! 😬"
    elif score >= 40:
        return f"今天的人品是: {score}\n还好还好有 {score}😐"
    elif score >= 20:
        return f"今天的人品是: {score}\n{score} 这数字太...要命了💀"
    elif score >= 0:
        return f"今天的人品是: {score}\n抽大奖¿🎁"


def from_input_get_score(user_id: int) -> int:
    today_date = int(when_is_now_in_utc_plus_8())
    random.seed(today_date + int(user_id))
    score = random.randint(0, 100)
    # 给那些运气烂的家伙
    if score < 35:
        score += random.randint(23, 31)
    if today_date in JRRP_GOOD_DAYS:
        score += 100
    return score


def when_is_now_in_utc_plus_8() -> int:
    # 获取当前时间
    current_time = datetime.utcnow()
    # 将当前时间调整为东八区时间
    eastern_eight_time = current_time + timedelta(hours=8)
    # 提取年月日
    year = eastern_eight_time.year
    month = eastern_eight_time.month
    day = eastern_eight_time.day
    return int(str(year) + str(month) + str(day))
