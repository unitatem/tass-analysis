import time
import networkx as nx


class GraphLoader:
    @staticmethod
    def load(path):
        print("Start reading")
        start = time.time()
        graph = nx.read_edgelist(path,
                                 delimiter=',',
                                 create_using=nx.Graph,
                                 nodetype=int,
                                 encoding="utf-8")
        print("TIME:", time.time() - start)
        print("Finish reading")
        return graph

    @staticmethod
    def export_pajek(graph, path):
        print("Start pajek export")
        start = time.time()
        nx.write_pajek(graph, path)
        print("TIME:", time.time() - start)
        print("Finish pajek export")
