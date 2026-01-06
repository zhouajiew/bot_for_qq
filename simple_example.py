# -*- coding: utf-8 -*-
import asyncio
import os
import random

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
# 引入C2CMessage
from botpy.message import C2CMessage

# 记得先创建一下配置文件config.yaml
# 格式如下注释
'''
appid: "AppID"
secret: "AppSecret"
'''
test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

async def main():
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    # client.run(appid=test_config["appid"], secret=test_config["secret"])

    # 建议这样启动机器人
    async with client as c:
        await c.start(appid=test_config["appid"], secret=test_config["secret"])

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    # 只能通过这种方式被动发送私聊消息(Bot单次回复的次数上限为4)
    async def on_c2c_message_create(self, message: C2CMessage):
        await message._api.post_c2c_message(
            openid=message.author.user_openid, # 用户的openid
            msg_type=0, msg_id=message.id,
            content=f"我收到了你的消息：{message.content}",
            # 如果想要发送多条消息记得额外设置一下msg_seq，因为msg_seq相同的话，会被去重导致消息发送失败
            # msg_seq=str(random.randint(1, 999999))
        )


if __name__ == "__main__":
    asyncio.run(main())

# pip install qq-botpy
