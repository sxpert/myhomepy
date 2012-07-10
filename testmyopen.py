#!/usr/bin/env python

import select, socket, string
import myOpenPass

DEBUG  = True
openpass = '12345'

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

class ownLoginRequest (ownPacket) :
	def __init__ (self, conn, openpass, nonce):
		self.conn = conn
		self.openpass = openpass
		self.nonce = nonce
		self.passwd = str(myOpenPass.ownCalcPass (self.openpass, self.nonce))

	def run (self) :
		pwdpacket = '*#'+self.passwd+'##'
		self.conn.log ('Logging in with password packet '+pwdpacket)
		self.conn.sock.send(pwdpacket)

	def __str__ (self) : 
		return "login request ["+\
			"openpass='"+self.openpass+"' "+\
			"nonce='"+self.nonce+"' "+\
			"passwd='"+self.passwd+"']"

class ownGatewayTime (ownPacket) :
	def __init__ (self, timeval) :
		self.hour = int(timeval[0])
		self.minute = int(timeval[1])
		self.second = int(timeval[2])
		tz = timeval[3]
		if tz[0] == '1' : 
			tz = '-'+tz[1:]
		else:
			tz = tz[1:]
		self.tz = int(tz)

	def __str__ (self) :
		return "Gateway Time : %02d:%02d:%02d UTC%+d"%(self.hour,self.minute,self.second,self.tz)

class ownGatewayDate (ownPacket) :
	DAYS = [ 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'sunday' ]

	def __init__ (self, dateval) :
		self.weekday = int(dateval[0])
		self.day = int(dateval[1])
		self.month = int(dateval[2])
		self.year = int(dateval[3])

	def __str__ (self) :
		return "Gateway Date : %s, %04d-%02d-%02d"%(self.DAYS[self.weekday],self.year,self.month,self.day)

#------------------------------------------------------------------------------


class ownSocket (object) :
	COMMAND = 1
	MONITOR = 2
	TYPES = { COMMAND : 'CMD',
		  MONITOR : 'MON' }

	def __init__ (self,address, port, socktype) :
		self.address = address
		self.port = port
		self.socktype = socktype
		self.buf = ''
		self.sock = None

	def log (self, msg):
		print '['+self.TYPES[self.socktype]+'] '+msg
	
	def connect (self):
		self.sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.address,self.port))
		self.sock.setblocking(0)

		self.handleMessage()
		if self.socktype == self.COMMAND :
			self.sock.send('*99*0##')
		elif self.socktype == self.MONITOR :
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
			if not normal :
				login = True
				for c in m:
					if c not in string.digits:
						login = False
				if login :
					return ownLoginRequest (self, openpass, m)
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
		if m[0] == '*' :
			m=m[1:]
			if m[0] == '#' :
				m=m[1:]
				v = m.split('*')
				val = int(v[0])
				if val == 0 :
					return ownGatewayTime(v[1:])
				elif val == 1 :
					return ownGatewayDate(v[1:])
				else :
					return UnknownPacket(msg)
		raise UnknownPacket(msg)

	def handleMessage (self) :
		if self.sock is None:
			self.connect()
		input, output, error = select.select([self.sock],[],[])
		if len(input)==0 :
			self.log('strange, nothing to read')

		msg = self.sock.recv(1024)
		if len(msg)==0:
			# socket has died
			self.log('socket has died, reconnecting')	
			self.sock = None
			return None

		self.buf+=msg
		p = self.buf.find('##')
		if p==-1 : 
			return None
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
		self.log(msg)
		return m

if __name__ == '__main__':
	s = ownSocket ('f454', 20000, ownSocket.MONITOR)
	while True:
		m = s.handleMessage()
		if 'run' in dir(m):
			m.run()
