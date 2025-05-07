# Encrypted Socket App

## Visão Geral
Este projeto é uma aplicação baseada em sockets criptografados, projetada para comunicação segura entre um servidor e clientes. Ele utiliza criptografia para garantir que os dados e mensagens dos usuários sejam transmitidos com segurança.

## Funcionalidades
- Autenticação segura de usuários usando senhas com hash.
- Comunicação criptografada entre servidor e clientes.
- Gerenciamento de usuários com credenciais pré-definidas.

## Pré-requisitos
- Node.js instalado no sistema.
- Python instalado no sistema.
- Um gerenciador de pacotes como npm ou yarn.

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/NinaBaltazar/encrypted-socket-app.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd encrypted-socket-app
   ```
3. Instale as dependências do Node.js:
   ```bash
   npm install
   ```
4. Instale as bibliotecas Python listadas no `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Uso
1. Inicie o servidor:
   ```bash
   node servidor/server.js
   ```
2. Conecte um cliente ao servidor:
   ```bash
   node cliente/client.js
   ```

### Baixar Arquivos
- Para baixar um arquivo de outro usuário, digite o nome do usuário seguido do nome do arquivo desejado. 
- O arquivo será salvo automaticamente na pasta `cliente/downloads`.

### Fazer Upload de Arquivos
- Para realizar o upload de um arquivo, crie um arquivo `.txt` na pasta `cliente/`.
- Ao realizar o upload, informe o caminho completo do arquivo, por exemplo: `cliente/nomedoarquivo.txt`.

## Configuração
- As credenciais dos usuários estão armazenadas no arquivo `servidor/users.json`. Você pode adicionar ou modificar usuários editando este arquivo. As senhas devem ser armazenadas como hashes seguros (por exemplo, SHA-256).

## Notas de Segurança
- Certifique-se de que o servidor esteja sendo executado em um ambiente seguro.
- Use senhas fortes para as contas de usuário.




