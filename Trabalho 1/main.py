# Filename: main.py
# Author: Vladimir Belinski
# Description: server side of a chat application

from bottle import run, get, post, view, request, route, static_file

chat_content = []

# The route() decorator links an URL path to a callback function, and adds a new route to
# the default application.

# Static files such as images or CSS files are not served automatically. It's necessary
# to add a route and a callback to control which files get served  and where to find them.
# The static_file() function is a helper to serve files in a safe and convenient way.
# To serve files in subdirectories it's necessary to use the :path filter in the wildcard:
# <filepath:path>.
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

# The HTTP protocol defines several request methods for different tasks. GET is the default
# for all routes with no other method specified. These routes will match GET requests only.
# To handle other methods such as POST add a method keyword argument to the route() decorator
# or use one of the five alternative decorators: get(), post(), put(), delete() or patch().
@get('/chat')
@post('/chat')
# To render a template you can use the template() function or the view() decorator. All you
# have to do is to provide the name of the template and the variables you want to pass to
# the template as keyword arguments. Bottle will look for templates in the ./views/ folder
# or any folder specified in the bottle TEMPLATE_PATH list. The view() decorator allows you
# to return a dictionary with the template variables instead of calling template().
@view('chat')
def renderChat():
    name = request.forms.getunicode('name')
    message = request.forms.getunicode('message')
    if name != None and message != None:
        chat_content.append([name, message])
    return dict(name=name, chat_content=chat_content)

# run() starts a built-in development server. It runs on localhost port 8080 and serves
# requests until you hit Control-c.
run(host='localhost', port=8080)
