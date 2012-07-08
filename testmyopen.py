#!/usr/bin/env python

import socket, string

DEBUG  = True

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

def parse_message(msg) :
	m = msg
	
	if DEBUG :
		print '[DEBUG] '+m	

	if m[0]!='*' : 
		raise InvalidPacket(msg)
	m = m[1:]
	e = m[-2:]
	if e != '##' :
		raise InvalidPacket(msg)
	m = m[0:-2]
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
	else:	
		raise UnknownWho(who, msg)

def handle_message(s) :
	msg = s.recv(1024)
	try :
		m = parse_message(msg)
	except UnknownPacket, e:
		m = 'Unknown Packet \'' + str(e) + '\''
	except UnknownWho, e:
		m = 'Unknown WHO value [' + str(e) + ']'	
	print '[MON] '+str(m)

if __name__ == '__main__':
	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('f454',20000))
	handle_message(s)
	s.send('*99*1##')
	while True:
		handle_message(s)
