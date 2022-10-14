import random
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def criaCipher(chave, iv, backend):
    # cria o objeto de criptografia a partir da chave
    aes = algorithms.AES(chave)
    # cria o modo de inicialização
    cbc = modes.CBC(iv)
    # cria o cipher
    cipher = Cipher(aes, cbc, backend=backend)

    return cipher


def critogrtafiaAES(mensagem, chave, iv, backend):  # funcao de criptografia
    # Ajusta a menssagem enviada para ser multipla de 16
    tamanhoBloco = 16
    n = len(mensagem)
    addEspaco = tamanhoBloco - n % tamanhoBloco
    novaMensagem = bytearray(mensagem + ' ' * addEspaco, encoding="utf8")

    cipher = criaCipher(chave, iv, backend)
    # pega o encriptador a partir do cipher
    encriptador = cipher.encryptor()
    # Encripta a mensagem
    mensagemCriptografada = encriptador.update(novaMensagem) + encriptador.finalize()

    return mensagemCriptografada


def descriptografiaAES(mensagemCriptografada, chave, iv, backend):  # funcao de descriptografia
    cipher = criaCipher(chave, iv, backend)
    decriptografador = cipher.decryptor()
    decriptografador.update(mensagemCriptografada) + decriptografador.finalize
    mensagemDescriptografada = mensagemCriptografada

    return mensagemDescriptografada


def HandleRequest(mClientSocket, mClientAddr):
    backend = default_backend()
    chave = os.urandom(32)
    iv = os.urandom(16)

    # Recebe no data1 o primo e gerador que foi enviado pelo cliente
    data1 = mClientSocket.recv(2048)

    req1 = data1.decode()
    chaves = req1.split(' ')

    primoComum = int(chaves[1])
    gerador = int(chaves[2])
    print(f'primocomum = {primoComum}// gerador = {gerador}')
    # envia para o cliente que esta de acordo com o primo e gerador recebido
    rep = 'Chaves OK'
    mClientSocket.send(rep.encode())

    # Cria uma chave confidencial do servidor
    chaveConfidencialServidor = random.randint(0, 1000)
    # Executa o primeiro dieff hellman e envia para o servidor sua chave publica do cliente o rep1
    rep1 = ((gerador ** (chaveConfidencialServidor)) % primoComum)
    mClientSocket.send(str(rep1).encode())

    # Recebe a chave publica do cliente
    data2 = mClientSocket.recv(2048)
    req2 = data2.decode()
    chavePublicaCliente = int(req2)

    # gera a chave compartihada do cliente e servidor
    chaveCompartilhada = (chavePublicaCliente ** chaveConfidencialServidor) % primoComum
    print(f'Chave compartilhada = {chaveCompartilhada}')
    # Envia para o cliente a chave compartilhada

    mClientSocket.send(str(chaveCompartilhada).encode())

    # Recebe a chave compartilhada do cliente
    data3 = mClientSocket.recv(2048)
    req3 = data3.decode()

    chaveIvBackend = (f'{chave} {iv} {backend}')
    mClientSocket.send(chaveIvBackend.encode())

    # Começa a transferencia dos dados e verifica se a chave compartilhada recebeida é a mesma enviada
    while True and req3 == str(chaveCompartilhada):
        print('Esperando o próximo pacote ...')

        data = mClientSocket.recv(2048)
        print(f'Requisição recebida de {mClientAddr}')
        req = data.decode()
        reqDescriptofrado = descriptografiaAES(req, chave, iv, backend)
        print(f'A requisição foi:{reqDescriptofrado}')

        # Após receber e processar a requisição o servidor está apto para enviar uma resposta.
        rep = f'Oi clinte {mClientAddr}'
        repCriptografado = critogrtafiaAES(rep, chave, iv, backend)
        mClientSocket.send(repCriptografado.encode())


mSocketServer = socket(AF_INET, SOCK_STREAM)

mSocketServer.bind(('127.0.0.1', 1235))

mSocketServer.listen()

while True:
    clientSocket, clientAddr = mSocketServer.accept()
    Thread(target=HandleRequest, args=(clientSocket, clientAddr)).start()
