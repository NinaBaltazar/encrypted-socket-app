import json
import os
import hashlib

USER_FILE = "servidor/users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

def login_user(conn):
    users = load_users()

    login = conn.recv(1024).decode()
    senha = conn.recv(1024).decode()

    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    if login in users:
        if users[login] == senha_hash:
            conn.send(b"Autenticado com sucesso!")
        else:
            conn.send(b"Senha incorreta.")
            conn.close()
    else:
        users[login] = senha_hash
        save_users(users)
        conn.send(b"Usuario nao encontrado. Criando novo...\nAutenticado com sucesso!")

    return login
