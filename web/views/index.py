# -*- coding: utf-8 -*-
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from decorators import *


class index(web.View):
    @login_required
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        session = await get_session(self.request)
        data = {
            'test_value': 42,
            'session': session
        }
        return data
