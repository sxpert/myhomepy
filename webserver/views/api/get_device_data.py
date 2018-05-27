# -*- coding: utf-8 -*-
import asyncio
import json

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session

import core.core_json_encoder as cje

from ...decorators import login_required


class GetDeviceData(web.View):
    @login_required
    async def get(self):
        # session = await get_session(self.request)
        config = self.request.app['config']
        systems = config.systems
        system_id = self.request.query.get('system_id')
        device_id = self.request.query.get('device_id')

        device = None
        if system_id is not None and system_id.isdecimal():
            system_id = int(system_id)
            if system_id in range(0, len(systems)):
                system = systems[system_id]
                devices = system.devices
                if device_id is not None and device_id in devices.keys():
                    device = devices[device_id]
        data = { 
            'ok': False
        }
        if device is not None:
            data['ok'] = True
            data['device'] = device.web_data
        return web.json_response(data)
