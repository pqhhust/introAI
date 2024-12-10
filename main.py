import osmnx as ox
import folium
import networkx as nx
from streamlit_folium import st_folium
import streamlit as st

# 1. Tải dữ liệu đồ thị đường phố phường Liễu Giai
place_name = "Liễu Giai, Hanoi, Vietnam"
graph = ox.graph_from_place(place_name, network_type="all")

# Chuyển đổi đồ thị sang định dạng GeoDataFrame
nodes, edges = ox.graph_to_gdfs(graph)

# 2. Tạo giao diện với Streamlit
st.title("Tìm đường đi ngắn nhất - Phường Liễu Giai")

# Hiển thị bản đồ
m = folium.Map(location=[21.0359, 105.8121], zoom_start=15)  # Tọa độ trung tâm phường Liễu Giai
folium.GeoJson(edges).add_to(m)

# Người dùng chọn hai điểm
st.write("Chọn hai điểm trên bản đồ:")
map_data = st_folium(m, height=500, width=700)

if map_data and map_data["last_clicked"]:
    st.write("Điểm đã chọn:")
    st.json(map_data["last_clicked"])  # Hiển thị thông tin điểm đã chọn

# Nếu người dùng đã chọn hai điểm
if "points" not in st.session_state:
    st.session_state.points = []

if st.button("Lưu điểm đã chọn"):
    if map_data and "last_clicked" in map_data:
        lat, lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
        st.session_state.points.append((lat, lon))
        st.success(f"Điểm ({lat}, {lon}) đã được lưu!")

# Nếu có đủ hai điểm, tính toán đường đi ngắn nhất
if len(st.session_state.points) == 2:
    st.write("Hai điểm đã chọn:", st.session_state.points)

    # Tìm nút gần nhất cho từng điểm
    origin_node = ox.nearest_nodes(graph, X=st.session_state.points[0][1], Y=st.session_state.points[0][0])
    destination_node = ox.nearest_nodes(graph, X=st.session_state.points[1][1], Y=st.session_state.points[1][0])

    # Tìm đường đi ngắn nhất
    shortest_route = nx.shortest_path(graph, origin_node, destination_node, weight="length")

    # Vẽ đường đi trên bản đồ
    route_map = ox.plot_route_folium(graph, shortest_route, route_color="blue", route_linewidth=5)
    st.write("Đường đi ngắn nhất:")
    st_folium(route_map, height=500, width=700)

# Nút reset để chọn lại điểm
if st.button("Reset"):
    st.session_state.points = []
    st.success("Đã reset các điểm đã chọn.")
