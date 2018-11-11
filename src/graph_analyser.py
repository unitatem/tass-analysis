import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from config import enable_plotter
from sklearn import linear_model


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

    def degrees_plot(self):
        print("Degrees plot")

        degree_cnt = dict()
        degree_sequence = self.get_degree_sequence()
        for d in degree_sequence:
            cnt = degree_cnt.get(d, 0)
            degree_cnt[d] = cnt + 1

        degree_cnt = [(d, c) for d, c in degree_cnt.items()]
        degree_cnt = sorted(degree_cnt, key=lambda x: x[0])

        plt.scatter(*zip(*degree_cnt))
        plt.title("Degree distribution plot")
        plt.xlabel("degree")
        plt.ylabel("count")
        plt.grid()
        plt.show()

    def get_degree_sequence(self):
        if self._degree_sequence is None:
            self._degree_sequence = sorted([degree for node, degree in self.graph.degree()], reverse=True)
        return self._degree_sequence

    def rank_plot(self):
        print("Rank plot")

        xx, yy = self._get_binned_degrees()
        assert len(xx) == len(yy)
        samples_cnt = len(yy)

        x_log = np.log(xx)
        assert len(x_log) == samples_cnt
        x_log.shape = (samples_cnt, 1)

        y_log = np.log(yy)
        y_log.shape = (samples_cnt, 1)

        model = linear_model.LinearRegression()
        model.fit(x_log, y_log)

        print('DEBUG coefficients: ', model.coef_)
        print('DEBUG intercept: ', model.intercept_)

        a = model.intercept_
        b = model.coef_[0][0]

        # minus because exponential function equals C * exp(-alpha)
        alpha = -b
        print("alpha: ", alpha)

        if enable_plotter:
            plt.plot(x_log, y_log, ".")

            x = [x_log[0], x_log[-1]]
            y = [xi * b + a for xi in x]
            plt.plot(x, y, "r-")

            plt.title("Degree rank plot")
            plt.ylabel("degree")
            plt.xlabel("rank")
            plt.grid()
            plt.show()

    def _get_binned_degrees(self):
        degrees = self.get_degree_sequence()
        size = len(degrees)
        threshold = np.logspace(0, np.log10(size), num=10)

        xx = list()
        yy = list()
        for i in range(0, len(threshold) - 1):
            lo = int(threshold[i])
            hi = int(threshold[i + 1])
            v = np.average(degrees[lo:hi])

            xx.append(0.5 * (lo + hi))
            yy.append(v)
        return xx, yy

    def hill_plot(self):
        print("Hill plot")

        k_alpha = list()
        degrees = self.get_degree_sequence()
        nodes_cnt = len(degrees)
        for consider_cnt in range(2, nodes_cnt + 1):
            if consider_cnt % 8000 == 0:
                print("progress: %.2f" % (consider_cnt / nodes_cnt))

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
            plt.grid()
            plt.show()
