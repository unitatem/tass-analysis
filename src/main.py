from config import graph_path, pajek_export_path
from graph_analyser import GraphAnalyser
from graph_loader import GraphLoader


def main():
    graph = GraphLoader.load(graph_path)
    # GraphLoader.export_pajek(graph, pajek_export_path)

    graph_analyzer = GraphAnalyser(graph)
    graph_analyzer.print_stats()
    graph_analyzer.connected_components()

    graph_analyzer.degree_plot()
    graph_analyzer.degree_rank_log_regression()
    graph_analyzer.hill_plot()


if __name__ == "__main__":
    main()
    print("END")
