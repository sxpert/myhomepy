# -*- coding: utf-8 -*-
import asyncio

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session

from myopen.commands.asyncio_cmd_general_off import CmdGeneralOff

from ....decorators import login_required


class AllOff(web.View):
    @login_required
    async def get(self):
        # session = await get_session(self.request)
        config = self.request.app['config']
        system_id = self.request.query.get('system_id')
        if system_id.isdecimal():
            system_id = int(system_id)
            if system_id < len(config.systems):
                system = config.systems[system_id]

                request_done = asyncio.Event()

                def task_done_callback(logger=None):
                    logger('task_done_callback')
                    request_done.set()
                    logger('task_done_callback : event set, returning')

                system.push_task(CmdGeneralOff, callback=task_done_callback)

                await request_done.wait()
        else:
            # problem here
            print('there was a problem with system_id %s' % system_id)
        return web.Response(text="ok")
