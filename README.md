# TelegramBotRua

也许是多功能的？不确定。

使用时最好关闭隐私模式。

今日人品灵感来源于[此](https://github.com/GooGuJiang/Gugumoe-bot)。

重复重复重复灵感来源于[此](https://github.com/rikumi/tietie-bot/blob/main/src/commands/repeat.ts)。

## 使用

`<Your Token Here>` 为从 @BotFather 获取的令牌。

### 不使用 Docker

#### 依赖

```bash
pip install -r requirements.txt
```

#### 运行

注意，在同时使用环境变量和命令行传参的情况下，命令行传参的优先级高于环境变量。

##### 直接传参
```bash
python3 main.py <Your Token Here>
```

##### 使用环境变量
```bash
export BOTTOKEN='<Your Token Here>'
python3 main.py
```

### 使用 Docker

#### 拉取

```bash
docker pull ghcr.io/cat0x1f/telegrambotrua:main
```

#### 运行

```bash
docker run --env BOTTOKEN=<Your Token Here> ghcr.io/cat0x1f/telegrambotrua:main
```
