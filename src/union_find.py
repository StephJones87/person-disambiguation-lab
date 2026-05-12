class UnionFind:

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def add(self, node):

        if node not in self.parent:
            self.parent[node] = node
            self.rank[node] = 0

    def find(self, node):

        self.add(node)

        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])

        return self.parent[node]

    def union(self, node_a, node_b):

        root_a = self.find(node_a)
        root_b = self.find(node_b)

        if root_a == root_b:
            return

        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b

        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a

        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1