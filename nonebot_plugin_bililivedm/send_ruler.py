from nonebot.log import logger
import aiohttp
from nonebot import get_plugin_config
from .Config import Config

try:
    if get_plugin_config(Config).bililivedown == "on":
        allowedws = False 
        try:
            if ws := get_plugin_config(Config).loadws:
                allowedws = ws
                logger.opt(colors=True).success(
                f"<yellow>事件响应地址</yellow> <green>loadws</green> : <blue>{ws}</blue> 已配置"
                )
            else:
                allowedws = False
                logger.opt(colors=True).warning(
                f"<yellow>事件响应地址</yellow> <green>loadws</green> <red>未被配置！</red>"
                )
        except AttributeError:
            allowedws = False
            logger.opt(colors=True).warning(
                f"<yellow>事件响应地址</yellow> <green>loadws</green> <red>未被配置！</red>"
                )
except AttributeError:
    pass


async def send_data(event, msg,type):
    url = allowedws
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            if hasattr(msg, 'price'):
                price = msg.price
            else:
                price = 0
            data = {"user_id": msg.uid, 
                    "nickname": f"{msg.uname}",
                    "message": f"{msg.msg}",
                    "room_id": event.room_id,
                    "type": type,
                    "price":price
                    }
            await ws.send_json(data)