import osmnx as ox
import matplotlib.pyplot as plt
from PIL import Image

def generate_map_image():
    # Định nghĩa bounding box cho Liễu Giai
    NORTH = 21.04299
    SOUTH = 21.03327
    EAST = 105.82080
    WEST = 105.81277

    # Tạo bounding box
    bbox = (NORTH, SOUTH, EAST, WEST)

    # Tải dữ liệu bản đồ với bounding box
    graph = ox.graph.graph_from_bbox(*bbox, network_type="all", simplify=True)
    
    # Plot bản đồ
    fig, ax = ox.plot_graph(
        graph,
        bgcolor='white',
        node_size=0,
        edge_color='#2E5894',
        edge_linewidth=1.0,
        show=False,
        close=False,
    )
    
    # Tùy chỉnh trục để khớp với bounding box
    ax.set_xlim([WEST, EAST])
    ax.set_ylim([SOUTH, NORTH])
    ax.set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    
    # Lưu ảnh bản đồ
    output_file = "lieu_giai_map.png"
    plt.savefig(output_file, format="png", dpi=300, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    # Kiểm tra và cắt viền trắng
    img = Image.open(output_file)
    img_cropped = img.crop(img.getbbox())
    img_cropped.save(output_file)

    print(f"Bản đồ đã được lưu tại: {output_file}")

if __name__ == "__main__":
    generate_map_image()
