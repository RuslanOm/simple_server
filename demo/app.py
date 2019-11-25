from aiohttp import web
from .routes import setup_routes
import aiohttp_jinja2
import jinja2
import asyncpgsa

from os import urandom
import aiohttp_auth

from aiohttp_auth import auth, autz
from aiohttp_auth.auth import auth_required
from aiohttp_auth.autz import autz_required
from aiohttp_auth.autz.policy import acl
from aiohttp_auth.permissions import Permission, Group
from .views.frontend import ACLAutzPolicy


async def create_app(config:dict):
    
    app = web.Application()
    app["config"] = config
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader("demo", "templates")
    )
    setup_routes(app)

    app.on_startup.append(on_start)
    app.on_cleanup.append(on_shotdown)

    return app


async def on_start(app):
    config = app["config"]
    app["db"] = await asyncpgsa.create_pool(dsn=config["database"])
    auth_policy = auth.CookieTktAuthentication(urandom(32), 60, include_ip=True)
    autz_policy = ACLAutzPolicy(app["db"])
    aiohttp_auth.setup(app, auth_policy, autz_policy)


async def on_shotdown(app):
    await app["db"].close()

