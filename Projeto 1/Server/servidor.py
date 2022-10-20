from ast import Break
import random
import cryptocode
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


def critogrtafiaAES(mensagem, senha): # funcao de criptografia
    mensagemCriptografada = cryptocode.encrypt(mensagem, f"{senha}")

    return mensagemCriptografada

def descriptografiaAES(mensagemCriptografada, senha): #funcao de descriptografia
    mensagemDescriptografada = cryptocode.decrypt(mensagemCriptografada, f"{senha}")

    return mensagemDescriptografada


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

    #Cria senha para a criptografia e manda para o cliente
    senhaCriptografia = random.randint(1000000,9999999)
    SenhaCriptografiaEnviar = (f'{senhaCriptografia}')
    mClientSocket.send(SenhaCriptografiaEnviar.encode())

    #Recebe assinatura das mensagens
    data4 = mClientSocket.recv(2048)
    assinatura = data4.decode()
    
    #Começa a transferencia dos dados e verifica se a chave compartilhada recebeida é a mesma enviada
    while True and req3 == str(chaveCompartilhada):
        print('Esperando o próximo pacote ...')

        #Recebe daddos/mensagem
        data = mClientSocket.recv(2048)
        print(f'Requisição recebida de {mClientAddr}')
        req = data.decode()

        #Recebe Assinatura da mensagem recebida
        data1 = mClientSocket.recv(2048)
        reqassinatura = data1.decode()

        #Verifica se a assinatura esta correta
        if str(reqassinatura) != str(assinatura):
            break
        else: 
            reqDescriptografado = descriptografiaAES(req, senhaCriptografia)
            print(f'A requisição foi:{reqDescriptografado}')

        # Após receber e processar a requisição o servidor está apto para enviar uma resposta.
        rep = f'Oi clinte {mClientAddr}'
        repCriptografado = critogrtafiaAES(rep, senhaCriptografia)
        mClientSocket.send(repCriptografado.encode())
        #envia assinatura
        mClientSocket.send(str(reqassinatura).encode())
    
    #Adicioana clientes na lista de clientes
    if mClientAddr not in listaClientes:
        listaClientes.append(mClientAddr)


listaClientes = []

mSocketServer = socket(AF_INET, SOCK_STREAM)

mSocketServer.bind(('127.0.0.1',1235))

mSocketServer.listen()

while True:
    clientSocket, clientAddr =  mSocketServer.accept()
    Thread(target=HandleRequest, args=(clientSocket, clientAddr)).start()
