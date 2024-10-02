from aiohttp import web

from app.views import login, signup, welcome


def setup_routes(app):
    app.router.add_get("/signup", signup)
    app.router.add_post("/signup", signup)
    app.router.add_get("/login", login)
    app.router.add_post("/login", login)
    app.router.add_get("/welcome", welcome)
