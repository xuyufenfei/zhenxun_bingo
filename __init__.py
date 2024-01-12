from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.params import CommandArg
import openai

# 插件的基本配置
__zx_plugin_name__ = "bing ai"
__plugin_usage__ = """
usage：
    问答：sydney+问题
    清除历史：sydney+清除历史
""".strip()
__plugin_des__ = "bing"
__plugin_cmd__ = ["sydney", "clear_history"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.3
__plugin_author__ = "xuyufenfei"
__plugin_settings__ = {"level": 5, "admin_level": 2, "default_status": True, "limit_superuser": False, "cmd": __plugin_cmd__}
__plugin_cd_limit__ = {"cd": 10, "limit_type": "group", "rst": "请求过快！"}

# 创建命令处理器
ai = on_command("sydney", priority=5, block=True)
clear_history = on_command("sydney 清除历史", priority=5, block=True)

# 会话历史存储
session_histories = {}

@ai.handle()
async def handle_chat(event: MessageEvent, arg: Message = CommandArg()):
    user_id = event.get_user_id()
    session_history = session_histories.get(user_id, [])

    try:
        msg = arg.extract_plain_text().strip()
        session_history.append({"role": "user", "content": msg})

        openai.api_key = "dummy"  
        openai.api_base = "https://copilot.github1s.tk"  # 替换为你的bingo网址，请勿带有后缀

        # 更新 OpenAI 聊天会话
        chat_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=session_history
        )

        response_text = chat_response.choices[0].message.content
        session_history.append({"role": "system", "content": response_text})

        # 管理会话历史长度
        if len(session_history) > 20:
            session_history = session_history[-20:]
            response_text = "达到上限，清除记录"
        session_histories[user_id] = session_history
    except Exception as e:
        response_text = f"发生错误：{e}"

    await ai.send(response_text, at_sender=True)

@clear_history.handle()
async def handle_clear_history(event: MessageEvent):
    user_id = event.get_user_id()

    # 清除指定用户的会话历史
    session_histories[user_id] = []

    # 向用户发送确认消息
    await clear_history.send("会话历史已清除", at_sender=True)
