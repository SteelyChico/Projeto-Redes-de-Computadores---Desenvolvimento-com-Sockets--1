from email.utils import formatdate
from datetime import datetime
from time import mktime


def sucesso():
    now = datetime.now()
    mStamp = mktime(now.timetuple())

    # header
    resposta = ''
    resposta += 'HTTP/1.1 200 OK\r\n'
    resposta += f'Date: {formatdate(timeval=mStamp, localtime=False, usegmt=True)}\r\n'
    resposta += 'Server: Localhost\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'
    resposta += '\r\n'

    # mensagem
    html = ''
    html += '<html>'
    html += '<head>'
    html += '<title>Redes de Computadores - CIn/UFPE</title>'
    html += '<meta charset="UTF-8">'
    html += '</head>'
    html += '<body>'
    html += '<h1>Hello World</h1>'
    html += '</body>'
    html += '</html>'

    resposta += html
    return resposta


def NotFound():
    now = datetime.now()
    mStamp = mktime(now.timetuple())

    resposta = ''
    resposta += 'HTTP/1.1 404 Not Found\r\n'
    resposta += f'Date: {formatdate(timeval=mStamp, localtime=False, usegmt=True)}\r\n'
    resposta += 'Server: LocalHost\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'
    resposta += '\r\n'

    html = ''
    html += '<html>'
    html += '<head>'
    html += '<title>Not Found - CIn/UFPE</title>'
    html += '<meta charset="UTF-8">'
    html += '</head>'
    html += '<body>'
    html += '<h1>Essa requisição não foi encontrada no servidor</h1>'
    html += '</body>'
    html += '</html>'

    resposta += html
    return resposta


def BadRequest():
    now = datetime.now()
    mStamp = mktime(now.timetuple())

    resposta = ''
    resposta += 'HTTP/1.1 400 Bad Request\r\n'
    resposta += f'Date: {formatdate(timeval=mStamp, localtime=False, usegmt=True)}\r\n'
    resposta += 'Server: localhost\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'
    resposta += '\r\n'

    html = ''
    html += '<html>'
    html += '<head>'
    html += '<title>Bad Request</title>'
    html += '<meta charset="UTF-8">'
    html += '</head>'
    html += '<body>'
    html += '<h1>Requisição não entendida pelo servidor, houve um erro de sintaxe</h1>'
    html += '</body>'
    html += '</html>'

    resposta += html
    return resposta


def erro403():
    now = datetime.now()
    mStamp = mktime(now.timetuple())

    resposta = ''
    resposta += 'HTTP/1.1 403 Forbidden\r\n'
    resposta += f'Date: {formatdate(timeval=mStamp, localtime=False, usegmt=True)}\r\n'
    resposta += 'Server: localhost\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'
    resposta += '\r\n'

    html = ''
    html += '<html>'
    html += '<head>'
    html += '<title>Forbidden</title>'
    html += '<meta charset="UTF-8">'
    html += '</head>'
    html += '<body>'
    html += '<h1>Cliente não tem acesso aos arquivos do servidor</h1>'
    html += '</body>'
    html += '</html>'

    resposta += html
    return resposta

