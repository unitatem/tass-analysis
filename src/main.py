from config import graph_path
from graph_analyser import GraphAnalyser
from graph_loader import GraphLoader


def main():
    graph = GraphLoader.load(graph_path)

    graph_analyzer = GraphAnalyser(graph)
    graph_analyzer.print_stats()
    # graph_analyzer.connected_components()
    graph_analyzer.degree()


if __name__ == "__main__":
    main()
    print("END")
