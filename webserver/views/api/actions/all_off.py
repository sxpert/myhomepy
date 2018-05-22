# -*- coding: utf-8 -*-
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from ....decorators import login_required


class AllOff(web.View):
    @login_required
    async def get(self):
        session = await get_session(self.request)
        config = self.request.app['config']

        return web.Response(text="ok")
