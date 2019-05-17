# -*- coding: utf-8 -*-
import asyncio

import aiohttp_jinja2
from aiohttp import WSMsgType, web
from aiohttp_session import get_session

from ...decorators import login_required
from core.logger import LOG_DEBUG

class WebSocket(web.View):
    @login_required
    async def get(self):
        config = self.request.app['config']
        print('WEBSOCKET preparing')
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        config.log("WEBSOCKET: initialized with %s"%(str(ws._writer.transport.get_extra_info('peername'))), LOG_DEBUG)
        print('WEBSOCKET register')
        config.websocket_register(ws)

        async for msg in ws:
            print('WEBSOCKET', msg.type)
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    config.log("websocket closing %s"%(str(ws._writer.transport.get_extra_info('peername'))), LOG_DEBUG)
                    await ws.close()
                else:
                    print('WEBSOCKET', msg.data)
                    # do more stuff
            elif msg.type == WSMsgType.ERROR:
                print('WEBSOCKET disconnected with exception %s' % (str(ws.exception())))
        print('WEBSOCKET unregistering websocket %s' % (str(ws)))
        config.websocket_unregister(ws)
        return ws
