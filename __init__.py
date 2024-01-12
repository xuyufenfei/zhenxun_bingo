from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.params import CommandArg
import openai

# 插件的基本配置
__zx_plugin_name__ = "bing ai"
__plugin_usage__ = """
usage：
    问答：sydney+问题
""".strip()
__plugin_des__ = "bing"
__plugin_cmd__ = ["sydney"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.3
__plugin_author__ = "xuyufenfei"
__plugin_settings__ = {"level": 5, "admin_level": 2, "default_status": True, "limit_superuser": False, "cmd": __plugin_cmd__}
__plugin_cd_limit__ = {"cd": 10, "limit_type": "group", "rst": "请求过快！"}

# 创建命令处理器
ai = on_command("sydney", priority=5, block=True)

@ai.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    try:
        msg = arg.extract_plain_text().strip()

        # 设置 OpenAI API 密钥和自定义服务 URL
        openai.api_key = "your-real-api-key"  # 替换为你的实际 API 密钥
        openai.api_base = "https://copilot.github1s.tk"  # 你的自定义服务 URL

        # 创建聊天会话
        chat_response = openai.ChatCompletion.create(
            model="Creative", 
            messages=[{"role": "user", "content": msg}]
        )

        # 提取 ChatGPT 的回复
        response_text = chat_response.choices[0].message.content

    except Exception as e:
        response_text = f"发生错误：{e}"

    # 发送回复给用户
    await ai.send(response_text, at_sender=True)
