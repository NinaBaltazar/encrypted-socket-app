from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class CryptoUtils:
    def __init__(self):
        self.key = get_random_bytes(16)

    def pad(self, data):
        pad_len = 16 - len(data) % 16
        return data + bytes([pad_len]) * pad_len

    def unpad(self, data):
        pad_len = data[-1]
        return data[:-pad_len]

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(self.pad(data))
        return cipher.iv + ct_bytes

    def decrypt(self, enc):
        iv = enc[:16]
        ct = enc[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(ct))
