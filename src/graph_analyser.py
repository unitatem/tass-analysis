import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from config import enable_plotter


class GraphAnalyser:
    def __init__(self, graph):
        self.graph = graph
        self._degree_sequence = None

    def print_stats(self):
        print("Graph stats:")
        self._stats(self.graph)

    @staticmethod
    def _stats(g):
        print("nodes_cnt (rzad) = {nodes} edges_cnt (rozmiar) = {edges}"
              .format(nodes=g.number_of_nodes(),
                      edges=g.number_of_edges()))

    def connected_components(self):
        print("Connected components:")
        print("total = {cnt}".format(cnt=nx.number_connected_components(self.graph)))

        max_sub_graphs = max(nx.connected_component_subgraphs(self.graph), key=len)
        self._stats(max_sub_graphs)

    def all_connected_components(self):
        print("All connected components:")
        print("total = {cnt}".format(cnt=nx.number_connected_components(self.graph)))

        sub_graphs = nx.connected_component_subgraphs(self.graph)
        for sg in sub_graphs:
            self._stats(sg)

    def rank_plot(self):
        print("Rank plot")

        if enable_plotter:
            plt.loglog(self.get_degree_sequence(), 'b')
            plt.title("Degree rank plot")
            plt.ylabel("degree")
            plt.xlabel("rank")
            plt.show()

        return 0

    def get_degree_sequence(self):
        if self._degree_sequence is None:
            self._degree_sequence = sorted([degree for node, degree in self.graph.degree()], reverse=True)
        return self._degree_sequence

    def hill_plot(self):
        print("Hill plot")

        k_alpha = list()
        degrees = self.get_degree_sequence()
        nodes_cnt = len(degrees)
        for consider_cnt in range(1, nodes_cnt + 1):
            if consider_cnt % 1000 == 0:
                print("progress:", consider_cnt / nodes_cnt)

            x = np.sum(np.log(degrees[nodes_cnt - consider_cnt:]))
            gamma = x / consider_cnt - np.log(degrees[nodes_cnt - consider_cnt])

            if gamma == 0.0:
                k_alpha.append(0.0)
                continue
            alpha = 1.0 + 1.0 / gamma
            k_alpha.append(alpha)

        if enable_plotter:
            plt.plot(k_alpha, 'b')
            plt.title("Hill diagram")
            plt.ylabel("alpha")
            plt.xlabel("k")
            plt.show()
