import json
import os
import hashlib
import time
from crypto_utils import decrypt_aes, encrypt_aes

USER_FILE = "servidor/users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

def send_encrypted(conn, session_key, msg):
    conn.send(encrypt_aes(session_key, msg.encode()))

def recv_encrypted(conn, session_key):
    return decrypt_aes(session_key, conn.recv(4096)).decode()

def login_user(conn, session_key):
    users = load_users()

    login = recv_encrypted(conn, session_key)
    senha = recv_encrypted(conn, session_key)

    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    if login in users:
        if users[login] == senha_hash:
            send_encrypted(conn, session_key, "\nAutenticado com sucesso!")
        else:
            send_encrypted(conn, session_key, "\nSenha incorreta.")
            time.sleep(0.1)
            conn.close()
    else:
        users[login] = senha_hash
        save_users(users)
        send_encrypted(conn, session_key, "\nUsuario nao encontrado. Criando novo...\nAutenticado com sucesso!")

    return login
