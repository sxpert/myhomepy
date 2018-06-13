import asyncio
import logging
import sys

from config.config import Config
from myopen.asyncio_own_server import setup_OWN_server

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s: %(message)s',
        stream=sys.stderr,
    )
    loop = asyncio.get_event_loop()

    config = Config(None)

    setup_OWN_server(loop, '0.0.0.0', 20005, 
        config.systems[0].gateway.passwd, 
        config.systems[0].gateway.address, 
        config.systems[0].gateway.port)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()
