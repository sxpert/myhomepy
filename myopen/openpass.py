#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

import sys

L_FFFFFFFF = 0xFFFFFFFF
L_FFFFFFF8 = 0xFFFFFFF8
L_FFFFFFF0 = 0xFFFFFFF0
L_FFFFFF80 = 0xFFFFFF80
L_FF000000 = 0xFF000000
L_00FF0000 = 0x00FF0000
L_0000FFFF = 0x0000FFFF
L_0000FF00 = 0x0000FF00
L_000000FF = 0x000000FF
ZERO = 0x0

def ownCalcPass (password, nonce) :
    flag = True    
    num1 = ZERO
    num2 = ZERO
    password = int(password)

    for c in nonce :
        num1 = num1 & L_FFFFFFFF
        num2 = num2 & L_FFFFFFFF
        if c == '1':
            length = not flag
            if not length :
                num2 = password
            num1 = num2 & L_FFFFFF80
            num1 = num1 >> 7
            num2 = num2 << 25
            num1 = num1 + num2
            flag = False
        elif c == '2':
            length = not flag
            if not length :
                num2 = password
            num1 = num2 & L_FFFFFFF0
            num1 = num1 >> 4
            num2 = num2 << 28
            num1 = num1 + num2
            flag = False
        elif c == '3':
            length = not flag
            if not length :
                num2 = password
            num1 = num2 & L_FFFFFFF8
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
            num1 = num2 & L_0000FF00
            num1 = num1 + (( num2 & L_000000FF ) << 24 )
            num1 = num1 + (( num2 & L_00FF0000 ) >> 16 )
            num2 = ( num2 & L_FF000000 ) >> 8
            num1 = num1 + num2
            flag = False
        elif c == '8':
            length = not flag
            if not length:
                num2 = password
            num1 = num2 & L_0000FFFF
            num1 = num1 << 16
            num1 = num1 + ( num2 >> 24 )
            num2 = num2 & L_00FF0000
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
    return num1 & L_FFFFFFFF

def test_passwd_calc(passwd, nonce, expected):
    res = ownCalcPass(passwd, nonce)
    m = passwd+' '+nonce+' '+str(res)+' '+str(expected)
    if res == int(expected) :
        print('PASS '+m)
    else :
        print('FAIL '+m)

if __name__ == '__main__':
    import sys

    test_passwd_calc('12345','603356072','25280520')
    test_passwd_calc('12345','410501656','119537670')
    test_passwd_calc('12345','630292165','119537670')
