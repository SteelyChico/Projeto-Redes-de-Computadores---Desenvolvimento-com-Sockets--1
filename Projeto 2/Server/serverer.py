import socket

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8000

tipo_arquivo_binario = ['png', 'jpeg', 'bmp', 'jpg']
tipo_arquivo_text = ['html', 'css', 'js']

cabecalho_resposta = f'HTTP/1.1 200 OK\r\n\r\n'

# criando o objeto socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# solicitar ao windows para ouvir na porta 8000
socket_servidor.bind((SERVER_ADDRESS, SERVER_PORT))
socket_servidor.listen()

print(f'Servidor ouvindo em {SERVER_ADDRESS}:{SERVER_PORT} pronto para receber conexões...')
socket_cliente, cliente_addr = socket_servidor.accept()

# debug
print(f'cliente conectado com sucesso. {cliente_addr[0]}:{cliente_addr[1]}')

# receber dados do cliente
dado_recebido = socket_cliente.recv(1024).decode()

print(f'arquivo solicitado: {dado_recebido}')

try:
# obtendo a extensao
    extensao = dado_recebido.split('.')[-1]
    print (extensao)
    if extensao not in tipo_arquivo_binario and extensao not in tipo_arquivo_text:
        print(f'O arquivo {dado_recebido} não está em uma formatação entendível')
        socket_cliente.sendall(b'HTTP/1.1 400 Bad request file\r\n\r\nFound Bad request file')
        socket_cliente.close()

    else:
        file = open(dado_recebido)
        print (file)
        arquivo_binario = False
        if extensao in tipo_arquivo_binario:
            arquivo_binario = True

        # abrir o arquivo
        if arquivo_binario:
            file = open(dado_recebido, 'rb')
            conteudo_arquivo = file.read()
            socket_cliente.sendall(conteudo_arquivo)
        else:
            file = open(dado_recebido, 'r')
            conteudo_arquivo = file.read()
            resposta_final = cabecalho_resposta + conteudo_arquivo
            socket_cliente.sendall(resposta_final.encode('utf-8'))

except FileNotFoundError:
    print(f'arquivo nao existe {dado_recebido}')
    socket_cliente.sendall(b'HTTP/1.1 404 File not found\r\n\r\nFound file not found')
    socket_cliente.close()


# encerrar a conexão
socket_cliente.close()


