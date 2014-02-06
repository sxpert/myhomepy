#!/usr/bin/python2.7 -3
#-*- coding: utf-8 -*-

import time
import re
import myOpenLayer1

#--------------------------------------------------------------------------------------------------
#
#
#

class tempCheck (object):
	def __init__ (self, socket, sensor, delay, loop) :
		self.address = socket.address
		self.port = socket.port
		self.passwd = socket.passwd
		self.sensor = sensor
		self.delay = delay
		self.loop = loop
		self.sock = None
		self.set_timeout()

	def set_timeout (self) :
		ts = time.time()
		if self.sock is None : 
			# calculate timer so that it falls on an entire self.delay value
			t = time.time()
			t = t - ( t % self.delay ) + self.delay
			ts = t
			#ts+=1
		else :
			ts += self.delay
		self.loop.add_timer (ts,self.check_temperature)

	def check_temperature (self) :
		self.sock = myOpenLayer1.OwnSocket(self.address, self.port, self.passwd, myOpenLayer1.OwnSocket.COMMAND)
		self.sock.set_ready_callback(self.send_command)
		self.sock.set_data_callback(self.get_data)
		self.loop.add_socket(self.sock)
		
	def send_command (self) :
		if self.sock is not None :
			c = '*#4*'+self.sensor+'*0##' 
			self.sock.log ('Getting temperature value from sensor '+self.sensor)
			self.sock.sock.send (c)

	def get_data (self, data) :
		if data == self.sock.ACK :
			self.sock.log('TempCheck: Closing socket');
			self.loop.remove_socket(self.sock)
			self.sock.close()
			self.sock = None
			return
		p = re.compile('\*#4\*(\d{1,3})\*0\*(\d{4})##')
		m = p.match(data)
		if m is not None :
			sensor = m.group(1)
			temp = float(m.group(2))/10 
			self.sock.log ('Sensor '+sensor+' reports '+str(temp)+'°C')
		else :
			self.sock.log ('Can\'t understand packet : '+data)
		self.set_timeout()
			

if __name__ == '__main__' :
	import config
	system_loop = myOpenLayer1.MainLoop(myOpenLayer1.system_logger)
	s = myOpenLayer1.OwnSocket(config.host,config.port,config.password,myOpenLayer1.ownSocket.MONITOR)
	system_loop.add_socket(s)
	t = tempCheck(s, '1', 5*60, system_loop)
	system_loop.run()
