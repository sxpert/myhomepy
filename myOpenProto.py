#!/usr/bin/env python
# -*- coding: utf-8 -*-

# system includes
import sys, select, socket, string
import datetime
# application includes
import myOpenPass

DEBUG  = True
openpass = '12345'
logfile	= 'myopenlog.log'

#------------------------------------------------------------------------------
#
# Exceptions definitions
# 

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

#------------------------------------------------------------------------------
#
# OpenWebNet packets
#

#----
# base class

class ownPacket (object) :
	def __init__ (self) :
		pass

#------------------------------------------------------------------------------
#
# system packets
#

#----
# Acknowledge packet

class ownAckPacket (ownPacket) :
	def __init__ (self, conn) :
		self.conn = conn

	def run (self) :
		if self.conn.state == self.conn.LOGGING:
			self.conn.state = self.conn.LOGGED
			self.conn.log('Login successful')

	def __str__ (self) :
		return 'ACK packet'

#----
# Negative Acknowledge packet

class ownNakPacket (ownPacket) :
	def __init__ (self, conn) :
		self.conn = conn

	def run (self):
		if self.conn.state == self.conn.LOGGING:
			self.conn.state = self.conn.FAILED
			self.conn.log('Login FAILED !')

	def __str__ (self):
		return 'NACK packet'

#----
# login request packet

class ownLoginRequest (ownPacket) :
	def __init__ (self, conn, openpass, nonce):
		self.conn = conn
		self.openpass = openpass
		self.nonce = nonce
		self.passwd = str(myOpenPass.ownCalcPass (self.openpass, self.nonce))

	def run (self) :
		pwdpacket = '*#'+self.passwd+'##'
		self.conn.log ('Logging in with password packet '+pwdpacket)
		self.conn.state = self.conn.LOGGING
		self.conn.sock.send(pwdpacket)

	def __str__ (self) : 
		return "login request ["+\
			"openpass='"+self.openpass+"' "+\
			"nonce='"+self.nonce+"' "+\
			"passwd='"+self.passwd+"']"

#------------------------------------------------------------------------------
#
# WHO = 1
# Light and automation
#

#----
# WHAT = 0
# turn something off

class ownAutomationOff (ownPacket) :
	def __init__ (self, device) :
		self.device = device
		
	def __str__ (self) :
		return self.device+' turned off'

#----
# WHAT = 1
# turn something on

class ownAutomationOn (ownPacket) :
	def __init__ (self, device) :
		self.device = device

	def __str__ (self):	
		return self.device+' turned on'

#----
# WHAT = 1000#
# automation event

class ownAutomationEvent (ownPacket) :
	def __init__ (self, eventinfo):
		self.eventinfo = eventinfo

	def __str__ (self):
		return 'automation event '+str(self.eventinfo)

#------------------------------------------------------------------------------
#
# WHO = 13
# Gateway related packets
# 

#----
# System time packet
# packet sent every 10 minutes by the Master clock device

class ownGatewayTime (ownPacket) :
	def __init__ (self, conn, timeval) :
		self.conn = conn
		self.hour = int(timeval[0])
		self.minute = int(timeval[1])
		self.second = int(timeval[2])
		tz = timeval[3]
		if tz[0] == '1' : 
			tz = '-'+tz[1:]
		else:
			tz = tz[1:]
		self.tz = int(tz)

	def run (self) :
		d = datetime.datetime.today()
		# should tests be done ?
		if True : 
			# check only when gateway reports between 00:00 and 00:20
			if not ((self.hour==0) and (self.minute<=20)):
				return
			# if time exactly the same, don't change anything
			if (d.hour==self.hour) and (d.minute==self.minute) and (d.second==self.second):	
				return
			# don't adjust for less than 5 seconds
			d1 = d.hour * 3600 + d.minute * 60 + d.second
			d2 = self.hour * 3600 + self.minute * 60 + self.second
			if abs(d1-d2) <=5 :
				return
		# update time if gateway reported time is wrong
		sock = self.conn
		if sock.mode == sock.MONITOR:
			sock = ownSocket(sock.address, sock.port, sock.COMMAND)
		sock.log('Time is wrong on gateway, updating time')
		while (sock.state is None) or (sock.state == sock.LOGGING) :
			m = sock.handleMessage()
			if 'run' in dir(m):
				m.run()
		# generate the time update packet
		tz = ''
		if abs(self.tz) == self.tz:
			tz += '0'
		else:
			tz += '1'
		tz += "%02d"%(abs(self.tz))
		dp = "*#13**#0*%02d*%02d*%02d*%s##"%(d.hour, d.minute, d.second, tz)
		sock.log('Updating time with packet \''+dp+'\'')	
		sock.sock.send (dp)
		m = sock.handleMessage()
		if m.__class__ == ownAckPacket:
			sock.log ('Time set successfully')
		sock.sock.send ("*#13**22##")
		m = sock.handleMessage()
		
	
	def __str__ (self) :
		return "Gateway Time : %02d:%02d:%02d UTC%+d"%(self.hour,self.minute,self.second,self.tz)

#----
# System date packet
# packet sent every 10 minutes by the Master clock device

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
	MODES = { COMMAND : 'CMD',
		  MONITOR : 'MON' }	
	LOGGING = 1
	LOGGED	= 2
	FAILED  = 3

	def __init__ (self,address, port, mode) :
		self.address = address
		self.port = port
		self.mode = mode
		self.buf = ''
		self.sock = None
		self.state = None

	def __del__ (self) :
		if not (self.sock is None):
			self.log ('Closing socket')
			self.sock.close()

	def log (self, msg):
		import datetime
		try :
			# generate datetime string
			d = datetime.datetime.today()
			ds = "%04d-%02d-%02d %02d:%02d:%02d"%(d.year,d.month,d.day,d.hour,d.minute,d.second)
			logmsg = ds+' ['+self.MODES[self.mode]+'] '+msg
			print logmsg
			lf = open(logfile,"a+")
			lf.write(logmsg+'\n')
			lf.close()
		except :
			pass
	
	def connect (self):
		self.sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
		try :
			self.sock.connect((self.address,self.port))
		except socket.error, e:
			self.sock = None
			self.log ("connexion error, sleeping some")
			return
		self.sock.setblocking(0)

		self.handleMessage()
		if self.mode == self.COMMAND :
			self.sock.send('*99*0##')
		elif self.mode == self.MONITOR :
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
				return ownNakPacket(self)
			if m == '1' : 
				return ownAckPacket(self)	
		elif who == 1:
			# automation
			return self.parseAutomation(normal, m, msg)
		elif who == 13:
			# gateway control
			return self.parseGateway(m, msg)
		else:	
			raise UnknownWho(who, msg)
	
	def parseAutomation (self, normal, m, msg) :
		if normal:
			v = m.split('*')
			p = v[0].find('#')
			if p == -1:
				v0 = int(v[0])
				if v0 == 0 :
					# off message
					return ownAutomationOff(v[1])
				elif v0 == 1 : 
					# on message
					return ownAutomationOn(v[1])
			else :
				v0 = v[0].split('#')
				if int(v0[0]) == 1000 :
					return ownAutomationEvent([v0[1],v[1]])
		raise UnknownPacket(msg)
	
	def parseGateway (self, m, msg) :
		if m[0] == '*' :
			m=m[1:]
			if m[0] == '#' :
				m=m[1:]
				v = m.split('*')
				val = int(v[0])
				if val == 0 :
					return ownGatewayTime(self, v[1:])
				elif val == 1 :
					return ownGatewayDate(v[1:])
				else :
					return UnknownPacket(msg)
		raise UnknownPacket(msg)

	def handleMessage (self) :
		if self.sock is None:
			self.connect()
		try :
			input, output, error = select.select([self.sock],[],[])
		except KeyboardInterrupt, e:
			self.log ("program exit")
			sys.exit(0)
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
