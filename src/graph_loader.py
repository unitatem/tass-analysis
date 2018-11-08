import networkx as nx


class GraphLoader:
    @staticmethod
    def load(path):
        print("Start reading")
        graph = nx.read_edgelist(path,
                                 delimiter=',',
                                 create_using=nx.Graph,
                                 nodetype=int,
                                 encoding="utf-8")
        print("Finish reading")
        return graph
