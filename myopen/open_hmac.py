import hashlib

def ownCalcHmacSha2(password, nonce):
    """
    calculates the response to the SHA2 HMAC challenge
    """
    if len(nonce) == 128:
        # sha2 based hmac seems to be the only one useful
        ra = message_to_bytes(nonce)
        hmac_sha2 = None
        return hmac_sha2
    raise AttributeError

def message_to_bytes(message):
    """
    takes a numeric message and transforms it into bytes for
    consumption by the hashlib algorithms

    example:

    "10121502" => b'\xac\xf2'
    """
    message_bytes = b''
    while len(message) > 0:
        message_bytes += int(message[0:2]) * 16 + int(message[2:4])
        message = message[4:]

    print(message_bytes)
    return message_bytes

def bytes_to_message(message_bytes):
    """
    takes a bytes array and transforms it to a numeric message

    example: 

    b'\xf2\xac' => "10121502"
    """