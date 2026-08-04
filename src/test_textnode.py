import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)

        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = TextNode("THIS IS A TEXT NODE", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("www.boot.dev", TextType.LINK, "https://www.boot.dev/")
        node2 = TextNode("www.boot.dev", TextType.LINK)

        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_leaf_node_to_html(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(),"<b>This is a text node</b>")



if __name__ == "__main__":
    unittest.main()