class Graph:
    def __init__(self):
        self.graph = {}
        self.size = 0

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = set(())
            self.size += 1
        self.graph[u].add(v)

    def get_neighbors(self, node):
        return self.graph[node]
    
    def get_dist_two(self, node):
        neighbors = self.get_neighbors(node)
        dist_two = set(())
        for neighbor in neighbors:
            dist_two = dist_two.union(self.get_neighbors(neighbor))
        return dist_two
    
    @staticmethod
    def make_from_file(filename):
        g = Graph()
        with open(filename, 'r') as f:
            for line in f:
                u, neighbors = line.split(':')
                for v in neighbors.strip().split(','):
                    g.add_edge(u, v)
                    g.add_edge(v, u)

        return g
    
    def skew_zero_forcing(self, initial_set=set(())):
        for v in initial_set:
            if v not in self.graph:
                return None
            
        F = initial_set.copy()
        while True:
            stable = True
            for v in self.graph:
                if v not in F and len(self.get_neighbors(v).symmetric_difference(F)) == 1:
                    F = F.union(self.get_neighbors(v))
                    stable = False
            if stable:
                break
        return F
