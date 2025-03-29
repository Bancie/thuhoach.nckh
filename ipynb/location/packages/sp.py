class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def printPath(self, parent, j):
        if parent[j] == -1:
            print(j, end=" ")
            return
        self.printPath(parent, parent[j])
        print(j, end=" ")

    def printSolution(self, dist, parent, src):
        print("Vertex\t Distance from Source\tPath")
        for i in range(self.V):
            print(f"{src} -> {i}\t {dist[i]}\t\t", end="")
            self.printPath(parent, i)
            print()

    def minDistance(self, dist, sptSet):
        min_val = 1e7
        min_index = -1
        for v in range(self.V):
            if dist[v] < min_val and not sptSet[v]:
                min_val = dist[v]
                min_index = v
        return min_index

    def dijkstra(self, src):
        dist = [1e7] * self.V
        parent = [-1] * self.V  # Parent array to store shortest path tree
        dist[src] = 0
        sptSet = [False] * self.V

        for _ in range(self.V):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True

            for v in range(self.V):
                if self.graph[u][v] > 0 and not sptSet[v] and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
                    parent[v] = u

        self.printSolution(dist, parent, src)

    def getShortestPath(self, src, dest):
        # This function returns the path from src to dest as a list
        dist = [1e7] * self.V
        parent = [-1] * self.V
        dist[src] = 0
        sptSet = [False] * self.V

        for _ in range(self.V):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True

            for v in range(self.V):
                if self.graph[u][v] > 0 and not sptSet[v] and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
                    parent[v] = u

        # Reconstruct path
        path = []
        crawl = dest
        while crawl != -1:
            path.insert(0, crawl)
            crawl = parent[crawl]

        return path, dist[dest]