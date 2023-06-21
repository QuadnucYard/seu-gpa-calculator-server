import os
import pathlib

import uvicorn
from fastapi import Depends, FastAPI, Form
from fastapi.responses import HTMLResponse  # 响应html
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

import api
from users import User, user_login, user_logout, get_current_user, users_db

app = FastAPI()
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# app.mount("/dist", StaticFiles(directory=os.path.join(BASE_DIR, 'fastapi/dist')), name="dist")
# app.mount("/assets", StaticFiles(directory=os.path.join(BASE_DIR, 'fastapi/dist/assets')), name="assets")


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/")
def main():
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'index.html')
    html_content = ''
    html_content = pathlib.Path(html_path).read_text()
    return HTMLResponse(content=html_content, status_code=200)


@app.get('/test')
def test():
    return 'fastapi + vue3'


class VisitModel(BaseModel):
    username: str


@app.post("/auth/visit")
async def visit(username: str = Form()):
    ss, form = await api.visit()
    form["username"] = username
    access_token = await user_login(username, ss, form)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "encrypt_salt": form["pwdDefaultEncryptSalt"],
    }


@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user: User = Depends(get_current_user)):
    if user:
        user.form["password"] = form_data.password
        return await api.login(user.session, user.form)


if __name__ == '__main__':
    uvicorn.run(  # type: ignore
        app='main:app',
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
"""
grant_type: password
username: 12345
password: 12345
"""
