from nonebot.permission import Permission
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot import on_command
import requests
import json

saying = on_command("saying")

types = {'a':'动画',
          'b':'漫画',
          'c':'游戏',
          'd':'文学',
          'e':'原创',
          'f':'来自网络',
          'g':'其他',           'h':'影视',
          'i':'诗词',           'j':'网易云',
          'k':'哲学',           'l':'抖机灵'}

# e.g. {"id":6491,"uuid":"2fcd691a-ebb0-4cf3-b189-b991de5ee36d","hitokoto":"遗忘，也是种解脱：当人们为之逝去，活下来的为之蒙恨的时候。","type":"c","from":"«最后的老兵»，TNO启示录事件","from_who":"The New Order:Last Days of Europe","creator":"Forevercontinent","creator_uid":7134,"reviewer":6844,"commit_from":"web","created_at":"1599385727","length":29}

@saying.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    content=(requests.get("https://v1.hitokoto.cn/?encode=json")).json()
    # content=json.loads(content)
    print(content)

    result="【一言】"
    result+=content["hitokoto"]
    result+="\n来源："
    result+=content["from"]
    result+="\n作者："
    result+=content["creator"]
    result+="\n类型："
    result+=types[content["type"]]

    print(result)

    await saying.send(result)