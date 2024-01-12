from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.params import CommandArg
import openai

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

ai = on_command("sydney", priority=5, block=True)

@ai.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    try:
        msg = arg.extract_plain_text().strip()

        
        openai.api_key = "dummy" 
        openai.api_base = "https://copilot.github1s.tk"  # 替换成你部署完成后bingo的网址，请勿带有任何后缀，

        
        chat_response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[{"role": "user", "content": msg}]
        )

        # 提取 ChatGPT 的回复
        response_text = chat_response.choices[0].message.content

    except Exception as e:
        response_text = f"发生错误：{e}"

    # 发送回复给用户
    await ai.send(response_text, at_sender=True)
