import aiohttp_jinja2
import bcrypt
from aiohttp import web
from pydantic import BaseModel, Field, ValidationError

users = {}


class SignupForm(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


@aiohttp_jinja2.template("signup.html")
async def signup(request):
    if request.method == "POST":
        data = await request.post()

        try:
            form = SignupForm(
                username=data.get("username"), password=data.get("password")
            )
        except ValidationError as e:
            return {"errors": e.errors()}
        username = form.username
        password = form.password

        if username in users:
            return {"errors": [{"msg": "Username already exists"}]}
        users[username] = hash_password(password)
        return web.HTTPFound("/login")
    return {}


class LoginForm(BaseModel):
    username: str
    password: str


def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(
        provided_password.encode("utf-8"), stored_password.encode("utf-8")
    )


@aiohttp_jinja2.template("login.html")
async def login(request):
    if request.method == "POST":
        data = await request.post()

        try:
            form = LoginForm(
                username=data.get("username"), password=data.get("password")
            )
        except ValidationError as e:
            return {"errors": e.errors()}
        username = form.username
        password = form.password

        if username not in users or not verify_password(
            users[username], password
        ):
            return {"errors": [{"msg": "Invalid username or password"}]}
        return web.HTTPFound("/welcome")
    return {}


@aiohttp_jinja2.template('welcome.html')
async def welcome(request):
    return {}
