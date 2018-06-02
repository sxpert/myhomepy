#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import asyncio
import base64
import os

import cryptography.fernet
from aiohttp import web

from . import decorators
from . import views

__all__ = ['WebServer']

# reloading a module :
#
# import inspect, importlib
# m = inspect.getmodule(index)
# print(m)
# importlib.reload(m)
# print(inspect.getmodule(index))


class WebServer(object):
    def __init__(self, address='127.0.0.1', port=8080,
                 site_data=None, loop=None, key=None, config=None):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.address = address
        self.port = port
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        if key is None:
            self.generate_new_key()
        else:
            self.set_key(key)
        self.site_data = site_data
        self.config = config

    def set_key(self, key):
        self.key = key
        self.b64_key = base64.urlsafe_b64decode(key)

    def generate_new_key(self):
        key = cryptography.fernet.Fernet.generate_key()
        self.set_key(key)

    # ========================================================================
    #
    # Reading and saving the configuration
    #
    # ========================================================================

    def loads(self, data):
        print(data)
        self.address = data.get('address', '127.0.0.1')
        self.port = data.get('port', 8080)
        k = data.get('session_key', None)
        if k is not None:
            key = k.encode('ascii')
            self.set_key(key)
        else:
            # create new key
            self.generate_new_key()
        return True

    def __to_json__(self):
        data = {}
        data['address'] = self.address
        data['port'] = self.port
        key = self.key.decode('ascii')
        data['session_key'] = key
        return data

    # ========================================================================
    #
    # Methods to setup and run the webserver
    #
    # ========================================================================

    def setup_sessions(self):
        from aiohttp_session import setup
        from aiohttp_session.cookie_storage import EncryptedCookieStorage
        self.sessions = EncryptedCookieStorage(self.b64_key)
        setup(self.app, self.sessions)
        print('sessions setup')

    def setup_jinja2(self):
        import aiohttp_jinja2
        import jinja2
        templates = os.path.join(self.path, 'templates')
        loader = jinja2.FileSystemLoader(templates)
        aiohttp_jinja2.setup(self.app, loader=loader)
        print('jinja2 setup')

    # self.web.register_routes(
    #     [
    #         ["^/$", website.ow_index.OW_index],
    #         ["^/API/ping$", website.ow_index.OW_ping],
    #         ["^/API/config$", website.ow_config.OW_config],
    #         ["^/API/ScanIds$", website.ow_scan_ids.OW_scan_ids],
    #         ["^/API/add_system(.*)$",
    #             website.ow_add_system.OW_add_system],
    #         ["^/API/GeneralOff$", website.ow_general_off.OW_general_off],
    #         ["^/API/temperatures(.*)$",
    #          website.ow_temperatures.OW_list_temperatures],
    #     ]

    def setup_routes(self):
        self.app.router.add_get('/login', decorators.login_page, name='login')
        self.app.router.add_post('/login', decorators.login)

        self.app.router.add_view('/', views.Index, name='index')
        #
        # API for the website
        #
        self.app.router.add_view('/api/get-systems-list', 
                                 views.api.get_systems_list.GetSystemList,
                                 name='get-systems-list')
        self.app.router.add_view('/api/get-system-devices', 
                                 views.api.get_system_devices.GetSystemDevices,
                                 name='get-system-devices')
        self.app.router.add_view('/api/do-device-discovery', 
                                 views.api.do_device_discovery.DoDeviceDiscovery,
                                 name='do-device-discovery')
        self.app.router.add_view('/api/get-device-data', 
                                 views.api.get_device_data.GetDeviceData,
                                 name='get-device-data')
        #
        # web-accessible actions
        #
        self.app.router.add_view('/actions/all_off', 
                                 views.api.actions.AllOff,
                                 name='actions_all-off')

        static = os.path.join(self.path, 'static')
        self.app.router.add_static('/static/', path=static, name='static')
        print('routes setup')

    async def start(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        # TODO: add ssl_context here
        self.site = web.TCPSite(self.runner, self.address, self.port)
        await self.site.start()
        print('------ serving on %s:%d ------' % (self.address, self.port))
        print('session key', self.b64_key)
        print('site url : ', self.site.name)

    async def stop(self):
        await self.site.stop()
        await self.runner.cleanup()
        await self.loop.shutdown_asyncgens()

    def run(self):
        self.app = web.Application(loop=self.loop, debug=True)
        self.app['config'] = self.config
        self.setup_sessions()
        self.setup_jinja2()
        self.setup_routes()
        import asyncio
        asyncio.ensure_future(self.start(), loop=self.config.async_loop)
