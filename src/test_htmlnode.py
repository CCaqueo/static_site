import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode('a href="www.boot.dev"', "Boot.dev")
        node2 = HTMLNode('a href="www.boot.dev"', "Boot.dev")
        
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("p", "This is a not paragraph")

        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("a", "This is a not paragraph")

        self.assertNotEqual(node, node2)

    def test_url(self):
        node = HTMLNode('a href="www.boot.dev"', "Boot.dev")
        html = node.props_to_html()

        node2 = HTMLNode('a href="www.boot.dev"', "Boot.dev")
        html2 = node2.props_to_html()

        self.assertEqual(html, html2)



if __name__ == "__main__":
    unittest.main()