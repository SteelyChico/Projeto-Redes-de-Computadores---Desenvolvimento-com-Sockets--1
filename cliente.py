import random
from socket import socket, AF_INET, SOCK_STREAM

mClientSocket = socket(AF_INET, SOCK_STREAM)
mClientSocket.connect(('localhost', 1235))


def primo(n): #função para verificar se é primo
    for i in range(2,n):
        if n % i == 0:
            return False
    return True

#criou o gerador e primo comum aos dois
primoComum = random.randint(1,1000)
gerador = random.randint(1,1000)

while not primo(primoComum):
    primoComum = random.randint(1,1000)

#Envia essas chaves para o servidor
chavesPrimoGerador = (f'chaves {primoComum} {gerador}')
mClientSocket.send(chavesPrimoGerador.encode())

#O cliente recebe uma mensagem aprovando que o servidor
#recebeu o gerador e o primo
data = mClientSocket.recv(2048)
req = data.decode()
if req == 'Chaves OK':
    #Cria uma chave confidencial do cliente
    chaveConfidencialCliente = random.randint(0,1000)
    #Executa o primeiro dieff hellman e envia para o servidor sua chave publica do cliente o rep1
    rep1 = (gerador**(chaveConfidencialCliente))%primoComum
    mClientSocket.send(str(rep1).encode())

    #Recebe a chave publica do servidor 
    data1 = mClientSocket.recv(2048)
    req1 = data.decode()
    chavePublicaServidor = int(req1)

    #gera a chave compartihada do cliente e servidor
    chaveCompartilhada = (chavePublicaServidor**chaveConfidencialCliente)%primoComum
    #Envia para o servidor a chave compartilhada
    mClientSocket.send(str(chaveCompartilhada).encode)
    #Recebe a chave compartilhada do servidor
    data2 = mClientSocket.recv(2048)
    req2 = data2.decode()

#Começa a transferencia dos dados e verifica se a chave compartilhada recebeida é a mesma enviada
while True and req2 == chaveCompartilhada:
    # Este loop foi criado apenas para que o cliente conseguisse enviar múltiplas solicitações
    message = input('>>')
    #Enviando a mensagem pelo socket criado.
    mClientSocket.send(message.encode())
    #Recebendo as respostas do servidor.
    data = mClientSocket.recv(2048)
    reply = data.decode()
    print(f'Resposta recebida:{reply}')

