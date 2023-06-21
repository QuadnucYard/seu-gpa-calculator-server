from typing import Any, cast

import aiohttp
import orjson
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

login_url = "https://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal"


async def visit():
    ss = aiohttp.ClientSession(headers=headers)
    res = await ss.get(login_url)
    soup = BeautifulSoup(await res.text(), "lxml")
    attrs = soup.select('[tabid="01"] input[type="hidden"]')
    form = dict[str, str]()
    for k in attrs:
        if k.has_attr("name"):
            form[cast(str, k["name"])] = cast(str, k["value"])
        elif k.has_attr("id"):
            form[cast(str, k["id"])] = cast(str, k["value"])
    return ss, form


# 登录信息门户，返回登录后的session
async def login(ss: aiohttp.ClientSession, form: dict[str, Any]):
    # 登录认证
    await ss.post(login_url, data=form)
    # 登录ehall
    await ss.get("http://ehall.seu.edu.cn/login?service=http://ehall.seu.edu.cn/new/index.html")

    res = await ss.get("http://ehall.seu.edu.cn/jsonp/userDesktopInfo.json")
    json_res = await res.json(loads=orjson.loads)
    try:
        name = json_res["userName"]
        print(f"{name[0]}** 登陆成功！")
        return json_res
    except Exception:
        print("认证失败！")
        return None


async def get_grade_list(ss: aiohttp.ClientSession):
    print("get_grade_list")
    await ss.get("http://ehall.seu.edu.cn/appShow?appId=4768574631264620")
    res0 = await ss.post("http://ehall.seu.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do", data={"*searchMeta": 1})
    res = await ss.post("http://ehall.seu.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do")
    return {
        "model": (await res0.json(loads=orjson.loads))["searchMeta"],
        "data": (await res.json(loads=orjson.loads))["datas"]["xscjcx"],
    }
