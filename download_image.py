import osmnx as ox
import networkx as nx
import os

def download_lieu_giai_map():
    # Download the graph with all types of roads
    # Note: graph_from_bbox expects positional arguments in order: north, south, east, west
    graph = ox.graph_from_place(
        query="Liễu Giai, Hanoi, Vietnam",  # Positional arguments in correct order
        network_type='all'
    )
    
    # Save the graph to a local file
    graph_path = "lieu_giai_graph.graphml"
    ox.save_graphml(graph, graph_path)
    print(f"Map saved to {graph_path}")

if __name__ == "__main__":
    download_lieu_giai_map()