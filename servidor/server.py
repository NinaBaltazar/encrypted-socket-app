import socket
from auth import login_user
from file_handler import handle_upload, handle_download, handle_list

HOST = '127.0.0.1'
PORT = 9090

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print(f"Servidor ouvindo em {HOST}:{PORT}...")
    conn, addr = s.accept()
    print(f"Conexão recebida de {addr}")

    with conn:
        user = login_user(conn)
        conn.send(b"Login bem-sucedido. Envie comando (UPLOAD, DOWNLOAD, LIST):")

        while True:
            comando = conn.recv(1024).decode().upper()
            if comando == "UPLOAD":
                handle_upload(conn, user)
            elif comando == "DOWNLOAD":
                handle_download(conn, user)
            elif comando == "LIST":
                handle_list(conn, user)
            else:
                conn.send(b"Comando invalido.")
