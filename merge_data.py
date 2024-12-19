import networkx as nx

file1 = "D:\introAI\lieu_giai_graph.graphml"
file2 = "D:\introAI\lieu_giai_graph_detailed.graphml"
output_file = "D:\introAI\lieu_giai_graph_merged.graphml"

G1 = nx.read_graphml(file1)
G2 = nx.read_graphml(file2)

for node, data in G2.nodes(data=True):
    if node not in G1:  
        G1.add_node(node, **data)

for edge in G2.edges(data=True):
    if not G1.has_edge(edge[0], edge[1]): 
        G1.add_edge(edge[0], edge[1], **edge[2])


nx.write_graphml(G1, output_file)

print(f"File hợp nhất lưu tại: {output_file}")
