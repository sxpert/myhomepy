# -*- coding: utf-8 -*-
import asyncio

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session

from ...decorators import login_required


class GetSystemList(web.View):
    @login_required
    async def get(self):
        # session = await get_session(self.request)
        config = self.request.app['config']
        systems = config.systems
        data = []
        for system in systems:
            sd = {}
            sd['id'] = system.id
            sd['display_name'] = system.display_name
            gateway = system.gateway
            gw = {}
            gw['display_name'] = gateway.display_name
            gw['model'] = gateway.model
            sd['gateway'] = gw
            data.append(sd)
        return web.json_response(data)
