from nonebot.log import logger
import aiohttp
from nonebot import get_plugin_config
from .Config import Config

bldm_config = get_plugin_config(Config)

try:
    if bldm_config.bililivedown == "on":
        allowedws = False 
        try:
            if ws := bldm_config.loadws:
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
        try:
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
        except aiohttp.client_exceptions.ClientConnectorError:
            logger.opt(colors=True).warning(
                f"<yellow>事件响应地址</yellow> <green>{url}</green> <red>连接被拒绝！</red>"
                )