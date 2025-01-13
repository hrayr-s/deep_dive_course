from binary_tree.draw_tree import networkx_graph
from tree import Node


if __name__ == '__main__':
    node = Node(72)
    for i in [44, 60, 62, 83, 72, 63, 56, 46, 80, 25, 15, 54, 92, 84, 96, 28, 58]:
        node.add(i)
    networkx_graph(node)

    print("Removing node 83...")
    node.delete(83)
    node.validate_tree() or "Not valid after deleting 83"
    networkx_graph(node)

    print("Mirroring recursively...")
    node.mirror_recursively()
    node.validate_tree() or "Not valid after mirroring recursively"
    networkx_graph(node)

    print("Mirroring in loop...")
    node.mirror_in_loop()
    node.validate_tree() or "Not valid after mirroring recursively"
    networkx_graph(node)
