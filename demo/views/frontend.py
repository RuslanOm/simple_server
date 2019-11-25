import aiohttp
import json
from sqlalchemy import select, insert
from sqlalchemy.sql import text
from aiohttp_jinja2 import template
from .. import db

import aiohttp_auth

from aiohttp import web
from aiohttp_auth import auth, autz
from aiohttp_auth.auth import auth_required
from aiohttp_auth.autz import autz_required
from aiohttp_auth.autz.policy import acl
from aiohttp_auth.permissions import Permission, Group


# create an ACL authorization policy class
class ACLAutzPolicy(acl.AbstractACLAutzPolicy):
    """The concrete ACL authorization policy."""

    def __init__(self, db, context=None):
        super().__init__(context)
        self.db = db

    async def acl_groups(self, user_identity):
        async with self.db.acquire() as conn:
            query = select([db.users]).where(db.users.c.user_login == user_identity)
            result = await conn.fetch(query)
        if result:
            user = dict(result[0])
        else:
            user = None
        if user is None:
            return tuple()
        return user['groups']


@template("login.html")
async def login(request):
    user_identity = request.query['login']
    password = request.query['pass']

    async with request.app["db"].acquire() as conn:
        query = select([db.users]).where(db.users.c.user_login == user_identity)
        result = await conn.fetch(query)
        print(query, result)
    if result:
        data = dict(result[0])
        print(data)
        user_db, password_db = data["user_login"], data["pass"]
    else:
        user_db = None
        password_db = None

    if user_db and password == password_db:
        # remember user identity
        await auth.remember(request, user_identity)
        return data

    raise web.HTTPUnauthorized()


@auth_required
async def test(request):
    return web.Response(text="OK, you are logged")


@auth_required
async def logout(request):
    # forget user identity
    await auth.forget(request)
    return web.Response(text='Ok logout')


@template("index.html")
async def index(request):
    site_name = request.app["config"]["site_name"]
    return {"site_name": site_name}


@template("success_reg.html")
async def reg_user(request):
    try:
        data = await request.post()
        user = data['login']
        password = data['pass']
        comment = data['comment']

        async with request.app["db"].acquire() as conn:
            query = insert(db.users, values={"user_login": user, "comment": comment, "pass":password})
            print(query)
            await conn.fetch(query)

        response_obj = {"status": "success", "message": f"user created {user, password, comment}"}
        return response_obj
    except Exception as e:
        response_obj = {"status": "error", "message": f"user was not created, because {e}"}
        return response_obj


@template("error.html")
async def error(request):
    return {}







