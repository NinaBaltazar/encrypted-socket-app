import socket
import threading
from auth import login_user
from file_handler import handle_upload, handle_download, handle_list

HOST = '127.0.0.1'
PORT = 9091

def handle_client(conn, addr):
    print(f"Conexão recebida de {addr}")
    with conn:
        user = login_user(conn)
        conn.send(b"Login bem-sucedido. Envie comando (UPLOAD, DOWNLOAD, LIST, SAIR):")

        while True:
            try:
                comando = conn.recv(1024).decode().upper()
                if not comando:
                    break
                if comando == "UPLOAD":
                    handle_upload(conn, user)
                elif comando == "DOWNLOAD":
                    handle_download(conn, user)
                elif comando == "LIST":
                    handle_list(conn, user)
                elif comando == "SAIR":
                    conn.send("Encerrando conexão.".encode('utf-8'))
                    break
                else:
                    conn.send(b"Comando invalido.")
            except:
                break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor ouvindo em {HOST}:{PORT}...")

    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
