class VC:
    def __init__(self, name):
        self.name = name
        self.vectorClock = { self.name : 0 }

    # Starting unexplored area...
    def __repr__(self):
        return "V%s" % repr(self.vectorClock)

    # Isso está errado: a ordem não é total
    def __lt__(self, o):
        ks = list(set(self.vectorClock.keys()).union(set(o.vectorClock.keys())))
        ks.sort()
        def nextv(k, vz):
            if k in vz:
                return vz[k]
            else:
                return 0
        for k in ks:
            if nextv(k, self.vectorClock) > nextv(k, o.vectorClock):
                return False
        return True
    # Ending unexplored area...

    def increment(self):
        self.vectorClock[self.name] += 1
        return self

    def update(self, sender):
        # Incrementing when receiving a message
        self.increment();
        for (name, vectorClock) in sender.vectorClock.items():
            if name in self.vectorClock:
                if vectorClock >= self.vectorClock[name]:
                    self.vectorClock[name] = vectorClock
            else:
                self.vectorClock[name] = vectorClock

v1 = VC("http://localhost:8080/")
v2 = VC("http://localhost:8081/")
v3 = VC("http://localhost:8082/")

# Incrementing when sending a message
v3.increment()
v2.update(v3)
v2.increment()
v1.update(v2)
v1.increment()
v2.increment()
v2.update(v1)
v3.update(v2)
v3.increment()
v2.increment()
v3.update(v2)
v1.update(v3)
v3.increment()
v1.update(v3)
print("V1", v1)
print("V2", v2)
print("V3", v3)

print("v1 > v2 ?", v1 > v2)
print("v2 > v3 ?", v2 > v3)
print("v1 < v3 ?", v1 < v3)
