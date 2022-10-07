import random
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


def HandleRequest(mClientSocket, mClientAddr):
    #Recebe no data1 o primo e gerador que foi enviado pelo cliente
    data1 = mClientSocket.recv(2048)

    req1 = data1.decode()
    chaves = req1.split(' ')
    
    primoComum = int(chaves[1])
    gerador = int(chaves[2])
    print(f'primocomum = {primoComum}// gerador = {gerador}')
    #envia para o cliente que esta de acordo com o primo e gerador recebido
    rep = 'Chaves OK'
    mClientSocket.send(rep.encode())

    #Cria uma chave confidencial do servidor
    chaveConfidencialServidor = random.randint(0,1000)
    #Executa o primeiro dieff hellman e envia para o servidor sua chave publica do cliente o rep1
    rep1 = ((gerador**(chaveConfidencialServidor)) % primoComum)
    mClientSocket.send(str(rep1).encode())

    #Recebe a chave publica do cliente
    data2 = mClientSocket.recv(2048)
    req2 = data2.decode()
    chavePublicaCliente = int(req2)

    #gera a chave compartihada do cliente e servidor
    chaveCompartilhada = (chavePublicaCliente**chaveConfidencialServidor)%primoComum
    print(f'Chave compartilhada = {chaveCompartilhada}')
    #Envia para o cliente a chave compartilhada
    
    mClientSocket.send(str(chaveCompartilhada).encode())
    
    #Recebe a chave compartilhada do cliente
    data3 = mClientSocket.recv(2048)
    req3 = data3.decode()
    
    #Começa a transferencia dos dados e verifica se a chave compartilhada recebeida é a mesma enviada
    while True and req3 == str(chaveCompartilhada):
        # Este loop foi criado para que o servidor conseguisse receber diversas requisições de
        # um mesmo cliente, usando a mesma conexão, ou seja, sem que fosse necessária a
        # criação de uma nova conexão.
        print('Esperando o próximo pacote ...')
        # Recebendo os dados do Cliente:
        # o Servidor irá receber bytes do cliente, sendo necessária a conversão de bytes
        # para string ou para o tipo desejado.
        data = mClientSocket.recv(2048)
        print(f'Requisição recebida de {mClientAddr}')
        req = data.decode()
        print(f'A requisição foi:{req}')
        # Após receber e processar a requisição o servidor está apto para enviar uma resposta.
        rep = input('>>>')
        mClientSocket.send(rep.encode())


mSocketServer = socket(AF_INET, SOCK_STREAM)

mSocketServer.bind(('127.0.0.1',1235))

mSocketServer.listen()

while True:
    clientSocket, clientAddr =  mSocketServer.accept()
    Thread(target=HandleRequest, args=(clientSocket, clientAddr)).start()
