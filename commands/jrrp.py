import random
from datetime import datetime, timedelta, timezone


def main(user_id: int) -> str:
    score = from_input_get_score(user_id)
    if score == 100:
        return f"今天的人品是: {score}\n人品超棒!🎉"
    elif score >= 90:
        return f"今天的人品是: {score}\n今天的人品非常不错呢!🤗"
    elif score >= 70:
        return f"今天的人品是: {score}\n哇，人品还挺好的!😊"
    elif score >= 60:
        return f"今天的人品是: {score}\n今天是 非常¿ 不错的一天呢!✨"
    elif score > 50:
        return f"今天的人品是: {score}\n你的人品还不错呢!🤔"
    elif score == 50:
        return f"今天的人品是: {score}\n五五开!😬"
    elif score >= 40:
        return f"今天的人品是: {score}\n还好还好有 {score}😐"
    elif score >= 20:
        return f"今天的人品是: {score}\n{score} 这数字太...要命了💀"
    elif score >= 0:
        return f"今天的人品是: {score}\n抽大奖¿🎁"


def from_input_get_score(user_id: int) -> int:
    today_date = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y%m%d")
    random.seed(int(today_date) + int(user_id))
    score = random.randint(0, 100)

    # 给那些运气烂的家伙
    if score < 30:
        score += random.randint(15, 30)
    return score
