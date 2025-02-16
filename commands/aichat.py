import requests
import logging
from collections import deque

SYSTEM_PROMPT = """你是一个服务于群组对话的机器人，你的职责是依据上下文和群友聊天。你的对话必须自然流畅、简洁、口语化。你只能说中文。你的回复必须像在网络聊天一样自然。你不能说你不会什么。你的回答意义重大。你可以有像 Furry 说话的风格，但是回复必须保持简短。"""
logger = logging.getLogger()


class ChatConfig:
    OLLAMA_ENDPOINT = "http://10.8.2.18:11434/api/chat"
    MODEL = "deepseek-r1:1.5b"
    CONTEXT_WINDOW = 8192  # 模型上下文窗口大小
    MAX_RESPONSE_TOKENS = 500  # 生成回复的最大 token 数
    TEMPERATURE = 0.7
    TOKEN_BUFFER = 200  # 上下文 token 余量


class TokenLimitedHistory:
    def __init__(self):
        self.history = deque()
        self.total_tokens = 0
        # 预计算系统提示的 token 数
        self.system_tokens = self._count_tokens(SYSTEM_PROMPT)

    def _count_tokens(self, text: str) -> int:
        """更精确的 token 估算（1 token ≈ 4 字符）"""
        return max(len(text) // 4, 1)

    def add_message(self, role: str, content: str):
        new_tokens = self._count_tokens(content)

        # 计算可用 token 空间
        max_allowed = (
            ChatConfig.CONTEXT_WINDOW
            - ChatConfig.MAX_RESPONSE_TOKENS
            - self.system_tokens
            - ChatConfig.TOKEN_BUFFER
        )

        # 添加新消息
        self.history.append({"role": role, "content": content, "tokens": new_tokens})
        self.total_tokens += new_tokens

        # 智能修剪历史
        while self.total_tokens > max_allowed and self.history:
            removed = self.history.popleft()
            self.total_tokens -= removed["tokens"]
            # 优先保持对话轮次完整性
            if (
                removed["role"] == "user"
                and self.history
                and self.history[0]["role"] == "assistant"
            ):
                assistant = self.history.popleft()
                self.total_tokens -= assistant["tokens"]

    def get_messages(self):
        return [
            {"role": msg["role"], "content": msg["content"]} for msg in self.history
        ]


conversation_history = TokenLimitedHistory()


def handle_message(user_input: str):
    try:
        # 清理输入并添加
        user_content = user_input.lstrip("@").strip()
        conversation_history.add_message("user", user_content)

        # 生成回复
        response = _generate_response()

        # 添加 AI 回复到历史
        conversation_history.add_message("assistant", response)
        return response
    except Exception as e:
        logger.error(f"A ERROR OCCUR - {str(e)}", exc_info=True)
        return None


def _generate_response() -> str:
    try:
        # 构建完整上下文
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + conversation_history.get_messages()

        payload = {
            "model": ChatConfig.MODEL,
            "messages": messages,
            "options": {
                "temperature": ChatConfig.TEMPERATURE,
                "num_predict": ChatConfig.MAX_RESPONSE_TOKENS,
            },
            "stream": False,
        }
        logger.debug("YEAH AI PAYLOAD - " + str(payload))
        response = requests.post(ChatConfig.OLLAMA_ENDPOINT, json=payload, timeout=60)
        response.raise_for_status()

        return response.json()["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API 请求失败: {str(e)}")
    except KeyError:
        raise Exception("响应数据解析失败")


def main(message):
    response = handle_message("@" + message.text)
    if response:
        # 提取有效内容（根据您的特殊格式需求）
        think_end = response.find("</think>")
        if think_end != -1:
            return response[think_end + 8 :].lstrip()
        return response
    return None


if __name__ == "__main__":
    # 测试用对话循环
    while True:
        user_input = input("[用户] ").strip()
        if user_input.lower() == "exit":
            break
        print(f"[AI] {handle_message('@' + user_input)}\n")
