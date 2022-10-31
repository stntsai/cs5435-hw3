import os
from cryptography.hazmat.primitives import hashes, padding, ciphers
from cryptography.hazmat.backends import default_backend
import base64
import binascii

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

def format_plaintext(is_admin, password):
    tmp = bytearray(str.encode(password))
    return bytes(bytearray((is_admin).to_bytes(1,"big")) + tmp)

def is_admin_cookie(decrypted_cookie):
    if len(decrypted_cookie) == 0:
        return False
    return decrypted_cookie[0] == 1

associated_data = b"some associated_data"

class Encryption(object):
    def __init__(self, in_key=None):
        self._backend = default_backend()
        self._block_size_bytes = int(ciphers.algorithms.AES.block_size/8)
        if in_key is None:
            self._key = os.urandom(self._block_size_bytes)
        else:
            self._key = in_key

    def encrypt(self, msg):
        iv = os.urandom(self._block_size_bytes)
        encryptor = Cipher(algorithms.AES(self._key), 
                           modes.GCM(iv),
                           self._backend).encryptor()

        ciphertext = encryptor.update(msg) + encryptor.finalize()
        return iv + ciphertext + encryptor.tag
    
    def decrypt(self, ctx):
        iv = ctx[:self._block_size_bytes]
        ciphertext = ctx[self._block_size_bytes:-self._block_size_bytes]
        tag = ctx[-self._block_size_bytes:]
        
        decryptor = Cipher(algorithms.AES(self._key),
                           modes.GCM(iv, tag),
                           self._backend).decryptor()      
         
        try:
            msg = decryptor.update(ciphertext) + decryptor.finalize()
            return msg  # Successful decryption
        except ValueError:
            return False  # Error!!

    
def test_encr_decr():
    encryption = Encryption()
    msg = b"secret test message"
    
    encr = encryption.encrypt(msg)
    decr = encryption.decrypt(encr)
    
    print("message decrypted =", decr)
        
if __name__=='__main__':
    test_encr_decr()
