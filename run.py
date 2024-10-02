from aiohttp import web

from app import create_app
from app.models import init_db

if __name__ == "__main__":
    init_db()
    web.run_app(create_app(), port=8080)
