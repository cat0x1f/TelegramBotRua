import re
import random

marks = r"[啊阿呀吗嘛吧呢捏罢,.?!;，。？！；]"
re_clause = re.compile(r".+?\s*(?:[,.?!:;()，。？！：；（）]+|$)")
re_determiner = re.compile(r"^(啥|甚|什么|什麽|什麼|哪个|哪样|哪)")
re_conjunction = re.compile(
    r"^(虽然|但是|然而|只是|不过|至于|那么|因为|由于|因此|所以|如果|假如|只要|即使|要是)"
)
re_a_or_b = re.compile(
    rf"\s*(.*?)\s*([是有])\s*(.+?)\s*{marks}*还是\s*(.+?)(?:{marks}+|$)"
)
re_yes_or_no = re.compile(
    rf"\s*(.*?)\s*(是不是|是否|有没有|有木有|有无)\s*(.*?)(?:{marks}+|$)"
)
re_have_so = re.compile(rf"\s*(.*?)\s*(这么|那么|多么)\s*有\s*(.*?)(?:{marks}+|$)")
re_yes = re.compile(rf"\s*(.*?)\s*([是有])\s*(.+?)\s*{marks}*[吗嘛吧罢?!？！]+")
re_right1 = re.compile(rf"\s*(.*?)\s*(对不对|行不行)\s*(?:{marks}+|$)")
re_right2 = re.compile(
    rf"\s*(.*?)\s*((?:应该|我猜|其实|确实|大概)?[对是有行])\s*(.*?)\s*[吗嘛吧罢]+\s*[.?。？]*\s*$"
)
re_can1 = re.compile(rf"\s*(.*?)\s*(能不能|会不会)\s*(.*?)(?:{marks}+|$)")
re_can2 = re.compile(rf"\s*(.*?)\s*([能会][吗嘛吧罢])\s*[.?。？]*\s*$")

TypUnknown = 0
TypIs = 1
TypHave = 2
TypIsAB = 3
TypHaveAB = 4
TypIsYesNo = 5
TypHaveYesNo = 6
TypHaveSo = 7
TypRight = 8
TypCan = 9


class Token:
    def __init__(self, typ, sub="", obj="", ind="", word=""):
        self.typ = typ
        self.sub = sub
        self.obj = obj
        self.ind = ind
        self.word = word

    def __str__(self):
        if not self.obj:
            return f"sub={self.sub}"
        elif not self.ind:
            return f"sub={self.sub}, obj={self.obj}"
        return f"sub={self.sub}, obj={self.obj}, ind={self.ind}"

    
def explode(s):
    ps = re_clause.findall(s)
    for i in range(len(ps) - 1, 0, -1):
        if ps[i].startswith(("是", "有", "还是")):
            ps[i - 1] += ps[i]
            del ps[i]
    return [p.strip() for p in ps if p.strip()]


def rm_rec(s, pattern):
    while True:
        old = s
        s = pattern.sub("", s)
        if s == old:
            break
    return s


def type_of_is(i, s):
    if i == 0:
        return TypHaveAB if s == "有" else TypIsAB
    elif i == 1:
        return TypHaveYesNo if "有" in s else TypIsYesNo
    elif i == 2:
        return TypHave if "有" in s else TypIs
    return TypUnknown


def match_of_is(s):
    ps = explode(s)
    for p in reversed(ps):
        if ms := re_a_or_b.match(p):
            return Token(type_of_is(0, ms[2]), ms[1], ms[3], ms[4], ms[2])
        if ms := re_yes_or_no.match(p):
            return Token(type_of_is(1, ms[2]), ms[1], ms[3], word=ms[2])
        if ms := re_have_so.match(p):
            return Token(TypHaveSo, ms[1], ms[3], word=ms[2])
        if ms := re_yes.match(p):
            return Token(type_of_is(2, ms[2]), ms[1], ms[3], word=ms[2])
    return None


def is_tokenize(s):
    token = match_of_is(s)
    if not token:
        return None
    token.sub = rm_rec(token.sub, re_conjunction)
    token.obj = rm_rec(token.obj, re_determiner)
    token.ind = rm_rec(token.ind, re_determiner)
    return token if token.obj or token.ind else None


def match_of_right(s):
    ps = explode(s)
    for p in reversed(ps):
        if ms := re_right1.match(s):
            return Token(TypRight, ms[1], word=ms[2])
        if ms := re_right2.match(s):
            if ms[2].endswith(("是", "有")):
                return Token(TypRight, ms[1], ms[3], word=ms[2])
            elif not ms[3]:
                return Token(TypRight, ms[1], word=ms[2])
    return None


def right_tokenize(s):
    token = match_of_right(s)
    if not token:
        return None
    token.sub = rm_rec(token.sub, re_conjunction)
    return token if not re_determiner.match(token.sub) else None


def match_of_can(s):
    ps = explode(s)
    for p in reversed(ps):
        if ms := re_can1.match(p):
            return Token(TypCan, ms[1], ms[3], word=ms[2])
        if ms := re_can2.match(p):
            return Token(TypCan, ms[1], word=ms[2])
    return None


def can_tokenize(s):
    token = match_of_can(s)
    return token


def yes_sel(options, token):
    if random.random() > 0.9:
        return random.choice(options[random.randint(0, 1)])
    hash_index = hash(token.__str__()) % 2
    return random.choice(options[hash_index])


def handle_is(message):
    token = is_tokenize(message)
    if not token:
        return None

    if token.ind:  # 是/有X还是Y
        return yes_sel(
            [[token.ind, f"{token.ind}！"], [token.obj, f"{token.obj}！"]], token
        )

    responses = {
        1: [["是", "是的", "是呢"], ["不是", "不是啊", "不是哦"]],
        2: [["有", "有的", "有啊", "有喔"], ["没有", "没有啊", "没"]],
        5: [["是", "是的", "确实是"], ["不是", "不是哦", "应该不是"]],
        6: [["有", "确实有"], ["没有", "没啊", "并没有"]],
        7: [[f"确实有{token.obj}", f"是的，有{token.obj}"], ["没有那么", "没那么多"]],
    }

    if token.typ in responses:
        return yes_sel(responses[token.typ], token)

    return None


def handle_right(message):
    token = right_tokenize(message)
    if not token:
        return None

    responses = {
        "对": [["对", "对的", "没错", "对喔"], ["不对", "不对啊", "不对呢"]],
        "是": [["是", "是的", "是的呢"], ["不是", "不是哦"]],
        "有": [["有", "有的", "有喔", "有呢"], ["没有", "没啊", "没有喔"]],
        "行": [["行", "可以", "行的呢"], ["不行", "不可以"]],
    }

    if token.word[0] in responses:
        return yes_sel(responses[token.word[0]], token)
    return None


def handle_can(message):
    token = can_tokenize(message)
    if not token:
        return None

    responses = {
        "能": [
            ["能", "可以", "能的", "可以的"],
            ["不能", "不可以", "不能哦", "不可以"],
        ],
        "会": [["会", "可以做到", "会呢"], ["不会", "做不到"]],
    }

    if token.word[0] in responses:
        return yes_sel(responses[token.word[0]], token)
    return None
