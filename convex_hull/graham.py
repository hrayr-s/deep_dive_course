import dataclasses
from typing import List

import networkx as nx
import matplotlib.pyplot as plt


def draw(points: List['Point']) -> None:
    graph = nx.DiGraph()
    plt.figure(figsize=(10, 6))
    pos = {f'{point.x}, {point.y}': (point.x, point.y) for point in points}
    for point in points:
        graph.add_edge(f'{point.x}, {point.y}', f'{point.x}, {point.y}')
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=2000,
        node_color="skyblue",
        font_size=14,
        font_weight="bold",
        arrowsize=20
    )
    plt.title("Binary Search Tree Visualization")
    plt.show()


@dataclasses.dataclass
class Point:
    x: int
    y: int


def find_bottom_most(points: List['Point']) -> 'Point':
    _min = points[0]

    for point in points:
        if point.y < _min.y:
            _min = point

    return _min


def sort_points_by_angle_for_point(point: Point, points: List[Point]) -> List[Point]:
    the_points_list = points.copy()
    the_points_list.sort(key=lambda _p: _p.x != point.x and (_p.y - point.y) / (_p.x - point.x) or 0)
    return the_points_list


if __name__ == '__main__':
    _points = [
        Point(1, 2),
        Point(5, 2),
        Point(3, 8),
        Point(2, 7),
        Point(4, 5),
        Point(8, 5),
        Point(6, 7),
        Point(8, 9),
        Point(9, 4),
        Point(3, 1),
        Point(3, 3),
        Point(7, 3),
    ]
    draw(_points)
    print(find_bottom_most(_points))
    print(sort_points_by_angle_for_point(find_bottom_most(_points), _points))

