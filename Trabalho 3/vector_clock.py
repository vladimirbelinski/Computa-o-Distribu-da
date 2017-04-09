# From Colouris et al.: a vector clock for a system of N processes is an array of N
# integers. Each process keeps its own vector clock, V_i, which it uses to timestamp
# local events. Processes piggyback vector timestamps on the messages they send to one
# another, and there are simple rules for updating the clocks:
# VC1: initially, V_i[j] = 0, for i,j = 1, 2, ..., N
# VC2: just before p_i timestamps an event, it sets V_i[j] := V_i[i] + 1
# VC3: p_i includes the value t = V_i in every message it sends
# VC4: when p_i receives a timestamp t in a message it sets V_i[j] := max(V_i[j], t[j]),
#      for j = 1, 2, ..., N. Taking the componentwise maximum of two vectors timestamps
#      in this way is known as a merge operation.
class VC:
    def __init__(self, name):
        self.name = name
        self.vectorClock = { self.name : 0 }

    # repr(object) returns a string containing a printable representation of an object.
    # A class can control what this function returns for its instances by defining a
    # __repr__() method.
    def __repr__(self):
        return "V%s" % repr(self.vectorClock)

    # Isso está errado: a ordem não é total
    # object.__lt__(self, other) is a "rich comparison" method. x < y calls x.__lt__(y)
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

    def increment(self):
        self.vectorClock[self.name] += 1
        return self

    def update(self, sender):
        # Incrementing when receiving a message
        self.increment();
        for (key, value) in sender.vectorClock.items():
            if key in self.vectorClock:
                if value >= self.vectorClock[key]:
                    self.vectorClock[key] = value
            else:
                self.vectorClock[key] = value

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
