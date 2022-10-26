import random
import cryptocode
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import htmlMessage
import cryptography
from cryptography.fernet import Fernet

# geração de chave
key = Fernet.generate_key()
# string a chave em um arquivo
with open('filekey.key', 'wb') as filekey:
    filekey.write(key)

# usando a chave gerada
fernet = Fernet(key)



def critogrtafiaAES(mensagem, senha):  # funcao de criptografia
    mensagemCriptografada = cryptocode.encrypt(mensagem, f"{senha}")

    return mensagemCriptografada


def descriptografiaAES(mensagemCriptografada, senha):  # funcao de descriptografia
    mensagemDescriptografada = cryptocode.decrypt(mensagemCriptografada, f"{senha}")

    return mensagemDescriptografada


def HandleRequest(mClientSocket, mClientAddr):
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

    # Cria senha para a criptografia e manda para o cliente
    senhaCriptografia = random.randint(100, 999)
    SenhaCriptografiaEnviar = (f'{senhaCriptografia}')
    mClientSocket.send(SenhaCriptografiaEnviar.encode())

    # Recebe assinatura das mensagens
    data4 = mClientSocket.recv(2048)
    assinatura = data4.decode()

    # verifica se a chave compartilhada recebeida é a mesma enviada, e recebe o indentificador do cliente
    if req3 == str(chaveCompartilhada):
        # Recebe identificacao do cliente
        data = mClientSocket.recv(2048)
        print(f'Requisição recebida de {mClientAddr}')
        req = data.decode()

        # Recebe Assinatura da mensagem recebida
        data1 = mClientSocket.recv(2048)
        reqassinatura = data1.decode()

        # Verifica se a assinatura esta correta
        if str(reqassinatura) != str(assinatura):
            print('Assinatura incompativel')
        else:
            reqDescriptografado = descriptografiaAES(req, senhaCriptografia)
            print(f'Identificação do cliente: {reqDescriptografado}')
            rep = f'Seu endereço: {mClientAddr}'
            repCriptografado = critogrtafiaAES(rep, senhaCriptografia)
            mClientSocket.send(repCriptografado.encode())
            # envia assinatura
            mClientSocket.send(str(reqassinatura).encode())
            # Após receber e processar a requisição o servidor está apto para enviar uma resposta.
            if int(reqDescriptografado) in clientesAutorizados:
                mensagemAutorizacao = 'cliente Autorizado'
                menssagemCriptografada = critogrtafiaAES(mensagemAutorizacao, senhaCriptografia)
                mClientSocket.send(menssagemCriptografada.encode())
                while True:
                    nomeArquivo = mClientSocket.recv(2048).decode()

                    nomeArquivoDescriptografado = descriptografiaAES(nomeArquivo, senhaCriptografia)

                    extensao = nomeArquivoDescriptografado.split('.')[-1]
                    arquivoBinario = False
                    if extensao in tipoArquivoBinario:
                        arquivoBinario = True

                    if (arquivoBinario is False) and extensao not in tipoArquivoText:
                        erro400 = "sintaxe cringe"
                        mClientSocket.send(erro400.encode())
                        print(htmlMessage.BadRequest())
                    else:
                        mClientSocket.send(key)
                        erro400 = 'sintaxe ok'
                        mClientSocket.send(erro400.encode())
                        try:
                            if arquivoBinario:
                                print('é binario')
                                file = open(nomeArquivoDescriptografado, 'rb')
                                original = file.read()
                                encrypted = fernet.encrypt(original)
                                mClientSocket.send(encrypted)
                                # mClientSocket.send(b'') #para parar o código
                            else:
                                print('não é binario')
                                file = open(nomeArquivoDescriptografado, 'rb')
                                # mClientSocket.send(b'') #para parar o código
                                original = file.read()
                                encrypted = fernet.encrypt(original)
                                mClientSocket.send(encrypted)

                        except FileNotFoundError:
                            print(f'arquivo nao existe {nomeArquivoDescriptografado}')
                            print(htmlMessage.NotFound())
                    
            else:
                print('Cliente nao autorizado')
                erro403 = 'O cliente não tem direitos de acesso ao conteúdo, portanto o servidor está rejeitando dar ' \
                          'a resposta. '
                print(htmlMessage.erro403())
                mClientSocket.send(erro403.encode())
                mClientSocket.close()

    # Adicioana clientes na lista de clientes
    if mClientAddr not in listaClientes:
        listaClientes.append([f'Identificação: {reqDescriptografado}', f'Chave compartilhada: {chaveCompartilhada}',
                              f'endereço: {mClientAddr}'])


tipoArquivoBinario = ['png', 'jpeg', 'bmp', 'jpg']
tipoArquivoText = ['html', 'css', 'js']
clientesAutorizados = [22, 10, 45, 44, 4433, 222, 44777]
listaClientes = []

mSocketServer = socket(AF_INET, SOCK_STREAM)

mSocketServer.bind(('127.0.0.1', 1235))

mSocketServer.listen()
print(f"servidor ouvindo em 127.0.0.1:1235")


while True:
    clientSocket, clientAddr = mSocketServer.accept()
    Thread(target=HandleRequest, args=(clientSocket, clientAddr)).start()
