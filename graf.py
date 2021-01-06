
#BFS

import collections

class Graph:
    def __init__(self):
        self.graph = collections.defaultdict(list)

    def add(self, start, po_prestavi):
        self.graph[start].append(po_prestavi)

    def get(self, key):
        return self.graph[key]

    def print(self):
        for key, value in self.graph.items():
            print(key, ":", value)











