from Crypto.Cipher import AES
import os

KEY_FILE = "servidor/key.bin"

def load_key():
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'wb') as f:
            f.write(os.urandom(16))
    with open(KEY_FILE, 'rb') as f:
        return f.read()

KEY = load_key()

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
