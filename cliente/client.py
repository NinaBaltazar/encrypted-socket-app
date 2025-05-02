import socket
import getpass
import os


class ClientApp:
    def __init__(self, host='127.0.0.1', port=9090):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_msg(self, msg):
        self.sock.send(msg.encode())

    def recv_msg(self):
        return self.sock.recv(1024).decode()

    def upload(self):
        nome = input("Nome do arquivo: ").strip()

        if not os.path.exists(nome):
            print("Arquivo não encontrado.")
            return

        nome_base = os.path.basename(nome)
        self.send_msg(nome_base)
        resposta = self.recv_msg()
        print(resposta)

        with open(nome, 'rb') as f:
            data = f.read()

        self.send_msg(str(len(data)))
        ack = self.recv_msg()
        if ack == "READY":
            self.sock.sendall(data)
            print(self.recv_msg())
        else:
            print("Erro ao iniciar upload")

    def download(self):
        nome = input("Nome do arquivo: ").strip()
        self.send_msg(nome)
        resposta = self.recv_msg()
        if resposta != "OK":
            print(resposta)
            return

        tamanho = int(self.recv_msg())
        self.send_msg("READY")

        data = b""
        while len(data) < tamanho:
            data += self.sock.recv(1024)

        with open(nome, 'wb') as f:
            f.write(data)

        print("Arquivo recebido com sucesso.")

    def list_files(self):
        print(self.recv_msg())

    def run(self):
        self.sock.connect((self.host, self.port))

        login = input("Login: ")
        senha = getpass.getpass("Senha: ")

        self.send_msg(login)
        self.send_msg(senha)

        resposta = self.recv_msg()
        print(resposta)

        if "sucesso" not in resposta:
            self.sock.close()
            exit()

        while True:
            prompt = self.recv_msg()
            print(prompt)

            comando = input("Digite o comando (UPLOAD, DOWNLOAD, LIST ou SAIR): ").strip().upper()
            self.send_msg(comando)

            if comando == "SAIR":
                break
            elif comando == "UPLOAD":
                self.upload()
            elif comando == "DOWNLOAD":
                self.download()
            elif comando == "LIST":
                self.list_files()
            else:
                print("Comando inválido.")

        self.sock.close()


if __name__ == "__main__":
    app = ClientApp()
    app.run()
