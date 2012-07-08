#!/usr/bin/env python
# -*- coding: utf-8 -*-

class i64bits :

    def __init__ (self, value = 0) :
        import types

        self._value = ''

        if type(value) == types.InstanceType:
            if value.__class__.__name__ == self.__class__.__name__:
                self._value = value._value
                return
            else :
                print 'error, can\'t handle '+str(value.__class__)
                return

        if type(value) == types.StringType:
            if len(value) == 64 :
                # should check for only '0' and '1'
                self._value = value
                return
            else :
                print 'error length '+str(len(value))
                return None

        fillchar = '0'
        if (abs(value) == value) :
            # positive number
            self._value = bin(value)[2:]
        else :
            # negative number
            n = bin(~value)[2:]
            while len(n)>0:
                c = n[0]
                n = n[1:]
                if c == '0' :
                    c = '1'
                else :
                    c = '0'
                self._value += c
            fillchar = '1'
        # fill
        while len(self._value) < 64:
            self._value = fillchar + self._value

    def __lshift__ (self, nbbits) :
        # cut up the nbbits at the begining of the string
        n = self._value[nbbits:]
        # append nbbits '0'
        while len(n) < 64 :
            n += '0'
        return i64bits(n)

    def __rshift__ (self, nbbits) :
        n = self._value[0:(64-nbbits)]
        # prepend nbbits fillchars
        fillchar =  self._value[0]
        while len(n) < 64 :
            n = fillchar + n
        return i64bits(n)

    def __add__ (self, other) :
        n1 = self._value
        n2 = i64bits(other)._value

        i = 63
        c = 0
        v = ''
        while i>=0 :
            c1 = int(n1[i])
            c2 = int(n2[i])
            v1 = c1 ^ c2
            v = str(c ^ v1) + v
            c = (v1 & c) | (c1 & c2)
            i = i - 1
        return i64bits(v)

    def __and__ (self, other) :
        n1 = self._value
        n2 = i64bits(other)._value
        i = 63
        v = ''
        while i>=0 :
            c1 = int(n1[i])
            c2 = int(n2[i])
            v = str(c1 & c2) + v
            i = i - 1
        return i64bits(v)

    def __invert__ (self) :
        n = self._value
        i=0
        v=''
        while i < 64:
            if n[i]=='1':
                c = '0'
            else :
                c = '1'
            v += c
            i = i + 1
        return i64bits(v)

    def __hex__ (self) :
        n = self._value
        v = ''
        while len(n) > 0 :
            c = n[0:4]
            n = n[4:]
            v += hex(int(c,2))[2:]
        return v

    def __repr__ (self) :
        return '<i64bits '+self._value+'>'

    def __str__ (self) :
        return self._value

def calcConnPass (password, nonce) :
    m_1 = i64bits(0xFFFFFFFFL)
    m_8 = i64bits(0xFFFFFFF8L)
    m_16 = i64bits(0xFFFFFFF0L)
    m_128 = i64bits(0xFFFFFF80L)
    m_16777216 = i64bits(0XFF000000L)
    num = 0
    flag = True
    num1 = i64bits()
    num2 = i64bits()
    password = i64bits(password)

    while (True) :
        length = num < len(nonce)
        if not length :
            break
        c = nonce[num]
        num1 = num1 & m_1
        num2 = num2 & m_1
        print num1
        print num2
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
        num = num + 1
    num3 = num1 & m_1
    return num3

if __name__ == '__main__':
    import sys

    res = calcConnPass (long('12345'), '603356072')
    print 'result   '+str(res)
    print 'decimal  '+str(long(str(res),2))
    exp = i64bits(25280520)
    print 'expected '+str(exp)
    print 'decimal  '+str(long(str(exp),2))
    #print 'result   '+str(hex(calcConnPass (long('12345'), '410501656')))
    #print 'expected '+str(hex(u64bits(119537670)))
