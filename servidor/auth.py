import json
import os
import hashlib


class AuthManager:
    USER_FILE = "servidor/users.json"

    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists(self.USER_FILE):
            return {}
        with open(self.USER_FILE, 'r') as f:
            return json.load(f)

    def save_users(self):
        with open(self.USER_FILE, 'w') as f:
            json.dump(self.users, f)

    def login_user(self, conn):
        login = conn.recv(1024).decode()
        senha = conn.recv(1024).decode()

        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        if login in self.users:
            if self.users[login] == senha_hash:
                conn.send(b"Autenticado com sucesso!")
            else:
                conn.send(b"Senha incorreta.")
                conn.close()
        else:
            self.users[login] = senha_hash
            self.save_users()
            conn.send(b"Usuario nao encontrado. Criando novo...\nAutenticado com sucesso!")

        return login
