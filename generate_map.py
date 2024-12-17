# generate_map.py
from math import radians, sin, cos, sqrt, asin
import folium
from folium.plugins import MousePosition

class MapGenerator:
    def __init__(self, center_lat, center_lng, zoom_start=13):
        self.map = folium.Map(location=[center_lat, center_lng], zoom_start=zoom_start, tiles='OpenStreetMap', name="map", attr="id:map")

    def add_marker(self, lat, lng, popup_text=None):
        folium.Marker([lat, lng], popup=popup_text).add_to(self.map)

    def save_map(self, filename="map.html"):
        self.map.save(filename)

# Coordinates for Lieu Giai
# (Lấy giá trị trung bình của các tọa độ cực trị đã phân tích từ analyze_coords.py)
center_lat = (21.04299 + 21.03327) / 2
center_lng = (105.82080 + 105.81277) / 2

# Example usage:
map_generator = MapGenerator(center_lat=center_lat, center_lng=center_lng)
map_generator.add_marker(center_lat, center_lng, "Center of Lieu Giai")
MousePosition().add_to(map_generator.map)  # Add MousePosition plugin for coordinate display
map_generator.save_map()
print("Map generated successfully as map.html")