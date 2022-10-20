import socket

servidorAddress = "127.0.0.1"
servidorPorta = 8000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect((servidorAddress, servidorPorta))
print('conectado')

while True:

    namefile = str(input('Arquivo:'))

    cliente.send(namefile.encode())

    with open(namefile, 'wb') as file:
        while True:
            data = cliente.recv(1500000)
            if not data:
                break
            file.write(data)

    print('dado recebido')
