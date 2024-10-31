<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-SimpleToWrite

_✨ NoneBot 插件描述 ✨_

这是一个b站直播间弹幕监听插件
</div>

## 特别鸣谢

- [blivedm](https://github.com/xfgryujk/blivedm)项目的灵感来源以及部分实现的参考

## 📖 介绍

通过ws连接b站直播间，监听弹幕
具体使用方法和配置见下面的配置和使用例子

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot_plugin_bililivedm

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot_plugin_bililivedm
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_bililivedm"]

</details>

## ⚙️ 配置


请在.env文件里面这样配置

```bash
bililiveid=[b站直播间id] ##默认为[]
bilitoken=  ##这里填一个已登录账号的cookie的SESSDATA字段的值。不填也可以连接，但是收到弹幕的用户名会打码，UID会变成0
bililivedown=on ##是否开启b站直播间弹幕监听功能，on为开启，其他为关闭,默认为on
loadws= ##是否开启websocket功能，默认为ws://127.0.0.1:8000/bilidm

```

## 如何使用b站弹幕功能

在.env文件里面配置好之后，在你自己的py文件里面这样使用ws
以默认的ws://127.0.0.1:8000/bilidm为例

```bash
from aiohttp import web
import threading
import nonebot

async def websocket_handler(request):  ##千万别在这里使用async def websocket_handler(request,bot: Bot):不然会导致报错无法连接
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        reout = msg.data
        tes = json.loads(msg.data)
        send = tes["message"]
        (bot,) = nonebot.get_bots().values()
        await bot.send_private_msg(user_id=12335, message=send)

    return ws

def run_app():
    app = web.Application()
    app.router.add_get("/bilidm", websocket_handler)
    web.run_app(app, host="127.0.0.1", port=8000,print=None)

# 在主线程中创建一个子线程，防止卡住nb进程（或者用py单独运行个.py文件也行）
thread = threading.Thread(target=run_app)
thread.start()

```

参数说明
```bash
{
    "user_id": int, 
    "nickname": str,
    "message": str,
    "room_id": int,
    "type": str, ##仅支持普通消息（message）和醒目留言（super_chat）
    "price":int
}

```