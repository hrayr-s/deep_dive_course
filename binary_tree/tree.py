import dataclasses
from typing import Optional, Union, List

from binary_tree.draw_tree import networkx_graph
from execution_time import execution_time

LEFT = False
RIGHT = True
ASCENDING = 'ASC'
DESCENDING = 'DESC'

@dataclasses.dataclass
class Node:
    value: int
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    parent: Optional['Node'] = None
    parent_side: Optional['int'] = None
    ordering: str = ASCENDING
    elements_count: int = 0

    @property
    def ascending(self):
        """
        Is current node ordering ascending
        :return:
        """
        return ASCENDING == self.ordering

    @property
    def descending(self):
        """
        Is current node ordering descending
        :return:
        """
        return DESCENDING == self.ordering

    def is_root(self):
        return self.parent is None

    @staticmethod
    def new(value: int, parent: Optional['Node'] = None, parent_side: Optional[int] = None) -> 'Node':
        """
        New Node instance from given parameters
        :param value:
        :param parent:
        :param parent_side:
        :return:
        """
        if (parent is None and parent_side is not None) or (parent is not None and parent_side is None):
            raise ValueError('Parent comes with its side parameter')
        return Node(value=value, parent=parent, parent_side=parent_side)

    def insert(self, value: int) -> None:
        """
        Adds/Inserts new Node to binary search tree.
        It simply calls `self.add(value)`
        :param value:
        :return:
        """
        self.add(value)

    def add(self, value: int) -> None:
        """
        Adds/Inserts new node to binary search tree
        :param value:
        :return:
        """
        if self.value == value:
            print('Node "{}" is already present in tree! Skipping...'.format(value))
            return
        if (self.ascending and value < self.value) or (self.descending and value > self.value):
            if self.left is not None:
                self.left.add(value)
                return
            else:
                # new node
                self.left = Node.new(value, parent=self, parent_side=LEFT)
        else:
            # if value is equal - will also be added on right branch
            if self.right is not None:
                self.right.add(value)
                return
            else:
                # new node
                self.right = Node.new(value, parent=self, parent_side=RIGHT)

        self.increment_count()

    def increment_count(self) -> None:
        self.elements_count += 1
        if self.parent is not None:
            self.parent.increment_count()

    def decrement_count(self) -> None:
        self.elements_count -= 1
        if self.parent is not None:
            self.parent.decrement_count()

    @property
    def lower(self) -> 'Node':
        return self.left if self.ascending else self.right

    @property
    def higher(self) -> 'Node':
        return self.right if self.ascending else self.left

    @execution_time
    def look_recursive(self, value: int, look_inside_parent=True) -> Optional['Node']:
        if value == self.value:
            return self
        else:
            node = None
            if self.lower is not None and value < self.value:
                node = self.lower.look_recursive(value, time=False)
            elif self.higher is not None and value > self.value:
                node = self.higher.look_recursive(value, time=False)
            if look_inside_parent and node is None and self.parent is not None:
                # it will look in one branch only
                # TODO recursion issue found
                node = self.parent.look_recursive(value, time=False)

        return node

    @execution_time
    def look_in_loop(self, value: int) -> Optional['Node']:
        temp_node = self
        while temp_node is not None:
            if temp_node.value == value:
                return temp_node
            if temp_node.lower is not None and value < temp_node.value:
                temp_node = temp_node.lower
            elif temp_node.higher is not None and value > temp_node.value:
                temp_node = temp_node.higher
            else:
                temp_node = None

        return temp_node

    @property
    def minimum(self):
        if self.lower is None:
            return self
        return self.lower.minimum

    @property
    def maximum(self):
        if self.higher is None:
            return self
        return self.higher.maximum

    def has_branches(self) -> bool:
        """
        Checks if the node has any branches.
        :return:
        """
        return self.left is not None or self.right is not None

    def has_exactly_one_branch(self) -> bool:
        """
        Checks if the node has exactly one branch
        :return:
        """
        return (self.left or self.right) and not (self.left and self.right)

    def get_the_branch(self):
        """
        This method must be used if the node has exactly one branch!
        Returns the left or right branch of the node.
        :return:
        """
        assert self.has_exactly_one_branch()
        if self.left:
            return self.left
        return self.right

    def branches_list(self):
        result = []
        if self.left:
            result.append(self.left)
        if self.right:
            result.append(self.right)
        return result

    def delete(self, node_or_value: Union[int, 'Node']) -> None:
        """
        deletes node or value from the tree
        :param node_or_value:
        :return:
        """
        # find the node if value given
        if isinstance(node_or_value, int):
            node = self.look_recursive(node_or_value)
        else:
            node = node_or_value

        if node is None:
            # node was not found
            return

        replacement = None

        if node.parent is None:
            # This is the root node
            raise NotImplementedError('Root node removal not yet implemented.')

        if not node.has_branches():
            if node.parent_side is LEFT:
                node.parent.left = None
            else:
                node.parent.right = None

        elif node.has_exactly_one_branch():
            replacement = node.get_the_branch()

        else:
            # if we walked so far, it means the node has both(left & right) branches

            # Let's check which branch has more elements and choose from that branch
            if node.left.elements_count > node.right.elements_count:
                # take the maximum from the branch as replacement
                replacement = node.left.maximum
            else:
                # take the minimum from the branch as replacement
                replacement = node.right.minimum

        if replacement:
            node.replace_with(replacement)

        self.decrement_count()

        del node

    def replace_with(self, node: 'Node') -> None:
        """
        Replaces current Node with provided `node` on the parent Node.
        :param node: the node to attach
        :return:
        """
        assert self.parent is not None, "`attach_to_parent` cannot be done on root node"
        # assert self.has_exactly_one_branch(), "`attach_to_parent` cannot be done if node has more than one branch"

        # detach replacement from its parent

        # here we're sure that our replacement has at most one child
        # as we selected maximum or minimum from the tree
        replacement_child_node = node.left or node.right

        if node.parent_side is LEFT:
            # node.parent.left = None
            node.parent.left = replacement_child_node
        else:
            # node.parent.right = None
            node.parent.right = replacement_child_node
        if replacement_child_node:
            replacement_child_node.parent = node.parent
            replacement_child_node.parent_side = node.parent_side

        node.parent = None

        # attach replacement to new parent
        if self.parent_side is LEFT:
            self.parent.left = node
        else:
            self.parent.right = node

        # attach child nodes from ancestor
        if self.right:
            node.right = self.right
            node.right.parent = node
        if self.left:
            node.left = self.left
            node.left.parent = node

        # finally attach parent node to replacement
        node.parent = self.parent
        node.parent_side = self.parent_side

    @execution_time
    def validate_tree(self, minimum=None, maximum=None) -> bool:
        if (
                minimum is not None and self.value < minimum
        ) or (
                maximum is not None and self.value > maximum
        ):
            return False
        return (
            self.left is None or self.left.validate_tree(minimum, self.value, time=False)
        ) and (
            self.right is None or self.right.validate_tree(self.value, maximum, time=False)
        )

    def mirror_recursively(self) -> None:
        """
        Mirrors current node and branches recursively.
        :return:
        """
        self.ordering = self.ordering == ASCENDING and DESCENDING or ASCENDING
        self.left, self.right = self.right, self.left
        self.left and self.left.mirror_recursively()
        self.right and self.right.mirror_recursively()

    def mirror_in_loop(self) -> None:
        current_level_nodes = [self]

        def _task(_nodes) -> List['Node']:
            upcoming_level_nodes = []
            for _node in _nodes:
                _node.left, _node.right = _node.right, _node.left
                upcoming_level_nodes += _node.branches_list()
            return upcoming_level_nodes

        while current_level_nodes:
            current_level_nodes = _task(current_level_nodes)

    def _next_or_prev_value(self, prev_or_next: bool, node: Optional['Node'] = None) -> Optional[int]:
        """
        :param prev_or_next: if True, return the next value, otherwise the previous value
        :param node:
        :return:
        """
        if node is None:
            node = self

        if prev_or_next:
            if self.right:
                return node.right.minimum
        else:
            if self.left:
                return node.left.maximum

        if node.parent and node.parent_side is not prev_or_next:
            return node.parent

        parent = node
        while parent.parent and not parent.parent.is_root() and parent.parent_side is prev_or_next:
            parent = parent.parent

        if parent.parent and (not parent.parent.is_root() or parent.parent_side is not prev_or_next):
            return parent.parent

        return None

    def next(self, node: Optional['Node'] = None) -> Optional['Node']:
        return self._next_or_prev_value(True, node)

    def prev(self, node: Optional['Node'] = None) -> Optional['Node']:
        return self._next_or_prev_value(False, node)


if __name__ == '__main__':

    def draw(_node) -> True:
        networkx_graph(node)
        return True

    test_elements_optimized_order = [72, 44, 60, 62, 83, 63, 56, 46, 80, 25, 15, 54, 92, 84, 96, 28, 58, 8, 7]
    node = Node(test_elements_optimized_order[0])
    for i in test_elements_optimized_order:
        node.add(i)

    draw(node)

    initial_count = len(test_elements_optimized_order) - 1

    assert node.elements_count == initial_count, "Root elements count should be {}, got {}".format(
        initial_count, node.elements_count
    )

    list_copy = test_elements_optimized_order.copy()

    list_copy.sort()
    tmp_node = node.look_recursive(list_copy[0])
    for i in list_copy[1:]:
        assert tmp_node.next().value == i, f"Expected next node for '{tmp_node.value}' to be {i}, got {tmp_node.next().value}"
        tmp_node = tmp_node.next()

    list_copy.sort(reverse=True)

    for i in list_copy[1:]:
        assert tmp_node.prev().value == i, f"Expected prev node for '{tmp_node.value}' to be '{i}', got '{tmp_node.prev().value}'"
        tmp_node = tmp_node.prev()

    del tmp_node
    del list_copy

    # validate removal of node that has both(left & right) branches
    node.delete(83)

    assert node.validate_tree(), draw(node) and "The tree is not valid"
    assert node.right.value == 84, draw(node) and f"Expected '84' on root right node, got '{node.right.value}'"
    assert node.elements_count == (initial_count - 1), draw(node) and f"Expected '{initial_count - 1}' on root right node, got '{node.elements_count}'"
    assert node.right.parent is node, draw(node) and f"Expected parent node to be the root, got '{node.right.parent.value}'"
    assert node.right.left.parent is node.right, draw(node) and f"Expected parent node to be the root, got '{node.right.left.parent.value}'"
    assert node.right.right.parent is node.right, draw(node) and f"Expected parent node to be the root, got '{node.right.right.parent.value}'"
    assert node.left.parent is node, draw(node) and f"Expected parent node to be the root, got '{node.left.parent.value}'"

    # validate mirroring recursively
    assert node.left.value == 44, draw(node) and f"Expected 44 on left node, got '{node.left.value}'"
    node.mirror_recursively()
    assert node.right.value == 44, draw(node) and f"Expected 44 on right node, got '{node.right.value}'"
    assert node.left.value == 84, draw(node) and f"Expected 84 on left node, got '{node.left.value}'"

    # validate mirroring in loop
    node.mirror_in_loop()
    assert node.right.value == 84, draw(node) and f"Expected 44 on right node, got '{node.right.value}'"
    assert node.left.value == 44, draw(node) and f"Expected 84 on left node, got '{node.left.value}'"

    # validate removal of a node that has no branches
    node.delete(80)
    assert node.validate_tree(), draw(node) and "The tree is not valid"
    assert node.right.value == 84, draw(node) and f"Expected 84 on right node, got '{node.right.value}'"
    assert node.right.left is None, draw(node) and draw(node) and f"Expected None on right left node, got '{node.right.left.value}'"

    # validate removal of a node that has right branch only
    node.delete(92)
    assert node.validate_tree(), draw(node) and "The tree is not valid"
    assert node.right.right.value == 96, draw(node) and f"Expected 96 on right node, got '{node.right.right.value}'"

    # validate removal of a node that has left branch only
    node.delete(15)
    assert node.validate_tree(), draw(node) and "The tree is not valid"
    assert node.left.left.left.value == 8, draw(node) and f"Expected 8 on left node, got '{node.left.left.left.value}'"

    # additional
    node.delete(46)
    assert node.validate_tree(), draw(node) and "The tree is not valid"
    assert node.look_recursive(56).left.value == 54, draw(node) and f"Expected 54 on left side of node '56', got '{node.look_recursive(56).left.value}'"

    node.add(46)
    assert node.validate_tree(), draw(node) and "The tree is not valid"
    assert node.look_recursive(54).left.value == 46, draw(node) and f"Expected '46' to be added on left of '54', got '{node.look_recursive(56).left.value}'"


    assert node.look_recursive(96).next() is None, draw(node) and f"Expected None on after 96, got '{node.look_recursive(96).next()}'"
    assert node.look_recursive(63).next() is node, draw(node) and f"Expected '{node.value}', got '{node.look_recursive(63).next().value}'"
    assert node.look_recursive(58).next().value == 60, draw(node) and f"Expected '{node.value}', got '{node.look_recursive(58).next().value}'"

    node.add(57)
    assert node.validate_tree(), draw(node) and "The tree is not valid"
    assert node.look_recursive(58).left.value == 57, draw(node) and f"Expected 57, got '{node.look_recursive(58).left.value}'"

    node.delete(60)
    assert node.validate_tree(), draw(node) and "The tree is not valid"
    assert node.look_recursive(56).right.value == 57, draw(node) and f"Expected 57, got '{node.look_recursive(56).right.value}'"

    draw(node)
    print("Everything is OK")
