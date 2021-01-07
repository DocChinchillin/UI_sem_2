
#BFS

import collections

class Graph:
    def __init__(self):
        self.graph = collections.defaultdict(list)
        self.premik = collections.defaultdict(tuple)

    def add(self, start, po_prestavi):
        self.graph[start].append(po_prestavi)

    def get(self, key):
        return self.graph[key]

    def addPremik(self, start, after, pr):
        self.premik[(start, after)] = pr

    def getPremik(self, start, after):
        return self.premik[(start, after)]

    def print(self):
        for key, value in self.graph.items():
            print(key, ":", value)











