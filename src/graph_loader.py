import logging

import networkx as nx

logging.basicConfig(level=logging.DEBUG)


class GraphLoader:
    def load(path):
        logging.info("Start reading")
        graph = nx.read_edgelist(path,
                                 delimiter=',',
                                 create_using=nx.Graph,
                                 nodetype=int,
                                 encoding="utf-8")
        logging.info("Finish reading")
        return graph
