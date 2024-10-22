# tree.py
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.number = None  # Add a number attribute (singular/plural)

    def add_child(self, child):
        self.children.append(child)
        
    # RECURSIVELY PRINT THE TREE
    def print_tree(self, depth=0):
        """Prints the tree structure."""
        print("  " * depth + self.value)
        for child in self.children:
            child.print_tree(depth + 1)
