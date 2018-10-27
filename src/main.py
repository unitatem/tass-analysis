from config import graph_path
from graph_analyser import GraphAnalyser
from graph_loader import GraphLoader


def main():
    graph = GraphLoader.load(graph_path)

    analyzer = GraphAnalyser(graph)
    analyzer.print_stats()


if __name__ == "__main__":
    main()
    print("END")
