import logging

import networkx as nx

logging.basicConfig(level=logging.DEBUG)


class GraphAnalyser:
    def __init__(self, graph):
        self.graph = graph

    def print_stats(self):
        logging.info("Graph stats:")
        self._stats(self.graph)

    @staticmethod
    def _stats(g):
        logging.info("nodes_cnt (rzad) = {nodes} edges_cnt (rozmiar) = {edges}"
                     .format(nodes=g.number_of_nodes(),
                             edges=g.number_of_edges()))

    def connected_components(self):
        logging.info("Connected components:")
        logging.info("total = {cnt}".format(cnt=nx.number_connected_components(self.graph)))

        max_sub_graphs = max(nx.connected_component_subgraphs(self.graph), key=len)
        self._stats(max_sub_graphs)

    def all_connected_components(self):
        logging.info("All connected components:")
        logging.info("total = {cnt}".format(cnt=nx.number_connected_components(self.graph)))

        sub_graphs = nx.connected_component_subgraphs(self.graph)
        for sg in sub_graphs:
            self._stats(sg)
