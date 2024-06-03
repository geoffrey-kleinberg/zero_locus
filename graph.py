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
                neighbor_count_not_in_F = 0
                neighbor_not_in_F = None
                for neighbor in self.get_neighbors(v):
                    if not neighbor in F:
                        neighbor_count_not_in_F += 1
                        neighbor_not_in_F = neighbor

                if neighbor_count_not_in_F == 1:
                    F.add(neighbor_not_in_F)
                    stable = False

            if stable:
                break
        return F
    
    def s_hat(self, initial_set=set(())):
        for v in initial_set:
            if v not in self.graph:
                return None
            
        values = {}
        for v in self.graph:
            values[v] = None

        F = self.skew_zero_forcing(initial_set)
        
        for v in F:
            values[v] = 0
            
        while True:
            this_round = set(())
            for v in self.graph:
                if values[v] is None:
                    this_round.add(v)
                    values[v] = 1
                    break
            
            contradiction = False


            while True:
                stable2 = True
                for v in self.graph:
                    neighbors = self.get_neighbors(v)
                    neighbor_sum = 0
                    count_none_neighbors = 0
                    none_neighbor = None
                    for neighbor in neighbors:
                        if values[neighbor] is None:
                            count_none_neighbors += 1
                            none_neighbor = neighbor
                        else:
                            neighbor_sum += values[neighbor]
                    
                    if count_none_neighbors == 1:
                        values[none_neighbor] = -1 * neighbor_sum
                        this_round.add(none_neighbor)
                        stable2 = False

                    if count_none_neighbors == 0 and neighbor_sum != 0:
                        contradiction = True
                        break
                
                if stable2:
                    break

            if contradiction:
                for v in this_round:
                    values[v] = 0
                    F.add(v)

            if list(values.values()).count(None) == 0:
                break

        return F
