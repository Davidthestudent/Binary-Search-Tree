from typing import Any, Generator, Tuple, Optional

from tree_node import TreeNode


class BinarySearchTree:
    """Binary-Search-Tree implemented for didactic reasons."""

    def __init__(self, root: TreeNode = None):
        """Initialize BinarySearchTree.

        Args:
            root (TreeNode, optional): Root of the BST. Defaults to None.
        
        Raises:
            ValueError: root is neither a TreeNode nor None.
        """
        self._root = root
        self._size = 0 if root is None else 1
        self._num_of_comparisons = 0

    def insert(self, key: int, value: Any) -> None:
        """Insert a new node into the BST."""
        if not isinstance(key, int):
            raise ValueError('Key must be an integer.')
        if value is None:
            raise KeyError('Value cannot be None.')

        # If the tree is empty, create a new node and make it the root
        if self._size == 0:
            self._root = TreeNode(key, value)
            self._size += 1
            return

        # Call the recursive helper function to insert the node
        self._insert_helper(self._root, key, value)

    def _insert_helper(self, node: TreeNode, key: int, value: Any) -> None:
        """Helper function to recursively insert a new node into the BST."""
        if node is None:
            # If we've reached an empty spot, create a new node
            return TreeNode(key, value)

        # If the key already exists, raise a KeyError
        if key == node.key:
            raise KeyError("Key already exists in the tree")

        # Recursively insert into the left subtree
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key, value)
                self._size += 1
            else:
                self._insert_helper(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = TreeNode(key, value)
                self._size += 1
            else:
                self._insert_helper(node.right, key, value)

    def find(self, key: int) -> TreeNode:
        """Find a node with the given key in the BST."""
        if not isinstance(key, int):
            raise ValueError('Key must be an integer.')
        if key is None:
            raise KeyError('Key cannot be None.')

        # Call the helper function to perform the search
        node, parent_key = self._find_helper(self._root, key)

        # If the node is not found, raise KeyError
        if node is None:
            raise KeyError('Key does not exist.')

        # Update the parent's key
        parent_key = parent_key if parent_key is not None else None

        return node

    def _find_helper(self, node: TreeNode, key: int) -> Tuple[Optional[TreeNode], Optional[int]]:
        """Helper function to find a node with the given key and its parent's key."""
        if node is None:
            return None, None

        if key == node.key:
            return node, node.parent.key if node.parent else None  # Key found at current node

        elif key < node.key:
            return self._find_helper(node.left, key)  # Search left subtree

        else:
            return self._find_helper(node.right, key)  # Search right subtree

    @property
    def size(self) -> int:
        return self._size
        # TODO

    # If users instead call `len(tree)`, this makes it return the same as `tree.size`
    __len__ = size

    # This is what gets called when you call e.g. `tree[5]`
    def __getitem__(self, key: int) -> Any:
        """Return value of node with given key.

        Args:
            key (int): Key to look for.

        Raises:
            ValueError: If key is not an integer.
            KeyError: If key is not present in the tree.

        Returns:
            Any: [description]
        """
        return self.find(key).value

    def remove(self, key: int) -> None:
        if not isinstance(key, int):
            raise ValueError('Key must be an integer.')

        current = self._root
        parent = None

        # Find the node with the given key and its parent
        while current is not None:
            if key == current.key:
                break
            elif key < current.key:
                parent = current
                current = current.left
            else:
                parent = current
                current = current.right

        if current is None:
            raise KeyError('Key does not exist.')

        # Case 1: Node to be deleted has no children
        if current.left is None and current.right is None:
            if parent is not None:
                if parent.left == current:
                    parent.left = None
                else:
                    parent.right = None
            else:
                self._root = None

        # Case 2: Node to be deleted has one child
        elif current.left is None:
            if parent is not None:
                if parent.left == current:
                    parent.left = current.right
                else:
                    parent.right = current.right
            else:
                self._root = current.right

        elif current.right is None:
            if parent is not None:
                if parent.left == current:
                    parent.left = current.left
                else:
                    parent.right = current.left
            else:
                self._root = current.left

        # Case 3: Node to be deleted has two children
        else:
            # Find the successor node (smallest node in the right subtree)
            successor_parent = current
            successor = current.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left

            # Copy the successor's key and value to the current node
            current.key = successor.key
            current.value = successor.value

            # Remove the successor node
            if successor_parent == current:
                successor_parent.right = successor.right
            else:
                successor_parent.left = successor.right

        self._size -= 1  # Decrement the size

    # Hint: The following 3 methods can be implemented recursively, and 
    # the keyword `yield from` might be extremely useful here:
    # http://simeonvisser.com/posts/python-3-using-yield-from-in-generators-part-1.html

    # Also, we use a small syntactic sugar here: 
    # https://www.pythoninformer.com/python-language/intermediate-python/short-circuit-evaluation/

    def inorder(self, node: TreeNode = None) -> Generator[TreeNode, None, None]:
        """Yield nodes in inorder."""
        node = node or self._root
        # This is needed in the case that there are no nodes.
        if not node:
            return iter(())
        yield from self._inorder(node)

    def preorder(self, node: TreeNode = None) -> Generator[TreeNode, None, None]:
        """Yield nodes in preorder."""
        node = node or self._root
        if not node:
            return iter(())
        yield from self._preorder(node)

    def postorder(self, node: TreeNode = None) -> Generator[TreeNode, None, None]:
        """Yield nodes in postorder."""
        node = node or self._root
        if not node:
            return iter(())
        yield from self._postorder(node)

    # this allows for e.g. `for node in tree`, or `list(tree)`.
    def __iter__(self) -> Generator[TreeNode, None, None]:
        yield from self._preorder(self._root)

    @property
    def is_valid(self) -> bool:
        return self._is_valid_helper(self._root, float('-inf'), float('inf'))

    def _is_valid_helper(self,node: 'TreeNode' ,min_val: float, max_val: float) -> bool:
        # Base case: if the node is None, it's a valid BST subtree
        if node is None:
            return True

        # Check if the node's key violates the BST property
        if not (min_val < node.key < max_val):
            return False
        left_valid = self._is_valid_helper(node.left, min_val, node.key)
        right_valid = self._is_valid_helper(node.right, node.key, max_val)
        return left_valid and right_valid


    def return_max_key(self) -> TreeNode:
        if self._root is None:
            return None
        else:
            current = self._root
            while current.right is not None:
                current = current.right
        return current

    def return_min_key(self) -> TreeNode:
        if self._root is None:
            return None
        else:
            current = self._root
            while current.left is not None:
                current = current.left
        return current

    def find_comparison(self, key: int) -> Tuple[int, int]:
        """Create an inbuilt python list of BST values in preorder and compute the number of comparisons needed for
           finding the key both in the list and in the BST.
           Return the numbers of comparisons for both, the list and the BST
        """
        bst_comparisons = 0
        bst_found = False
        current = self._root
        while current:
            bst_comparisons += 1
            if current.key == key:
                bst_found = True
                break
            elif key < current.key:
                bst_comparisons += 1
                current = current.left
            else:
                bst_comparisons += 1
                current = current.right
        python_list = list(node.key for node in self._preorder(current))
        list_comparisons = 0
        if key in python_list:
            list_comparisons = python_list.index(key) + 1
        else:
            list_comparisons = len(python_list)

        return list_comparisons, bst_comparisons

    def __repr__(self) -> str:
        return f"BinarySearchTree({list(self._inorder(self._root))})"

    ####################################################
    # Helper Functions
    ####################################################

    def get_root(self):
        return self._root

    def _inorder(self, current_node):
        if current_node is None:
            return None
        yield from self._inorder(current_node.left)
        yield current_node  # Yield the current node
        yield from self._inorder(current_node.right)

    def _preorder(self, current_node):
        if current_node is None:
            return None
        yield current_node
        yield from self._preorder(current_node.left)
        yield from self._preorder(current_node.right)

    def _postorder(self, current_node):
        if current_node is None:
            return
        yield from self._postorder(current_node.left)  # Corrected from _inorder to _postorder
        yield from self._postorder(current_node.right)  # Corrected from _inorder to _postorder
        yield current_node
    # You can of course add your own methods and/or functions!
    # (A method is within a class, a function outside of it.)
