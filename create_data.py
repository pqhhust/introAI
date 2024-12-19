import osmnx as ox

north, south, east, west = 21.04299, 21.03327, 105.82080, 105.81277
bbox = (north, south, east, west)

G = ox.graph.graph_from_bbox(bbox, network_type='all', retain_all=True, simplify=False )

ox.save_graphml(G, filepath='lieu_giai_graph_detailed.graphml')

print("Đã tạo file lieu_giai_graph_detailed.graphml")

