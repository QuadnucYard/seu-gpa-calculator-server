import pathlib
import tomllib

import uvicorn
from fastapi import Depends, FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse  # 响应html
from fastapi.security import OAuth2PasswordRequestForm

import api
from users import User, user_login, user_logout, get_current_user

cfg = tomllib.loads(pathlib.Path("config.toml").read_text())

app = FastAPI()
BASE_DIR = pathlib.Path(".").absolute()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/")
def main():
    html_content = pathlib.Path(BASE_DIR / "static" / "index.html").read_text()
    return HTMLResponse(content=html_content)


@app.get('/test')
def test():
    return 'fastapi + vue3'


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


@app.get("/auth")
async def auth(user: User = Depends(get_current_user)):
    ...


@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user: User = Depends(get_current_user)):
    if user:
        user.form["password"] = form_data.password
        re_login = await api.login(user.session, user.form)
        user.data = re_login
        return re_login


@app.post("/auth/logout")
async def logout(user: User = Depends(get_current_user)):
    if user:
        await user_logout(user.token)


@app.get("/user/me")
async def get_user(user: User = Depends(get_current_user)):
    return user.data if user else None


@app.get("/query")
async def query(user: User = Depends(get_current_user)):
    if user:
        return await api.get_grade_list(user.session)


if __name__ == "__main__":
    uvicorn.run(  # type: ignore
        app="main:app",
        host=cfg["app"]["host"],
        port=cfg["app"]["port"],
        reload=True,
    )
