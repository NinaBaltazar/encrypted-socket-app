import socket
import getpass
import os

HOST = '127.0.0.1'
PORT = 9090

def send_msg(sock, msg):
    sock.send(msg.encode())

def recv_msg(sock):
    return sock.recv(1024).decode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    login = input("Login: ")
    senha = getpass.getpass("Senha: ")

    send_msg(s, login)
    send_msg(s, senha)

    resposta = recv_msg(s)
    print(resposta)

    if "sucesso" not in resposta:
        s.close()
        exit()

    while True:
        prompt = recv_msg(s)
        print(prompt)

        comando = input("Digite o comando (UPLOAD, DOWNLOAD, LIST ou SAIR): ").strip().upper()
        send_msg(s, comando)

        if comando == "SAIR":
            break

        elif comando == "UPLOAD":
            nome = input("Nome do arquivo: ").strip()
            if not os.path.exists(nome):
                print("Arquivo não encontrado.")
                continue

            send_msg(s, nome)
            resposta = recv_msg(s)
            print(resposta)

            with open(nome, 'rb') as f:
                data = f.read()

            send_msg(s, str(len(data)))
            ack = recv_msg(s)
            if ack == "READY":
                s.sendall(data)
                print(recv_msg(s))
            else:
                print("Erro ao iniciar upload")

        elif comando == "DOWNLOAD":
            nome = input("Nome do arquivo: ").strip()
            send_msg(s, nome)
            resposta = recv_msg(s)
            if resposta != "OK":
                print(resposta)
                continue

            tamanho = int(recv_msg(s))
            send_msg(s, "READY")

            data = b""
            while len(data) < tamanho:
                data += s.recv(1024)

            with open(nome, 'wb') as f:
                f.write(data)

            print("Arquivo recebido com sucesso.")

        elif comando == "LIST":
            print(recv_msg(s))

        else:
            print("Comando inválido.")
