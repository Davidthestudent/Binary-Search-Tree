from typing import Any
from collections import deque


class TreeNode:

    def __init__(self, key: int, value: Any, right: 'TreeNode' = None,
                 left: 'TreeNode' = None, parent: 'TreeNode' = None):
        """Initialize TreeNode.

        Args:
            key (int): Key used for sorting the node into a BST.
            value (Any): Whatever data the node shall carry.
            right (TreeNode, optional): Node to the right, with a larger key. Defaults to None.
            left (TreeNode, optional): Node to the left, with a lesser key. Defaults to None.
            parent (TreeNode, optional): Parent node. Defaults to None.
        """
        self.key = key
        self.value = value
        self.right = right
        self.left = left
        self.parent = parent

    def __repr__(self) -> str:
        return f"TreeNode({self.key}, {self.value})"

    @property
    def depth(self) -> int:
        if self.key is None or self.parent is None:
            return 0
        return self.depth_helper(self.key)

    def depth_helper(self, key: int) -> int:
        node = self.find_node(key)  # Find the node corresponding to the key
        if node is None:
            return 0
        return self._depth(node)

    def _depth(self, node: 'TreeNode') -> int:
        if node is None:
            return 0
        left_depth = self._depth(node.left)
        right_depth = self._depth(node.right)
        return 1 + max(left_depth, right_depth)
        # TODO

    def find_node(self, key: int) -> 'TreeNode':
        """Find and return the node with the given key."""
        # Base case: If the current node is None or its key matches the given key, return the current node
        if self.key is None or self.key == key:
            return self
        # If the given key is less than the current node's key, search in the left subtree
        elif key < self.key and self.left:
            return self.left.find_node(key)
        # If the given key is greater than the current node's key, search in the right subtree
        elif key > self.key and self.right:
            return self.right.find_node(key)
        else:
            return None

    @property
    def is_external(self) -> bool:
        if self.left is None and self.right is None:
            return True
        else:
            return False
        # TODO

    @property
    def is_internal(self) -> bool:
        if self.left is not None or self.right is not None:
            return True
        else:
            return False

    # You can of course add your own methods and/or functions!
    # (A method is within a class, a function outside of it.)
