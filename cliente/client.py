import socket
import getpass
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crypto_utils import (
    generate_ec_key_pair,
    export_public_key,
    import_public_key,
    derive_shared_key_ec,
    encrypt_aes,
    decrypt_aes
)

HOST = '127.0.0.1'
PORT = 9090

def send_encrypted(sock, key, msg):
    sock.send(encrypt_aes(key, msg.encode()))

def recv_encrypted(sock, key):
    return decrypt_aes(key, sock.recv(4096)).decode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Troca de chaves EC
    client_priv, client_pub = generate_ec_key_pair()
    server_pub_bytes = s.recv(1024)
    s.send(export_public_key(client_pub))
    server_pub = import_public_key(server_pub_bytes)
    session_key = derive_shared_key_ec(client_priv, server_pub)

    # Autenticação
    login = input("Login: ")
    senha = getpass.getpass("Senha: ")

    send_encrypted(s, session_key, login)
    send_encrypted(s, session_key, senha)

    resposta = recv_encrypted(s, session_key)
    print(resposta)

    if "sucesso" not in resposta:
        input("Pressione Enter para sair...")
        s.close()
        exit()

    while True:
        prompt = recv_encrypted(s, session_key)
        print(prompt)

        comando = input("\nDigite o comando (UPLOAD, DOWNLOAD, LIST ou SAIR): ").strip().upper()
        send_encrypted(s, session_key, comando)

        if comando == "SAIR":
            break

        elif comando == "UPLOAD":
            nome = input("Nome do arquivo: ").strip()
            if not os.path.exists(nome):
                print("\nArquivo não encontrado.")
                continue

            nome_base = os.path.basename(nome)
            send_encrypted(s, session_key, nome_base)
            print(recv_encrypted(s, session_key))

            with open(nome, 'rb') as f:
                data = f.read()

            encrypted = encrypt_aes(session_key, data)
            send_encrypted(s, session_key, str(len(encrypted)))
            if recv_encrypted(s, session_key) == "READY":
                s.sendall(encrypted)
                print(recv_encrypted(s, session_key))

        elif comando == "DOWNLOAD":
            remetente = input("De qual usuário você deseja baixar?: ").strip()
            nome = input("Nome do arquivo: ").strip()

            send_encrypted(s, session_key, remetente)
            send_encrypted(s, session_key, nome)
            resposta = recv_encrypted(s, session_key)
            if resposta != "OK":
                print(resposta)
                continue

            tamanho = int(recv_encrypted(s, session_key))
            send_encrypted(s, session_key, "READY")

            data = b""
            while len(data) < tamanho:
                data += s.recv(1024)

            decrypted = decrypt_aes(session_key, data)

            # Salvar na pasta correta do cliente
            base_dir = os.path.dirname(__file__)
            download_path = os.path.join(base_dir, 'downloads', remetente)
            os.makedirs(download_path, exist_ok=True)

            with open(os.path.join(download_path, nome), 'wb') as f:
                f.write(decrypted)

            print("\nArquivo recebido com sucesso.")

        elif comando == "LIST":
            print(recv_encrypted(s, session_key))

        else:
            print("\nComando inválido.")

        # Sempre espera "FIM_OPERACAO" antes de voltar ao menu
        fim_operacao = recv_encrypted(s, session_key).strip()
        if fim_operacao != "FIM OPERACAO":
            print("\nErro de sincronização com servidor. Recebido: {fim_operacao}.")
            break