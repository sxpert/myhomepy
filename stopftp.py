#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import myOpenProto as mo

if __name__ == '__main__':
	print "stopping ftp"
	s = mo.ownSocket ("f454.sxpert.org", 20000, mo.ownSocket.COMMAND)
	while (s.state is None) or (s.state == s.LOGGING) :
		m = s.handleMessage()
		if 'run' in dir(m):
			m.run()
	s.log ('stopping ftp server')
	s.sock.send ('*#13**#33*0##')
	m = s.handleMessage()	
