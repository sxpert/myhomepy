# -*- coding: utf-8 -*-
import asyncio

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session

from ...decorators import login_required


class GetSystemDevices(web.View):
    @login_required
    async def get(self):
        # session = await get_session(self.request)
        config = self.request.app['config']
        systems = config.systems
        system_id = self.request.query.get('system_id')
        if isinstance(system_id, str) and system_id.isdecimal():
            system_id = int(system_id)
        system = systems[system_id]
        data = { 
            'ok': False
        }
        if system is not None:
            devices = []
            for hw_addr, device in system.devices.items():
                dev = {}
                dev['id'] = hw_addr
                dev['icon'] = device.icon

                devices.append(dev)
            data['ok'] = True
            data['devices'] = devices
        print(data)
        return web.json_response(data)
