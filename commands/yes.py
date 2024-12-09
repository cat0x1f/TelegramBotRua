import re

# 定义标点符号
marks = r'[啊阿呀吗嘛吧呢捏罢,.?!;，。？！；]'

# 正则表达式定义
re_clause = re.compile(r'.+?\s*(?:[,.?!:;()，。？！：；（）]+|$)')
re_determiner = re.compile(r'^(啥|甚|什么|什麽|什麼|哪个|哪样|哪)')
re_conjunction = re.compile(r'^(虽然|但是|然而|只是|不过|至于|那么|因为|由于|因此|所以|如果|假如|只要|即使|要是)')
re_a_or_b = re.compile(rf'\s*(.*?)\s*([是有])\s*(.+?)\s*{marks}*还是\s*(.+?)(?:{marks}+|$)')
re_yes_or_no = re.compile(rf'\s*(.*?)\s*(是不是|是否|有没有|有木有|有无)\s*(.*?)(?:{marks}+|$)')
re_have_so = re.compile(rf'\s*(.*?)\s*(这么|那么|多么)\s*有\s*(.*?)(?:{marks}+|$)')
re_yes = re.compile(rf'\s*(.*?)\s*([是有])\s*(.+?)\s*{marks}*[吗嘛吧罢?!？！]+')
re_right1 = re.compile(rf'\s*(.*?)\s*(对不对|行不行)\s*(?:{marks}+|$)')
re_right2 = re.compile(rf'\s*(.*?)\s*((?:应该|我猜|其实|确实|大概)?[对是有行])\s*(.*?)\s*[吗嘛吧罢]+\s*[.?。？]*\s*$')
re_can1 = re.compile(rf'\s*(.*?)\s*(能不能|会不会)\s*(.*?)(?:{marks}+|$)')
re_can2 = re.compile(rf'\s*(.*?)\s*([能会][吗嘛吧罢])\s*[.?。？]*\s*$')

# 类型定义
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

# Token 类
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

# 分句函数
def explode(s):
    ps = re_clause.findall(s)
    for i in range(len(ps) - 1, 0, -1):
        if ps[i].startswith(("是", "有", "还是")):
            ps[i - 1] += ps[i]
            del ps[i]
    return [p.strip() for p in ps if p.strip()]

# 删除特定模式的递归函数
def rm_rec(s, pattern):
    while True:
        old = s
        s = pattern.sub("", s)
        if s == old:
            break
    return s

# 类型判断
def type_of_is(i, s):
    if i == 0:
        return TypHaveAB if s == "有" else TypIsAB
    elif i == 1:
        return TypHaveYesNo if "有" in s else TypIsYesNo
    elif i == 2:
        return TypHave if "有" in s else TypIs
    return TypUnknown

# 处理 "是/有" 类型的句子
def match_of_is(s):
    ps = explode(s)
    for p in reversed(ps):
        if (ms := re_a_or_b.match(p)):
            return Token(type_of_is(0, ms[2]), ms[1], ms[3], ms[4], ms[2])
        if (ms := re_yes_or_no.match(p)):
            return Token(type_of_is(1, ms[2]), ms[1], ms[3], word=ms[2])
        if (ms := re_have_so.match(p)):
            return Token(TypHaveSo, ms[1], ms[3], word=ms[2])
        if (ms := re_yes.match(p)):
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

# 处理 "对不对" 类型的句子
def match_of_right(s):
    ps = explode(s)
    for p in reversed(ps):
        if (ms := re_right1.match(s)):
            return Token(TypRight, ms[1], word=ms[2])
        if (ms := re_right2.match(s)):
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

# 处理 "能不能" 类型的句子
def match_of_can(s):
    ps = explode(s)
    for p in reversed(ps):
        if (ms := re_can1.match(p)):
            return Token(TypCan, ms[1], ms[3], word=ms[2])
        if (ms := re_can2.match(p)):
            return Token(TypCan, ms[1], word=ms[2])
    return None

def can_tokenize(s):
    token = match_of_can(s)
    return token

# 示例测试
if __name__ == "__main__":
    sentences = [
        "你是学生还是老师？",
        "这样做对不对？",
        "我们能不能一起去？",
    ]
    for sentence in sentences:
        print("Sentence:", sentence)
        print("Is Token:", is_tokenize(sentence))
        print("Right Token:", right_tokenize(sentence))
        print("Can Token:", can_tokenize(sentence))
