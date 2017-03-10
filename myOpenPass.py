#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#


def ownCalcPass (password, nonce) :
    m_1 = 0xFFFFFFFFL
    m_8 = 0xFFFFFFF8L
    m_16 = 0xFFFFFFF0L
    m_128 = 0xFFFFFF80L
    m_16777216 = 0XFF000000L
    flag = True
    num1 = 0L
    num2 = 0L
    password = long(password)

    for c in nonce :
        num1 = num1 & m_1
        num2 = num2 & m_1
        if c == '1':
            length = not flag
            if not length :
                num2 = password
            num1 = num2 & m_128
            num1 = num1 >> 7
            num2 = num2 << 25
            num1 = num1 + num2
            flag = False
        elif c == '2':
            length = not flag
            if not length :
                num2 = password
            num1 = num2 & m_16
            num1 = num1 >> 4
            num2 = num2 << 28
            num1 = num1 + num2
            flag = False
        elif c == '3':
            length = not flag
            if not length :
                num2 = password
            num1 = num2 & m_8
            num1 = num1 >> 3
            num2 = num2 << 29
            num1 = num1 + num2
            flag = False
        elif c == '4':
            length = not flag
            if not length:
                num2 = password
            num1 = num2 << 1
            num2 = num2 >> 31
            num1 = num1 + num2
            flag = False
        elif c == '5':
            length = not flag
            if not length:
                num2 = password
            num1 = num2 << 5
            num2 = num2 >> 27
            num1 = num1 + num2
            flag = False
        elif c == '6':
            length = not flag
            if not length:
                num2 = password
            num1 = num2 << 12
            num2 = num2 >> 20
            num1 = num1 + num2
            flag = False
        elif c == '7':
            length = not flag
            if not length:
                num2 = password
            num1 = num2 & 0xFF00L
            num1 = num1 + (( num2 & 0xFFL ) << 24 )
            num1 = num1 + (( num2 & 0xFF0000L ) >> 16 )
            num2 = ( num2 & m_16777216 ) >> 8
            num1 = num1 + num2
            flag = False
        elif c == '8':
            length = not flag
            if not length:
                num2 = password
            num1 = num2 & 0xFFFFL
            num1 = num1 << 16
            num1 = num1 + ( num2 >> 24 )
            num2 = num2 & 0xFF0000L
            num2 = num2 >> 8
            num1 = num1 + num2
            flag = False
        elif c == '9':
            length = not flag
            if not length:
                num2 = password
            num1 = ~num2
            flag = False
        else :
            num1 = num2
        num2 = num1
    return num1 & m_1

def ownTestCalcPass (passwd, nonce, expected) :
	res = ownCalcPass(passwd, nonce)
	m = passwd+' '+nonce+' '+str(res)+' '+str(expected)
	if res == long(expected) :
		print 'PASS '+m
	else :
		print 'FAIL '+m

if __name__ == '__main__':
    import sys

    ownTestCalcPass('12345','603356072','25280520')
    ownTestCalcPass('12345','410501656','119537670')
    ownTestCalcPass('12345','630292165','119537670')
