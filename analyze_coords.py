# analyze_coords.py
import networkx as nx
import osmnx as ox

def analyze_coordinates():
    # Load the graph
    graph_path = "lieu_giai_graph.graphml"
    G = ox.load_graphml(graph_path)
    
    # Extract all coordinates
    lats = []
    lons = []
    
    for node, data in G.nodes(data=True):
        if 'y' in data and 'x' in data:
            lats.append(float(data['y']))
            lons.append(float(data['x']))
    
    # Get exactly 4 bounds
    north = max(lats)
    south = min(lats)
    east = max(lons)
    west = min(lons)
    
    # Print the 4 coordinates in order: North East South West
    print("\nBounding Box Coordinates (North East South West):")
    print(f"{north:.5f} {east:.5f} {south:.5f} {west:.5f}")

if __name__ == "__main__":
    analyze_coordinates()