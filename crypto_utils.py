from Crypto.Cipher import AES, DES3, ChaCha20
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.asymmetric import ec, dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

BLOCK_SIZE = 16  # Para AES e 3DES

# -------------------------------
# Padding para AES e 3DES
# -------------------------------

def pad(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad_len]) * pad_len

def unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len]

# -------------------------------
# Algoritmos de Criptografia Simétrica
# -------------------------------

def encrypt_aes(key: bytes, data: bytes) -> bytes:
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b"AES" + iv + cipher.encrypt(pad(data))

def decrypt_aes(key: bytes, data: bytes) -> bytes:
    iv = data[3:19]
    ct = data[19:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct))

def encrypt_3des(key: bytes, data: bytes) -> bytes:
    key = key.ljust(24, b'0')[:24]
    iv = get_random_bytes(8)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    return b"3DS" + iv + cipher.encrypt(pad(data))

def decrypt_3des(key: bytes, data: bytes) -> bytes:
    key = key.ljust(24, b'0')[:24]
    iv = data[3:11]
    ct = data[11:]
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct))

def encrypt_chacha20(key: bytes, data: bytes) -> bytes:
    cipher = ChaCha20.new(key=key)
    return b"CHC" + cipher.nonce + cipher.encrypt(data)

def decrypt_chacha20(key: bytes, data: bytes) -> bytes:
    nonce = data[3:11]
    ct = data[11:]
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.decrypt(ct)

def encrypt_all(key: bytes, data: bytes) -> dict:
    return {
        'AES': encrypt_aes(key, data),
        '3DES': encrypt_3des(key, data),
        'ChaCha20': encrypt_chacha20(key, data)
    }

def decrypt_auto(key: bytes, data: bytes) -> bytes:
    prefix = data[:3]
    if prefix == b"AES":
        return decrypt_aes(key, data)
    elif prefix == b"3DS":
        return decrypt_3des(key, data)
    elif prefix == b"CHC":
        return decrypt_chacha20(key, data)
    else:
        raise ValueError("Algoritmo de criptografia não reconhecido")

# -------------------------------
# Troca de Chaves com ECC
# -------------------------------

def generate_ec_key_pair():
    private_key = ec.generate_private_key(ec.SECP256R1())
    return private_key, private_key.public_key()

def export_public_key(pub_key) -> bytes:
    return pub_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def import_public_key(pub_bytes: bytes):
    return serialization.load_pem_public_key(pub_bytes, backend=default_backend())

def derive_shared_key_ec(private_key, peer_public_key) -> bytes:
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'ec dh',
        backend=default_backend()
    ).derive(shared_secret)

# Alias para facilitar a importação
derive_shared_key = derive_shared_key_ec

# -------------------------------
# Troca de Chaves com DH
# -------------------------------

def generate_dh_parameters():
    return dh.generate_parameters(generator=2, key_size=2048)

def generate_dh_key_pair(parameters):
    private_key = parameters.generate_private_key()
    return private_key, private_key.public_key()

def export_dh_public_key(pub_key) -> bytes:
    return pub_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def import_dh_public_key(pub_bytes: bytes):
    return serialization.load_pem_public_key(pub_bytes, backend=default_backend())

def derive_shared_key_dh(private_key, peer_public_key) -> bytes:
    shared_secret = private_key.exchange(peer_public_key)
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'dh key',
        backend=default_backend()
    ).derive(shared_secret)
