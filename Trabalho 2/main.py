# Filename: main.py
# Author: Vladimir Belinski
# Description: server side of a chat application (with multicast)

from bottle import run, get, post, view, request, route, static_file, template, redirect
import bottle
import json
import threading
import requests
import time
import sys

chatContent = set([])
name = ""
peers = ['localhost:' + p for p in sys.argv[2:]]
lock = threading.Lock()

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

# Just redirecting 'localhost:port/' to 'localhost:port/chat'
@route('/')
def chatRedirect():
    redirect('/chat')

# The HTTP protocol defines several request methods for different tasks. GET is the default
# for all routes with no other method specified. These routes will match GET requests only.
# To handle other methods such as POST add a method keyword argument to the route() decorator
# or use one of the five alternative decorators: get(), post(), put(), delete() or patch().

# To render a template you can use the template() function or the view() decorator. All you
# have to do is to provide the name of the template and the variables you want to pass to
# the template as keyword arguments. Bottle will look for templates in the ./views/ folder
# or any folder specified in the bottle TEMPLATE_PATH list. The view() decorator allows you
# to return a dictionary with the template variables instead of calling template().

@get('/chat')
@view('chat')
def chat():
    return dict(name=name, chatContent=list(chatContent))

@post('/send')
def sendMessage():
    global name
    nme = request.forms.getunicode('name')
    message = request.forms.getunicode('message')
    if nme != None and message != None:
        chatContent.add((nme, message))
        name = nme
        redirect('/chat')

@get('/peers')
def dumpsPeers():
    return json.dumps(peers)

def checkPeers():
    global lock
    time.sleep(5)
    while True:
        time.sleep(1)
        newPeers = []
        for p in peers:
            try:
                r = requests.get(p + '/peers')
                newPeers.append(p)
                newPeers.extend(json.loads(r.text))
            except:
                pass

            time.sleep(1)
        with lock:
            peers.extend(list(set(newPeers)))

@get('/chatContent')
def dumpsMsg():
    return json.dumps(list(chatContent))

def getMessagesFrom(p):
    link = "http://" + p + "/chatContent"
    try:
        r = requests.get(link)
        if r.status_code == 200:
            obj = json.loads(r.text)
            setT = set((a, b) for [a,b] in obj)
            return setT
    except:
        print("Connection Error")
    return set([])

def unionMsg():
    while True:
        time.sleep(1)
        newMessage = set([])
        global chatContent
        for p in peers:
            time.sleep(1)
            msgFromPeer = getMessagesFrom(p)
            print(msgFromPeer)
            if msgFromPeer.difference(chatContent):
                newMessage = newMessage.union(msgFromPeer.difference(chatContent))
        chatContent = chatContent.union(newMessage)

thrClient = threading.Thread(target=checkPeers)
thrClient.start()

thrUnionMsg = threading.Thread(target=unionMsg)
thrUnionMsg.start()

# run() starts a built-in development server. It runs on localhost port given in argv[1] and
# serves requests until you hit Control-c.
run(host='localhost', port=int(sys.argv[1]))
