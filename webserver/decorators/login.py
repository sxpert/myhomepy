# -*- encoding: utf-8 -*-
from http import HTTPStatus

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session, new_session

__all__ = [
    'login_required', 'login_page', 'login'
]


DATABASE = [
    ('u', 'xxx'),
]


def login_required(fn):
    async def wrapped(req, *args, **kwargs):
        request = req
        if isinstance(req, web.View):
            request = req.request
        app = request.app
        router = app.router

        session = await get_session(request)

        if 'user_id' not in session:
            # TODO: check if we can find all that...
            session['_return_to'] = request.match_info.route.name
            return web.HTTPFound(router['login'].url_for())

        user_id = session['user_id']
        # actually load user from your database (e.g. with aiopg)
        user = DATABASE[user_id]
        app['user'] = user
        return await fn(req, *args, **kwargs)

    return wrapped


@aiohttp_jinja2.template('login.html')
async def login_page(request):
    return {}  # web.Response(content_type='text/html', text=tmpl)


async def login(request):
    router = request.app.router
    form = await request.post()
    user_signature = (form['name'], form['password'])

    # actually implement business logic to check user credentials
    try:
        user_id = DATABASE.index(user_signature)
        # Always use `new_session` during login to guard against
        # Session Fixation. See aiohttp-session#281
        session = await get_session(request)
        return_to = session['_return_to']
        return_to_url = '/'
        if return_to is not None:
            return_to_url = router[return_to].url_for()
        session = await new_session(request)
        session['user_id'] = user_id
        return web.HTTPFound(return_to_url)
    except ValueError:
        return web.Response(text='No such user', status=HTTPStatus.FORBIDDEN)
