import unittest
from split_nodes_delimiter import *


class TestSplitNodeDelimiter(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_two_code_blocks(self):
        node = TextNode("This is text with two `code block1` and `code block2` words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with two ", TextType.TEXT), TextNode("code block1", TextType.CODE), TextNode(" and ", TextType.TEXT), TextNode("code block2", TextType.CODE), TextNode(" words", TextType.TEXT)])

    def test_eq_input_list(self):
        original_node = TextNode("This is text with a `code block` word, a **bold** word and an _italic_ word.", TextType.TEXT)
        nodes = split_nodes_delimiter([original_node], "`", TextType.CODE)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word, a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT)
        ]

        self.assertEqual(nodes, result)


if __name__ == "__main__":
    unittest.main()