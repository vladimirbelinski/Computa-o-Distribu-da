from bottle import run, get, post, view, request, redirect, route, static_file

chat_content = []

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@get('/chat')
@post('/chat')
@view('chat')
def renderChat():
    name = request.forms.getunicode('name')
    message = request.forms.getunicode('message')
    if name != None and message != None:
        chat_content.append([name, message])
    return dict(name=name, chat_content=chat_content)

run(host='localhost', port=8080)
