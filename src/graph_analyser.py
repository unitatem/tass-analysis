class GraphAnalyser:
    def __init__(self, graph):
        self.graph = graph

    def print_stats(self):
        print("Nodes = ", self.graph.number_of_nodes())
        print("Edges = ", self.graph.number_of_edges())
