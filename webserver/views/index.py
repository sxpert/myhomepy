# -*- coding: utf-8 -*-
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from ..decorators import login_required


class Index(web.View):
    @login_required
    @aiohttp_jinja2.template('index.html.j2')
    async def get(self):
        print('getting session')
        session = await get_session(self.request)
        print('session', session)
        config = self.request.app['config']
        print('config', config)
        data = {
            'test_value': 42,
            'systems': config.systems,
            'session': session
        }
        print('data for template', data)
        return data
