import time 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crypto_utils import decrypt_aes, encrypt_aes

UPLOAD_DIR = "servidor/uploads"

def send_encrypted(conn, key, msg):
    conn.send(encrypt_aes(key, msg.encode()))

def recv_encrypted(conn, key):
    return decrypt_aes(key, conn.recv(4096)).decode()

def ensure_user_dir(user):
    user_path = os.path.join(UPLOAD_DIR, user)
    os.makedirs(user_path, exist_ok=True)
    return user_path

def handle_upload(conn, user, key):
    remetente = user
    nome = recv_encrypted(conn, key)
    send_encrypted(conn, key, "OK")

    size = int(recv_encrypted(conn, key))
    send_encrypted(conn, key, "READY")

    data = b""
    while len(data) < size:
        data += conn.recv(4096)

    plaintext = decrypt_aes(key, data)
    print("Conteúdo recebido (descriptografado):", plaintext.decode(errors="replace"))

    path = os.path.join(ensure_user_dir(remetente), nome)
    with open(path, 'wb') as f:
        f.write(plaintext)

    send_encrypted(conn, key, "\nArquivo salvo com sucesso.")
    time.sleep(0.05)
    send_encrypted(conn, key, "\nFIM OPERACAO")

def handle_download(conn, key):
    remetente = recv_encrypted(conn, key)
    nome = recv_encrypted(conn, key)
    path = os.path.join(ensure_user_dir(remetente), nome)

    if not os.path.exists(path):
        send_encrypted(conn, key, "\nNOT_FOUND")
        time.sleep(0.05)
        send_encrypted(conn, key, "\nFIM OPERACAO")
        return

    send_encrypted(conn, key, "OK")

    with open(path, 'rb') as f:
        plaintext = f.read()

    encrypted = encrypt_aes(key, plaintext)
    print("Conteúdo a ser enviado (criptografado):", encrypted[:64])
    
    send_encrypted(conn, key, str(len(encrypted)))
    ack = recv_encrypted(conn, key)
    if ack == "READY":
        conn.sendall(encrypted)

    time.sleep(0.05)
    send_encrypted(conn, key, "\nFIM OPERACAO")

def handle_list(conn, key):
    users = os.listdir(UPLOAD_DIR)
    response = ""
    for user in users:
        arquivos = os.listdir(os.path.join(UPLOAD_DIR, user))
        response += f"{user}: {', '.join(arquivos)}\n"

    send_encrypted(conn, key, response if response else "\nNenhum arquivo disponível.")
    time.sleep(0.05)
    send_encrypted(conn, key, "\nFIM OPERACAO")
