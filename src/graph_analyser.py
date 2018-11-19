import time
from collections import Counter

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from sklearn import linear_model

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
        start = time.time()
        print("total = {cnt}".format(cnt=nx.number_connected_components(self.graph)))

        max_sub_graphs = max(nx.connected_component_subgraphs(self.graph), key=len)
        print("TIME:", time.time() - start)
        self._stats(max_sub_graphs)

    def all_connected_components(self):
        print("All connected components:")
        print("total = {cnt}".format(cnt=nx.number_connected_components(self.graph)))

        sub_graphs = nx.connected_component_subgraphs(self.graph)
        for sg in sub_graphs:
            self._stats(sg)

    def degree_plot(self):
        print("Degree rank plot")
        degree_sequence = sorted([degree for node, degree in self.graph.degree()])
        degree_cnt = dict(Counter(degree_sequence))
        degree_cnt = [(d, degree_cnt.get(d)) for d in degree_cnt.keys()]
        print(degree_cnt)

        plt.plot(*zip(*degree_cnt), ".")
        plt.title("Degree distribution plot")
        plt.xlabel("degree")
        plt.ylabel("count")
        plt.grid()
        plt.show()

    def degree_rank_log_regression(self):
        print("Rank plot")
        degree_sequence = sorted([degree for node, degree in self.graph.degree()])
        degree_cnt = dict(Counter(degree_sequence))
        print(degree_cnt)

        xx = list(degree_cnt.keys())
        yy = list(degree_cnt.values())
        assert len(xx) == len(yy)

        xx, yy = self._log_binning(xx, yy, 20)

        s = np.sum(yy)
        cdf = np.cumsum(yy)
        ccdf = s - cdf
        yy = ccdf

        xx = np.array(xx)
        yy = np.array(yy) + 1
        samples_cnt = len(yy)

        x_log = np.log10(xx)
        x_log.shape = (samples_cnt, 1)

        y_log = np.log10(yy)
        y_log.shape = (samples_cnt, 1)

        model = linear_model.LinearRegression()
        model.fit(x_log, y_log)

        print('DEBUG coefficients: ', model.coef_)
        print('DEBUG intercept: ', model.intercept_)

        a = model.intercept_
        b = model.coef_[0][0]

        # minus because exponential function = C * exp(-alpha)
        alpha = -b
        print("alpha: ", alpha)

        if enable_plotter:
            plt.plot(x_log, y_log, ".")

            x = [x_log[0], x_log[-1]]
            y = [xi * b + a for xi in x]
            plt.plot(x, y, "r-")

            plt.title("Degree rank plot")
            plt.ylabel("ccdf")
            plt.xlabel("rank")
            plt.grid()
            plt.show()

    def _log_binning(self, xx, yy, bins_cnt):
        x_min = np.min(xx)
        x_max = np.max(xx)
        thresholds = np.logspace(np.log10(x_min), np.log10(x_max), bins_cnt)

        x_bin = list()
        y_bin = list()
        x_begin = 0
        x_end = 0
        thresholds[-1] += 1
        thresholds = thresholds[1:]
        for i in range(len(thresholds)):
            while x_end < len(xx) and xx[x_end] < thresholds[i]:
                x_end += 1
            if x_begin == x_end:
                continue
            x = np.mean(xx[x_begin:x_end])
            y = np.mean(yy[x_begin:x_end])

            x_bin.append(x)
            y_bin.append(y)

            x_begin = x_end
        return x_bin, y_bin

    def hill_plot(self):
        print("Hill plot")

        k_alpha = list()
        degree_sequence = sorted([degree for node, degree in self.graph.degree()])
        degree_cnt = dict(Counter(degree_sequence))
        degree_cnt = sorted(list(degree_cnt.values()), reverse=True)
        print(degree_cnt)

        nodes_cnt = len(degree_cnt)
        for consider_cnt in range(2, nodes_cnt + 1):
            x = np.sum(np.log(degree_cnt[:consider_cnt]))
            gamma = x / consider_cnt - np.log(degree_cnt[consider_cnt - 1])
            alpha = 1.0 + 1.0 / gamma

            if consider_cnt % 25 == 0 and consider_cnt >= 100:
                print("alpha(k = {k}) = {alpha}".format(k=consider_cnt,
                                                        alpha=alpha))
            k_alpha.append(alpha)

        if enable_plotter:
            plt.plot(k_alpha, 'b')
            plt.title("Hill diagram")
            plt.ylabel("alpha")
            plt.xlabel("k")
            plt.grid()
            plt.show()
