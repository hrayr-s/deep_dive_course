import dataclasses
from decimal import Decimal
from typing import Optional, Tuple, List, Union

from binary_tree.draw_tree import networkx_graph, draw_points_lists


@dataclasses.dataclass(frozen=True)
class Point:
    """
    Point in 2D system
    """
    x: int
    y: int

    def __len__(self) -> int:
        """
        Corresponds to the N dimensional points.
        In current system the N is equal to two (2). So we constantly return 2
        :return:
        """
        return 2

    def __hash__(self):
        return hash((self.x, self.y))

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y

    @staticmethod
    def from_coord_tuple(coord_tuple: Tuple[int, int]) -> "Point":
        return Point(*coord_tuple)

    @staticmethod
    def from_list(points: List[Tuple[int, int]]) -> List["Point"]:
        return list(map(Point.from_coord_tuple, points))


def distance_between(point1: Point, point2: Point) -> Union[Decimal, int]:
    """
    Fictive distance between two points.
    This distance can only be used for comparison. It is not actual distance between two points.
    :param point1:
    :param point2:
    :return:
    """
    return sum(abs(point1[i] - point2[i]) for i in range(len(point1)))


@dataclasses.dataclass()
class Node:
    point: Point
    level: int = 0
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    parent: Optional['Node'] = None

    @property
    def value(self):
        return f"(%s)" % ','.join(str(self.point[i]) for i in range(len(self.point)))

    @classmethod
    def new(cls, point: Point, parent: Optional['Node'] = None, level: int = 0) -> 'Node':
        return Node(point=point, parent=parent, level=level)

    def add(self, point: 'Point', level: int = 0) -> 'Node':
        """
        adds new point to the tree
        :param point:
        :param level:
        :return: `Node` its self
        """
        compared_result = point[level%2] < self.point[level%2]

        level += 1

        if compared_result:
            if self.left is None:
                self.left = Node.new(point=point, parent=self, level=level)
            else:
                self.left.add(point, level)
        else:
            if self.right is None:
                self.right = Node.new(point=point, parent=self, level=level)
            else:
                self.right.add(point, level)

        return self

    def _side_by_point_and_level(self, point):
        if point[self.level % 2] < self.point[self.level % 2]:  # [0] => Point.__getitem__(0)
            return self.left, self.right

        return self.right, self.left

    def nearest_neighbor(
            self,
            point: 'Point',
            # using lists (mutable object) to imitate C like modify by reference
            current_min: List[Union[Decimal, int]],
            current_node: List['Node'],
    ):
        assert isinstance(current_min, list)
        assert isinstance(current_node, list)

        if current_min[0] >= distance_between(point, self.point):
            current_min[0] = distance_between(point, self.point)
            current_node[0] = self

        direct_node, indirect_node = self._side_by_point_and_level(point)
        if direct_node is not None:
            direct_node.nearest_neighbor(point=point, current_min=current_min, current_node=current_node)

        if abs(point[self.level % 2] - self.point[self.level % 2]) < current_min[0]:
            if indirect_node is not None:
                indirect_node.nearest_neighbor(point=point, current_min=current_min, current_node=current_node)

        # The code below is the opened variant of the code above as if we checked sides statically.
        # The Code repeats. So, decided to use names `direct_node` and `indirect_node`
        #   - `direct_node` is the node we must search in
        #   - `indirect_node` is the other branch we can look but only if the aimed point is closer to its plane.

        # if point[self.level % 2] < self.point[self.level % 2]:  # [0] => Point.__getitem__(0)
        #     if self.left is not None:
        #         self.left.nearest_neighbor(point=point, current_min=current_min, current_node=current_node)
        #
        #     if abs(point[self.level % 2] - self.point[self.level % 2]) < current_min[0]:
        #         if self.right is not None:
        #             self.right.nearest_neighbor(point=point, current_min=current_min, current_node=current_node)
        # else:
        #     if self.right is not None:
        #         self.right.nearest_neighbor(point=point, current_min=current_min, current_node=current_node)
        #
        #     if abs(point[self.level % 2] - self.point[self.level % 2]) < current_min[0]:
        #         if self.left is not None:
        #             self.left.nearest_neighbor(point=point, current_min=current_min, current_node=current_node)

if __name__ == "__main__":
    # list of raw coordinates
    points_list = [(2,3), (1,9), (8,7), (5,1), (4,8), (3,2), (7,4), (9,6)]

    # visualize the points on coordinate system
    draw_points_lists(Point.from_list(points_list))

    # construct the tree
    root = Node.new(point=Point.from_coord_tuple(points_list[0]))
    for _p in Point.from_list(points_list[1:]):
        root.add(_p)

    # visualize the tree
    networkx_graph(root)

    # aim a point to find nearest
    aim_point = Point(6, 5)

    # use lists to work with referenced variables
    current_min_val = [distance_between(point1=aim_point, point2=root.point)]
    node_reference = [root]

    # run finder
    root.nearest_neighbor(point=aim_point, current_min=current_min_val, current_node=node_reference)

    # result
    print(node_reference[0].point)
    print(current_min_val)
