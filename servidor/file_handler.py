import os


class FileHandler:
    UPLOAD_DIR = "servidor/uploads"

    def ensure_user_dir(self, user):
        user_path = os.path.join(self.UPLOAD_DIR, user)
        os.makedirs(user_path, exist_ok=True)
        return user_path

    def handle_upload(self, conn, user):
        nome = conn.recv(1024).decode()
        conn.send(b"OK")

        try:
            size = int(conn.recv(1024).decode())
            conn.send(b"READY")

            data = b""
            while len(data) < size:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet

            user_dir = self.ensure_user_dir(user)
            path = os.path.join(user_dir, nome)

            with open(path, 'wb') as f:
                f.write(data)

            conn.send(b"Arquivo salvo com sucesso.")
        except Exception as e:
            conn.send(f"Erro ao salvar arquivo: {e}".encode())

    def handle_download(self, conn, user):
        nome = conn.recv(1024).decode()
        user_dir = self.ensure_user_dir(user)
        path = os.path.join(user_dir, nome)

        if not os.path.exists(path):
            conn.send(b"NOT_FOUND")
            return

        conn.send(b"OK")

        with open(path, 'rb') as f:
            data = f.read()

        conn.send(str(len(data)).encode())
        ack = conn.recv(1024).decode()
        if ack != "READY":
            return

        conn.sendall(data)

    def handle_list(self, conn, user):
        user_dir = self.ensure_user_dir(user)
        arquivos = os.listdir(user_dir)
        if not arquivos:
            conn.send(b"Nenhum arquivo encontrado.")
        else:
            conn.send("\n".join(arquivos).encode())
