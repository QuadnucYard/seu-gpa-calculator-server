from dataclasses import dataclass

import aiohttp
from fastapi import Depends

from auth import create_access_token as _create_access_token
from auth import oauth2_scheme


@dataclass
class User:
    token: str
    session: aiohttp.ClientSession
    form: dict[str, str]


users_db = dict[str, User]()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User | None:
    return users_db.get(token)


def create_access_token(username: str) -> str:
    return _create_access_token(data={"username": username})


async def user_login(username: str, session: aiohttp.ClientSession, form: dict[str, str]):
    access_token = create_access_token(username)
    users_db[access_token] = User(token=access_token, session=session, form=form)
    return access_token


async def user_logout(token: str):
    await users_db[token].session.close()
    del users_db[token]