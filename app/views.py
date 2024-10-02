import aiohttp_jinja2
from aiohttp import web
from pydantic import ValidationError
from .forms import SignupForm, LoginForm
from .utils import hash_password, verify_password
from app.config import SessionLocal
from app.models import User
from sqlalchemy.exc import IntegrityError


@aiohttp_jinja2.template("signup.html")
async def signup(request):
    session = SessionLocal()

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

        user = session.query(User).filter(User.username == username).first()
        if user:
            return {"errors": [{"msg": "Username already exists"}]}

        hashed_password = hash_password(password)
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return {"errors": [{"msg": "Username already exists"}]}
        return web.HTTPFound("/login")
    return {}


@aiohttp_jinja2.template("login.html")
async def login(request):
    session = SessionLocal()

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

        user = session.query(User).filter(User.username == username).first()

        if not user or not verify_password(user.password, password):
            return {"errors": [{"msg": "Invalid username or password"}]}

        return web.HTTPFound("/welcome")
    return {}


@aiohttp_jinja2.template('welcome.html')
async def welcome(request):
    return {}
