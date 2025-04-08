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

    status = recv_msg(s)
    print(status)

    if "sucesso" not in status and "Criando novo" not in status:
        exit()

    while True:
        prompt = recv_msg(s)
        print(prompt)

        comando = input("Digite o comando (UPLOAD, DOWNLOAD, LIST ou SAIR): ").strip().upper()
        send_msg(s, comando)

        if comando == "SAIR":
            print("Saindo.")
            break

        elif comando == "UPLOAD":
            nome = input("Nome do arquivo: ")
            if not os.path.exists(nome):
                print("Arquivo não encontrado.")
                continue

            send_msg(s, nome)
            resposta = recv_msg(s)
            print(resposta)
            if resposta != "OK":
                continue

            with open(nome, 'rb') as f:
                data = f.read()

            send_msg(s, str(len(data)))  # envia o tamanho como string
            ack = recv_msg(s)  # espera confirmação
            if ack != "READY":
                print("Erro no protocolo.")
                continue

            s.sendall(data)  # envia o conteúdo

            print(recv_msg(s))  # confirmação do servidor

        elif comando == "DOWNLOAD":
            nome = input("Nome do arquivo: ")
            send_msg(s, nome)

            status = recv_msg(s)
            if status != "OK":
                print("Arquivo não encontrado no servidor.")
                continue

            tamanho = int(recv_msg(s))
            s.send(b"READY")  # confirmação para o servidor

            data = b""
            while len(data) < tamanho:
                packet = s.recv(4096)
                if not packet:
                    break
                data += packet

            with open(nome, 'wb') as f:
                f.write(data)

            print("Arquivo recebido com sucesso.")

        elif comando == "LIST":
            print(recv_msg(s))

        else:
            print("Comando inválido.")
