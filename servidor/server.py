import socket
from auth import AuthManager
from file_handler import FileHandler


class ServerApp:
    def __init__(self, host='127.0.0.1', port=9090):
        self.host = host
        self.port = port
        self.auth_manager = AuthManager()
        self.file_handler = FileHandler()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Servidor ouvindo em {self.host}:{self.port}...")

            conn, addr = s.accept()
            print(f"Conexão recebida de {addr}")

            with conn:
                user = self.auth_manager.login_user(conn)
                conn.send(b"Login bem-sucedido. Envie comando (UPLOAD, DOWNLOAD, LIST):")

                while True:
                    comando = conn.recv(1024).decode().upper()
                    if comando == "UPLOAD":
                        self.file_handler.handle_upload(conn, user)
                    elif comando == "DOWNLOAD":
                        self.file_handler.handle_download(conn, user)
                    elif comando == "LIST":
                        self.file_handler.handle_list(conn, user)
                    else:
                        conn.send(b"Comando invalido.")


if __name__ == "__main__":
    server = ServerApp()
    server.run()
