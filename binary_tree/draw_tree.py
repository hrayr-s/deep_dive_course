import networkx as nx
import matplotlib.pyplot as plt


def add_edges(graph, root, parent=None, pos=None, level = 0, x: float = 0.0, dx: float = 1.0):
    pos = pos or {}
    if root is not None:
        pos[root.value] = (x, -level)
        if parent is not None:
            graph.add_edge(parent.value, root.value)
        add_edges(graph, root.left, root, pos, level + 1, x - dx, dx / 2)
        add_edges(graph, root.right, root, pos, level + 1, x + dx, dx / 2)
    return pos


def networkx_graph(root):
    graph = nx.DiGraph()
    positions = add_edges(graph, root)
    # Draw the graph
    plt.figure(figsize=(10, 6))
    nx.draw(graph, positions, with_labels=True, node_size=2000, node_color="skyblue", font_size=14, font_weight="bold",
            arrowsize=20)
    plt.title("Binary Search Tree Visualization")
    plt.show()


def draw_points_lists(points):
    # Extract x and y coordinates from the points list
    x_coords = [p.x for p in points]
    y_coords = [p.y for p in points]

    # Create a scatter plot
    plt.scatter(x_coords, y_coords, color='blue', marker='o')

    # Optionally, annotate each point with its coordinates or index
    for i, p in enumerate(points):
        plt.annotate(f'({p.x}, {p.y})', (p.x, p.y), textcoords="offset points", xytext=(5, 5), ha='center')

    # Label the axes and add a title
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Visualization of Points')

    # Add a grid for easier visualization of positions
    plt.grid(True)

    # Display the plot
    plt.show()
