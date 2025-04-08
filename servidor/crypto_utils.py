from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from crypto_utils import encrypt, decrypt, pad, unpad
from crypto_utils import CryptoUtils

KEY = get_random_bytes(16)

def pad(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt(data):
    cipher = AES.new(KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data))
    return cipher.iv + ct_bytes

def decrypt(enc):
    iv = enc[:16]
    ct = enc[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct))