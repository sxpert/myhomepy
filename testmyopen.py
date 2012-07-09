#!/usr/bin/env python

import socket, string

DEBUG  = True

class InvalidConnectionType (Exception):
	def __init__ (self):
		pass

class InvalidPacket (Exception):
	def __init__ (self, packet):
		self._packet = packet
	def __str__ (self):
		return self._packet

class UnknownPacket (Exception):
	def __init__ (self, packet):
		self._packet = packet
	def __str__ (self):
		return self._packet

class UnknownWho (Exception) :
	def __init__ (self, who, packet):
		self._who = who
		self._packet = packet
	def __str__ (self):
		return 'who = '+str(self._who)+' \''+self._packet+'\''

class ownPacket (object) :
	def __init__ (self) :
		pass

class ownAckPacket (ownPacket) :
	def __init__ (self) :
		pass
	def __str__ (self) :
		return 'ACK packet'

class ownNakPacket (ownPacket) :
	def __init__ (self) :
		pass
	def __str__ (self):
		return 'NACK packet'

#------------------------------------------------------------------------------

COMMAND = 1
MONITOR = 2

class ownSocket (object) :
	def __init__ (self,address, port, socktype) :
		self.address = address
		self.port = port
		self.socktype = socktype
		self.buf = ''
		self.sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.address,self.port))

		self.handleMessage()
		if self.socktype==COMMAND:
			self.sock.send('*99*0##')
		elif self.socktype==MONITOR:
			self.sock.send('*99*1##')
		else:
			raise InvalidConnectionType 	
 
	def parseMessage (self, msg) :
		m = msg
	
		if m[0]!='*' : 
			raise InvalidPacket(msg)
		m = m[1:]
		normal=True
		if m[0] == '#':
			normal = False
			m = m[1:]
		# find WHO
		p = m.find('*')
		if p == -1:
			raise UnknownPacket(msg)
		who = m[0:p]
		m = m[(p+1):]
		if len(who) == 0:
			who = None
		else :
			# check if all chars of who are digits
			for c in who :
				if c not in string.digits:
					raise InvalidPacket(msg)
			who = int(who)
		if who is None: 
			if m == '0' :
				return ownNackPacket()
			if m == '1' : 
				return ownAckPacket()	
		elif who == 13:
			# gateway control
			return self.parseGateway(m, msg)
		else:	
			raise UnknownWho(who, msg)
	
	def parseGateway(self, m, msg) :
		print 'Gateway message '+m
		return None

	def handleMessage (self) :
		p = self.buf.find('##')
		if p==-1 :
			msg = self.sock.recv(1024)
			self.buf+=msg
			p = self.buf.find('##')
			if p==-1 : 
				return
		msg = self.buf[0:p]
		self.buf = self.buf[(p+2):]
		m = None
		try :
			m = self.parseMessage(msg)
		except UnknownPacket, e:
			msg = 'Unknown Packet \'' + str(e) + '\''
		except UnknownWho, e:
			msg = 'Unknown WHO value [' + str(e) + ']'	
		else:
			msg = str(m) 
		print '[MON] '+msg
		return m

if __name__ == '__main__':
	s = ownSocket('f454',20000,MONITOR)
	while True:
		s.handleMessage()
