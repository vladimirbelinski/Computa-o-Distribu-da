# -*- coding: utf-8 -*-
# Filename: main.py
# Author: Vladimir Belinski
# Description: server side of a chat application (with multicast). In this
# version a vector is used to order the messages.

from bottle import run, get, post, view, request, route, static_file, template, redirect
from frozendict import frozendict
import bottle
import json
import threading
import requests
import time
import sys

# From Colouris et al.: a vector clock for a system of N processes is an array
# of N integers. Each process keeps its own vector clock, V_i, which it uses to
# timestamp local events. Processes piggyback vector timestamps on the messages
# they send to one another, and there are simple rules for updating the clocks:
# VC1: initially, V_i[j] = 0, for i,j = 1, 2, ..., N
# VC2: just before p_i timestamps an event, it sets V_i[j] := V_i[i] + 1
# VC3: p_i includes the value t = V_i in every message it sends
# VC4: when p_i receives a timestamp t in a message it sets
#      V_i[j] := max(V_i[j], t[j]), for j = 1, 2, ..., N. Taking the
#      componentwise maximum of two vectors timestamps in this way is known as a
#      merge operation.
class VC:
    def __init__(self, name):
        self.name = name
        self.vectorClock = { self.name : 0 }

    # repr(object) returns a string containing a printable representation of an
    # object. A class can control what this function returns for its instances
    # by defining a __repr__() method.
    def __repr__(self):
        return "V%s" % repr(self.vectorClock)

    def increment(self):
        self.vectorClock[self.name] += 1
        return self

    def update(self, sender):
        # Incrementing when receiving a message
        self.increment();
        for (key, value) in sender.items():
            if key not in vc.vectorClock or vc.vectorClock[key] < sender[key]:
                vc.vectorClock[key] = value

chatContent = set([])
peers = ['http://localhost:' + p for p in sys.argv[2:]]
lock = threading.Lock()
vc = VC('http://localhost:' + sys.argv[1])

# The route() decorator links an URL path to a callback function, and adds a new
# route to the default application.

# Static files such as images or CSS files are not served automatically. It's
# necessary to add a route and a callback to control which files get served  and
# where to find them.The static_file() function is a helper to serve files in a
# safe and convenient way.To serve files in subdirectories it's necessary to use
# the :path filter in the wildcard: <filepath:path>.
@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

def lt(a, b):
    keys = list(set(a[2].keys()).union(b[2].keys()))
    keys.sort()
    a = tuple(a[2][k] if k in a[2] else 0 for k in keys)
    b = tuple(b[2][k] if k in b[2] else 0 for k in keys)
    for i in range(0, len(a) - 1):
        if a < b: return True
        if b < a: return False
    return False

allMsg = []

def sortMsg():
    global allMsg
    for i in range(1, len(allMsg)):
        key = allMsg[i]
        k = i
        while k > 0 and lt(key, allMsg[k - 1]):
            allMsg[k] = allMsg[k - 1]
            k -= 1
            allMsg[k] = key

# Just redirecting 'localhost:port/' to 'localhost:port/chat'
@route('/')
def chatRedirect():
    redirect('/chat')

# The HTTP protocol defines several request methods for different tasks. GET is
# the default for all routes with no other method specified. These routes will
# match GET requests only.To handle other methods such as POST add a method
# keyword argument to the route() decorator or use one of the five alternative
# decorators: get(), post(), put(), delete() or patch().

# To render a template you can use the template() function or the view()
# decorator. All you have to do is to provide the name of the template and the
# variables you want to pass to the template as keyword arguments. Bottle will
# look for templates in the ./views/ folder or any folder specified in the
# bottle TEMPLATE_PATH list. The view() decorator allows you to return a
# dictionary with the template variables instead of calling template().

@get('/chat')
@view('chat')
def chat():
    global allMsg
    name = request.query.name
    allMsg = list(chatContent)
    sortMsg()
    return dict(name=name, chatContent=list(allMsg))

@post('/send')
def sendMessage():
    name = request.forms.getunicode('name')
    message = request.forms.getunicode('message')
    if name != None and message != None:
        vc.increment()
        aux = (name, message, frozendict(vc.vectorClock))
        chatContent.add(aux)
        redirect('chat?name=' + name)
    else:
        redirect('/chat')

# json.dumps(obj, fp, ...) serialize obj as a JSON formatted stream to fp
# (a .write()-supporting file-like object) using a conversion table that can be
# found here: https://docs.python.org/3/library/json.html#py-to-json-table

# dumpsPeers() returns a 'JSON list' with the peers known
@get('/peers')
def dumpsPeers():
    return json.dumps(peers)

def checkPeers():
    global lock
    # time.sleep() for debugging
    time.sleep(5)
    while True:
        time.sleep(1)
        newPeers = []
        for p in peers:
            try:
                # requests.get(p + '/peers') will return the peers known by host
                # 'p' if this server is not down. E.g.: if server 8080 knows
                # 8081 and 8082 it will be returned ["localhost:8080",
                # "localhost:8082"]
                r = requests.get(p + '/peers')
                # if this line is reached it means that p is not down
                newPeers.append(p)
                # list.extend(seq): the method extend() appends the contents of
                # seq to list json.loads(fp, ...) deserialize fp (a .write()-
                # supporting file-like object containing a JSON document) to a
                # Python object.
                newPeers.extend(json.loads(r.text))
            except:
                pass

            time.sleep(1)
        with lock:
            # newPeers is transformed into a 'set' to eliminate duplicates.
            # After that it is transformed into a list again and extended to
            # peers
            peers.extend(list(set(newPeers)))

@get('/chatContent')
# dumpsMsg() returns a 'JSON list' with the messages known
def dumpsMsg():
    return json.dumps([(name, message, dict(vectorClock)) for (name, message, vectorClock) in chatContent])

# getMessagesFrom(p) get the messages from peer 'p'
def getMessagesFrom(p):
    try:
        r = requests.get(p + "/chatContent")
        # 200 OK is the code for success
        if r.status_code == 200:
            pMsg = json.loads(r.text)
            return set((a, b, frozendict(t)) for [a, b, t] in pMsg)

    except:
        print("Connection Error!")
    return set([])

def unionMsg():
    while True:
        time.sleep(1)
        global chatContent
        for p in peers:
            time.sleep(1)
            msgFromPeer = getMessagesFrom(p)
            # if the messages from peer 'p' are different from the messages from
            # chatContent, then, for each new message, the value in the
            # vectorClock is updated (because a new message was received) and
            # the new message(s) are added to chatContent
            for (name, message, vectorClock) in msgFromPeer.difference(chatContent):
                vc.update(vectorClock)
                chatContent.add((name, message, vectorClock))

# thread for peers
thrPeers = threading.Thread(target=checkPeers)
thrPeers.start()

# thread for messages
thrUnionMsg = threading.Thread(target=unionMsg)
thrUnionMsg.start()

# run() starts a built-in development server. It runs on localhost port given in
# argv[1] and serves requests until you hit Control-c.
run(host='localhost', port=int(sys.argv[1]))
