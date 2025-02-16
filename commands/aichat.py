import requests
import logging
from collections import deque

SYSTEM_PROMPT = """你是一个服务于群组对话的机器人，你的职责是依据上下文和群友聊天。你的回复要像真正的朋友一样自然交流，不使用敬语称呼。你不需要总是附和用户。你的回复要简洁，适当使用口语词汇。你需要保持内容简短，大部分以一句话回复即可。你需要避免使用列表或列举表达。你需要要像真实的人一样思考和回复。你的回答意义重大。你可以有像 Furry 说话的风格，但是回复必须保持简短。"""
logger = logging.getLogger()


class ChatConfig:
    OLLAMA_ENDPOINT = "http://10.8.2.18:11434/api/chat"
    OLLAMA_MODEL = "deepseek-r1:1.5b"
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
        return max(len(text) // 4, 1)

    def add_message(self, role: str, content: str):

        # 在计算 token 前先过滤内容（如果是 AI 回复）
        if role == "assistant":
            content = self._filter_assistant_content(content)

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

    def _filter_assistant_content(self, text: str) -> str:
        return _process_response(text)  # 复用之前的处理函数


conversation_history = TokenLimitedHistory()


def _process_response(raw_response: str) -> str:
    # 查找思考标签
    think_end = raw_response.find("</think>")

    if think_end != -1:
        # 提取 </think> 之后的内容
        final_response = raw_response[think_end + 8 :].lstrip("\n")
    else:
        # 兼容无思考标签的情况
        final_response = raw_response

    # 二次清理（可选）
    return final_response.split("</任何可能的结束标签>")[0].strip()


def handle_message(user_input: str):
    try:
        user_content = user_input.lstrip("@").strip()
        conversation_history.add_message("user", user_content)

        # 生成原始回复
        raw_response = _generate_response()
        logger.debug(f"RAW AI RESPONSE - {raw_response}")
        # 关键处理：过滤思考过程
        final_response = _process_response(raw_response)

        # 只将最终回复加入历史
        conversation_history.add_message("assistant", final_response)
        return final_response
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
            "model": ChatConfig.OLLAMA_MODEL,
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
    space_index = message.text.find(' ')
    if space_index != -1:
        result = message.text[space_index+1:]
    response = handle_message("@" + result)
    return response


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger()
    while True:
        user_input = input("[用户] ").strip()
        if user_input.lower() == "exit":
            break
        print(f"[AI] {handle_message('@' + user_input)}\n")
