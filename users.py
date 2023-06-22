import asyncio
from dataclasses import dataclass
from typing import Any

import aiohttp
from fastapi import Depends

from auth import create_access_token as _create_access_token
from auth import oauth2_scheme


@dataclass
class User:
    token: str
    session: aiohttp.ClientSession
    form: dict[str, str]
    data: Any


users_db = dict[str, User]()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User | None:
    return users_db.get(token)


def create_access_token(username: str) -> str:
    return _create_access_token(data={"username": username})


async def delay_logout(token: str):
    await asyncio.sleep(3600)
    await user_logout(token)


async def user_login(username: str, session: aiohttp.ClientSession, form: dict[str, str]):
    access_token = create_access_token(username)
    users_db[access_token] = User(token=access_token, session=session, form=form, data=None)
    asyncio.ensure_future(delay_logout(access_token))
    return access_token


async def user_logout(token: str):
    if token not in users_db:
        return
    await users_db[token].session.close()
    del users_db[token]