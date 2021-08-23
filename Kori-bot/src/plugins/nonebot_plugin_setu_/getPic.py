import nonebot
from httpx import AsyncClient
import aiofiles
import json
import glob
from nonebot.log import logger

local_proxy = nonebot.get_driver().config.local_proxy

async def getUrl(num:str):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    }
    req_url = "https://api.lolicon.app/setu?num="+num
    params = {
        "r18": 0,
        "size1200": 'true',
    }
    async with AsyncClient(proxies={"all://":None}) as client:
        res = await client.get(req_url,params=params,headers=head,timeout=10.0)
        try:
            res = json.loads(res.text)
            datas = res['data']
            await downPic(datas)
        except Exception as e:
            logger.error(e)
            logger.error(res.txt)


async def downPic(datas):
    head = {
        'referer': 'https://www.pixiv.net/',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    async with AsyncClient(proxies={"all://":local_proxy}) as client:
        for data in datas:
            url = data['url'].replace('i.pixiv.cat','i.pximg.net')
            response = await client.get(url=url,headers=head,timeout=10.0)
            index = len(glob.glob('./loliconImages/*.jpg'))
            img_path = 'loliconImages/' + str(index) + '.jpg'
            async with aiofiles.open(img_path, 'wb') as f:
                try:
                    await f.write(response.content)
                except TimeoutError:
                    pass