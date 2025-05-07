import socket
import threading
from auth import login_user
from file_handler import handle_upload, handle_download, handle_list
from crypto_utils import (
    generate_ec_key_pair,
    export_public_key,
    import_public_key,
    derive_shared_key_ec as derive_shared_key,
    encrypt_aes,
    decrypt_aes
)

HOST = '127.0.0.1'
PORT = 9090

server_private, server_public = generate_ec_key_pair()

def send_encrypted(conn, session_key, msg):
    conn.send(encrypt_aes(session_key, msg.encode()))

def recv_encrypted(conn, session_key):
    data = conn.recv(4096)
    return decrypt_aes(session_key, data).decode()

def client_handler(conn, addr):
    print(f"Conexão recebida de {addr}")

    # Troca de chaves
    conn.send(export_public_key(server_public))
    client_pub_bytes = conn.recv(1024)
    client_public = import_public_key(client_pub_bytes)
    session_key = derive_shared_key(server_private, client_public)

    user = login_user(conn, session_key)

    # Envia só uma vez após login
    send_encrypted(conn, session_key, "\nLogin bem-sucedido!")

    while True:
        try:
            comando = recv_encrypted(conn, session_key).upper()
        except:
            break

        if comando == "UPLOAD":
            handle_upload(conn, user, session_key)
            send_encrypted(conn, session_key, "FIM OPERACAO")

        elif comando == "DOWNLOAD":
            handle_download(conn, session_key)
            send_encrypted(conn, session_key, "FIM OPERACAO")

        elif comando == "LIST":
            handle_list(conn, session_key)
            send_encrypted(conn, session_key, "FIM OPERACAO")

        elif comando == "SAIR":
            break

        else:
            send_encrypted(conn, session_key, "\nComando inválido.")
            send_encrypted(conn, session_key, "FIM OPERACAO")

    conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor ouvindo em {HOST}:{PORT}...")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=client_handler, args=(conn, addr), daemon=True).start()