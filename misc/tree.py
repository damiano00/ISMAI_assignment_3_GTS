class Tree:

    class Node:
        def __init__(self, label=None):
            self.label = label
            self.children = []
            return

    def __init__(self):
        self._root = None
        self._size = 0
        return

    def root(self):
        return self._root

    def size(self):
        return self._size

    def add_root(self, node_label=None):
        self._root = self.Node(node_label)
        return self._root

    def add_child(self, nid, node_label=None):
        node = nid
        child_node = self.Node(node_label)
        node.children.append(child_node)
        self._size += 1
        return child_node

    @staticmethod
    def is_leaf(nid):
        node = nid
        return not node.children

    @staticmethod
    def num_children(nid):
        node = nid
        return len(node.children)

    @staticmethod
    def child(nid, i):
        node = nid
        return node.children[i] if node.children and i < len(node.children) else None

    @staticmethod
    def children(nid):
        node = nid
        return node.children

    @staticmethod
    def node_label(nid):
        node = nid
        return node.label


def depth_first_traversal(tree, nid, depth, func, pid = None, num=None):
    func(depth, tree.node_label(nid), pid, num)
    for i in range(tree.num_children(nid)):
        depth_first_traversal(tree, tree.child(nid, i), depth+1, func, tree.node_label(nid), i)
    return
