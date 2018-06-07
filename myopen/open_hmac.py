import hashlib
import secrets

# this appears to be half-wrong in the docs...
a = '736F70653E'
b = '636F70653E'

def ownCalcHmacSha2(password, ra):
    """
    calculates the response to the SHA2 HMAC challenge
    returns (rb, hmac(ra, rb, a, b, kab), hmac(ra, rb, kab))
    """
    if len(ra) == 128:
        rax = message_to_hex(ra)
        rbx = secrets.token_hex(32)
        rb_msg = hex_to_message(rbx)
        kab = sha256_calc_kab(password)
        c_msg = sha256_calc_client_response(rax, rbx, kab)
        s_msg = sha256_calc_server_response(rax, rbx, kab)
        return (rb_msg, c_msg, s_msg) 
    raise AttributeError

def sha256_calc_kab(password):
    p = password.encode('ascii')
    m = hashlib.sha256()
    m.update(p)
    return m.hexdigest()

def sha256_calc_client_response(ra, rb, kab):
    m = hashlib.sha256()
    m.update(ra.encode('ascii'))
    m.update(rb.encode('ascii'))
    m.update(a.encode('ascii'))
    m.update(b.encode('ascii'))
    m.update(kab.encode('ascii'))
    return hex_to_message(m.hexdigest())

def sha256_calc_server_response(ra, rb, kab):
    m = hashlib.sha256()
    m.update(ra.encode('ascii'))
    m.update(rb.encode('ascii'))
    m.update(kab.encode('ascii'))
    return hex_to_message(m.hexdigest())
    
def message_to_hex(message):
    mb = ''
    while len(message) > 0:
        mb += '%x%x' % (int(message[0:2]), int(message[2:4]))
        message = message[4:]
    return mb

def hex_to_message(msg_nibbles):
    """
    takes a bytes array and transforms it to a numeric message

    example: 

    b'\xf2\xac' => "10121502"
    """
    message = ""
    for c in msg_nibbles:
        message += '%02d' % int(c, 16)
    return message

