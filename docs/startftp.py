#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import myOpenProto as mo

if __name__ == '__main__':
	print "starting ftp"
	import config
	s = mo.ownSocket (config.host, config.password, config.port, mo.ownSocket.COMMAND)
	while (s.state is None) or (s.state == s.LOGGING) :
		m = s.handleMessage()
		if 'run' in dir(m):
			m.run()
	s.log ('starting ftp server')
	s.sock.send ('*#13**#31*0##')
	m = s.handleMessage()	
