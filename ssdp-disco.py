import asyncio
import socket
import struct
import sys

BROADCAST_PORT = 1900
BROADCAST_ADDR = "239.255.255.250"
#BROADCAST_ADDR = "ff0e::c"

class DiscoveryClientProtocol:
    def connection_made(self, transport):
        self.transport = transport
        sock = self.transport.get_extra_info('socket')
        group = socket.inet_aton(BROADCAST_ADDR)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        print('started')
        
    def datagram_received(self, data, addr):
        print("------------------------------------------------------------------------------")
        print(data.decode())

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()

loop = asyncio.get_event_loop()
#message = DISCOVERY_MESSAGE
connect = loop.create_datagram_endpoint(DiscoveryClientProtocol, local_addr=(BROADCAST_ADDR, BROADCAST_PORT,), family=socket.AF_INET)
transport, protocol = loop.run_until_complete(connect)
loop.run_forever()
transport.close()
loop.close()