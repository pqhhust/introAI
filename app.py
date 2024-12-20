# app.py
from flask import Flask, render_template, request, jsonify, send_file
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from math import sqrt, radians, cos, sin, asin, sqrt
from io import BytesIO
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class PathFinder:
    def __init__(self):
        # Bounding box coordinates for Lieu Giai
        self.NORTH = 21.04299
        self.SOUTH = 21.03327
        self.EAST = 105.82080
        self.WEST = 105.81277
        self.graph = None
        self.G = None
        self.load_graph()

    def haversine(self, point1, point2):
        """Calculate the great circle distance between two points on the earth"""
        lon1, lat1 = point1
        lon2, lat2 = point2
        
        # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371000  # Radius of earth in meters
        return c * r

    def load_graph(self):
        try:
            graph_path = "lieu_giai_graph_enhanced2.graphml"
            self.G = ox.load_graphml(graph_path)
            
            # Convert graph nodes to (lon, lat) coordinates
            pos = {node: (float(self.G.nodes[node]['x']), float(self.G.nodes[node]['y'])) 
                  for node in self.G.nodes()}
            
            # Build graph structure with actual road distances
            self.graph = {}
            for node in self.G.nodes():
                neighbors = []
                for neighbor in self.G.neighbors(node):
                    if 'length' in self.G.edges[node, neighbor, 0]:
                        dist = float(self.G.edges[node, neighbor, 0]['length'])
                        neighbors.append((pos[neighbor], dist))
                self.graph[pos[node]] = neighbors
            
            logger.info("Graph loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load graph: {str(e)}")
            return False

    def pixel_to_geo(self, pixel_coord, img_width, img_height):
        """Convert pixel coordinates to geographic coordinates."""
        x_ratio = pixel_coord[0] / img_width
        y_ratio = (img_height - pixel_coord[1]) / img_height
        
        lon = self.WEST + (self.EAST - self.WEST) * x_ratio
        lat = self.SOUTH + (self.NORTH - self.SOUTH) * y_ratio
        
        return (lon, lat)

    def geo_to_pixel(self, geo_coord, img_width, img_height):
        """Convert geographic coordinates to pixel coordinates."""
        lon, lat = geo_coord
        
        x_ratio = (lon - self.WEST) / (self.EAST - self.WEST)
        y_ratio = (lat - self.SOUTH) / (self.NORTH - self.SOUTH)
        
        x = int(x_ratio * img_width)
        y = int((1 - y_ratio) * img_height)
        
        return (x, y)

    def find_closest_node(self, point):
        """Find the closest node in the graph to the given point."""
        if not self.graph:
            raise ValueError("Graph not loaded")
            
        return min(self.graph.keys(), 
                  key=lambda node: self.haversine(node, point))

    def a_star(self, start, goal):
        """A* pathfinding algorithm using actual road distances."""
        if not self.graph:
            return []
            
        open_set = {start}
        closed_set = set()
        came_from = {}
        
        g_score = {node: float('inf') for node in self.graph}
        g_score[start] = 0
        
        f_score = {node: float('inf') for node in self.graph}
        f_score[start] = self.haversine(start, goal)

        while open_set:
            current = min(open_set, key=lambda node: f_score[node])
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            open_set.remove(current)
            closed_set.add(current)

            for neighbor, cost in self.graph[current]:
                if neighbor in closed_set:
                    continue
                    
                tentative_g_score = g_score[current] + cost

                if neighbor not in open_set:
                    open_set.add(neighbor)
                elif tentative_g_score >= g_score[neighbor]:
                    continue

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + self.haversine(neighbor, goal)

        return []

pathfinder = PathFinder()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/map')
def get_map():
    try:
        # Create figure with fixed dimensions
        fig, ax = plt.subplots(figsize=(12, 12))
        
        # Plot graph with consistent orientation
        ox.plot_graph(
            pathfinder.G,
            ax=ax,
            node_size=0,
            edge_color='#2E5894',
            edge_linewidth=1.0,
            show=False,
            close=False,
            bgcolor='white'
        )
        
        # Fix orientation using exact bounds
        ax.set_xlim([pathfinder.WEST, pathfinder.EAST])
        ax.set_ylim([pathfinder.SOUTH, pathfinder.NORTH])
        
        # Remove axes and margins
        ax.set_axis_off()
        plt.margins(0,0)
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        
        # Save high-quality image
        img_data = BytesIO()
        plt.savefig(img_data, format='png', dpi=300, bbox_inches='tight', pad_inches=0)
        img_data.seek(0)
        plt.close(fig)
        
        return send_file(img_data, mimetype='image/png')
        
    except Exception as e:
        logger.error(f"Error generating map: {str(e)}")
        return "Error generating map", 500

@app.route('/find_path', methods=['POST'])
def find_path():
    try:
        data = request.get_json()
        
        img_width = data['width']
        img_height = data['height']
        start_pixel = tuple(data['start'])
        end_pixel = tuple(data['end'])
        
        # Convert clicked points to geographic coordinates
        start_geo = pathfinder.pixel_to_geo(start_pixel, img_width, img_height)
        end_geo = pathfinder.pixel_to_geo(end_pixel, img_width, img_height)
        
        # Find nearest nodes and calculate path
        start_node = pathfinder.find_closest_node(start_geo)
        end_node = pathfinder.find_closest_node(end_geo)
        path = pathfinder.a_star(start_node, end_node)
        
        # Convert path back to pixel coordinates
        pixel_path = [
            pathfinder.geo_to_pixel(coord, img_width, img_height)
            for coord in path
        ]
        
        return jsonify({
            'success': True,
            'path': pixel_path
        })
    except Exception as e:
        logger.error(f"Error finding path: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)