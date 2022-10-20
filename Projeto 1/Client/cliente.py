import random
from socket import socket, AF_INET, SOCK_STREAM
import cryptocode

def critogrtafiaAES(mensagem, senha): # funcao de criptografia
    mensagemCriptografada = cryptocode.encrypt(mensagem, f"{senha}")

    return mensagemCriptografada

def descriptografiaAES(mensagemCriptografada, senha): #funcao de descriptografia
    mensagemDescriptografada = cryptocode.decrypt(mensagemCriptografada, f"{senha}")

    return mensagemDescriptografada


def CriaGeradores(): #criou o gerador e primo comum aos dois
    geradorPrimo = random.randint(1,1000)
    gerador = random.randint(1,1000)

    while not primo(geradorPrimo):
        geradorPrimo = random.randint(1,1000)
    return geradorPrimo, gerador 

def primo(n): #função para verificar se é primo
    for i in range(2,n):
        if n % i == 0:
            return False
    return True

mClientSocket = socket(AF_INET, SOCK_STREAM)
mClientSocket.connect(('localhost', 1235))

geradorPrimo, gerador = CriaGeradores()
#Envia essas chaves para o servidor
chavesPrimoGerador = (f'chaves {geradorPrimo} {gerador}')
mClientSocket.send(chavesPrimoGerador.encode())

#O cliente recebe uma mensagem aprovando que o servidor
#recebeu o gerador e o primo
confimacao = mClientSocket.recv(2048)
req = confimacao.decode()

if req == 'Chaves OK':
    #Cria uma chave confidencial do cliente
    chaveConfidencialCliente = random.randint(0,1000)
    #Executa o primeiro dieff hellman e envia para o servidor sua chave publica do cliente o rep1
    rep1 = (gerador**(chaveConfidencialCliente))%geradorPrimo
    mClientSocket.send(str(rep1).encode())

    #Recebe a chave publica do servidor 
    data1 = mClientSocket.recv(2048)
    req1 = data1.decode()
    chavePublicaServidor = int(req1)
    print(f'Chave publica do servidor = {chavePublicaServidor}')

    #gera a chave compartihada do cliente e servidor
    chaveCompartilhada = (chavePublicaServidor**chaveConfidencialCliente)%geradorPrimo
    print(f'chave compartilhada = {chaveCompartilhada}')

    #Envia para o servidor a chave compartilhada
    mClientSocket.send(str(chaveCompartilhada).encode())
    #Recebe a chave compartilhada do servidor
    data2 = mClientSocket.recv(2048)
    req2 = data2.decode()

    #Recebe Chave/Senha de criptografia
    data3 = mClientSocket.recv(2048)
    req3 = data3.decode()
    senhaCriptografia = req3

    #Cria assinatura e manda para o servidor
    assinaturaDig = random.randint(0,999999999)
    assinatura = f"{assinaturaDig}"
    mClientSocket.send(assinatura.encode())
    print(assinatura)

#Começa a transferencia dos dados e verifica se a chave compartilhada recebeida é a mesma enviada
while True and req2 == str(chaveCompartilhada):
    # Este loop foi criado apenas para que o cliente conseguisse enviar múltiplas solicitações
    mensagem = input('>>')
    #criptografa a mensagem recebida 
    mensagemCriptografada = critogrtafiaAES(mensagem,senhaCriptografia)
    #Envia a mensagem criptografada pelo socket criado
    mClientSocket.send(mensagemCriptografada.encode())

    mClientSocket.send(assinatura.encode())
    #Recebendo as respostas do servidor
    data = mClientSocket.recv(2048)
    reply = data.decode()
    #Recebe assinatura
    data1 = mClientSocket.recv(2048)
    reply1 = data1.decode()

    #Verifica assinatura
    if str(reply1) != str(assinatura):
        break
    else:
        #descriptografa a mensagem recebida
        mensagemDescriptografada = descriptografiaAES(reply, senhaCriptografia)
        print(f'Resposta recebida:{mensagemDescriptografada}')
