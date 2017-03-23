from bottle import run, get, post, view, request, redirect, route, static_file
import bottle

chat_content = []

@bottle.route('/static/<path:path>')
def server_static(path):
    return static_file(path, root='static')

@get('/chat')
@post('/chat')
@view('chat')
def renderChat():
    name = request.forms.getunicode('name')
    message = request.forms.getunicode('message')
    if name != None and message != None:
        chat_content.append([name, message])
    return {'name': name, 'chat_content': chat_content}

run(host='localhost', port=8080)
