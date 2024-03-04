# TelegramBotRua

也许是多功能的？不确定。

使用时最好关闭隐私模式。

今日人品灵感来源于[此](https://github.com/GooGuJiang/Gugumoe-bot)。

重复重复重复灵感来源于[此](https://github.com/rikumi/tietie-bot/blob/main/src/commands/repeat.ts)。

## 直接运行

### 依赖

```bash
pip install pyTelegramBotAPI aiohttp
```

### 运行

```bash
python3 main.py <Your Token Here>
```

## 使用 Docker

### 拉取

```bash
docker pull ghcr.io/cat0x1f/telegrambotrua:main
```

### Docker 运行

```bash
docker run --env BOTTOKEN=yourtoken ghcr.io/cat0x1f/telegrambotrua:main
```

其中的 `yourtoken` 为从 @BotFather 获取的令牌。
