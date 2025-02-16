SYSTEM_PROMPT = """你是一个服务于群组对话的福瑞机器人，你的职责是依据上下文和群友聊天，同时保持对话自然流畅。你必须说话简洁，并且口语化。你只能说中文。你的回复必须像在网络聊天一样自然。你无论如何，都不能回复没有学会的内容。你的回答意义重大，如果你的回答让我满意，我将支付 200 美元小费。"""

# TODO
# system prompt
# 上下文不是用轮数而是最大的文本长度
import requests
import logging
from typing import List, Dict, Optional
logger = logging.getLogger()

# 配置参数
class ChatConfig:
    OLLAMA_ENDPOINT = "http://10.8.2.18:11434/api/chat"  # Ollama默认端点
    MODEL = "deepseek-r1:1.5b"  # 使用的本地模型名称
    MAX_HISTORY = 6  # 最大对话轮次（用户+AI为一轮）
    TEMPERATURE = 0.7  # 创造性参数
    MAX_TOKENS = 500  # 生成最大token数


conversation_history: List[Dict[str, str]] = []


def handle_message(user_input: str) -> Optional[str]:
    """
    处理用户输入并返回AI回复
    :param user_input: 用户输入（以@开头的消息）
    :return: AI回复内容或None
    """
    try:
        if not user_input.startswith("@"):
            return None

        # 清理输入并添加到历史
        user_content = user_input.lstrip("@").strip()
        _add_to_history("user", user_content)

        # 生成AI回复
        response = _generate_response()

        # 添加AI回复到历史
        _add_to_history("assistant", response)
        return response
    except Exception as e:
        logger.error("YEAH AI PROCESS FAIL")


def _add_to_history(role: str, content: str):
    """添加消息到历史记录并执行修剪"""
    conversation_history.append({"role": role, "content": content.strip()})
    _trim_history()


def _trim_history():
    """智能修剪历史记录"""
    # 删除最旧的完整对话轮次（用户+AI为一轮）
    while len(conversation_history) > ChatConfig.MAX_HISTORY * 2:
        # 寻找最早的连续用户消息
        for i in range(len(conversation_history)):
            if conversation_history[i]["role"] == "user":
                # 删除该用户消息及其之前的记录
                del conversation_history[: i + 1]
                return
        # 如果没有找到用户消息，退化到FIFO
        conversation_history.pop(0)


def _generate_response() -> str:
    """调用Ollama API生成回复"""
    try:
        conversation_history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        payload = {
            "model": ChatConfig.MODEL,
            "messages": conversation_history,
            "options": {
                "temperature": ChatConfig.TEMPERATURE,
                "num_predict": ChatConfig.MAX_TOKENS,
            },
            "stream": False,
        }
        logger.debug("YEAH AI PAYLOAD - "+ str(payload))
        response = requests.post(ChatConfig.OLLAMA_ENDPOINT, json=payload, timeout=60)
        response.raise_for_status()

        return response.json()["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API请求失败: {str(e)}")
    except KeyError:
        raise Exception("解析响应数据失败")
    except Exception as e:
        raise Exception(f"未知错误: {str(e)}")


def main(message):
    response = handle_message("@" + message.text)
    logger.debug("YEAH AI THINKING"+response)
    if response != None:
        index = response.find("</think>")
        if index != -1:
            # 获取 </think> 之后的内容
            content_after = response[index + len("</think>") :].lstrip('\n')
            return content_after


if __name__ == "__main__":
    while True:
        test_messages = input("[用户]")
        response = handle_message("@" + test_messages)
        print(f"[AI] {response}\n")
