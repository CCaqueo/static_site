import unittest
from leafnode import *

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "boot.dev", {"href": "www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="www.boot.dev">boot.dev</a>')

    def test_leaf_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.children, None)

if __name__ == "__main__":
    unittest.main()