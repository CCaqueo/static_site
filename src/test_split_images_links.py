import unittest
from split_images_links import *

class TestSplitImagesLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [title](https://i.imgur.com/zjjcJKZ.png) and another [title](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("title", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("title", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_no_images_returns_original_node(self):
        node = TextNode("This is plain text with no markdown images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_image_at_start_no_leading_text_node(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is at the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end_no_trailing_text_node(self):
        node = TextNode(
            "The image is at the end ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("The image is at the end ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_only_image_no_text_nodes_at_all(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes,
        )

    def test_two_adjacent_images_no_text_between(self):
        node = TextNode(
            "![first](https://a.com/1.png)![second](https://a.com/2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://a.com/1.png"),
                TextNode("second", TextType.IMAGE, "https://a.com/2.png"),
            ],
            new_nodes,
        )

    def test_non_text_node_is_passed_through_unchanged(self):
        # Un nodo que ya es BOLD, LINK, etc. no debe tocarse aunque
        # su .text contenga sintaxis de imagen
        node = TextNode("![fake image](https://a.com/x.png)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_multiple_old_nodes_mixed_types(self):
        nodes = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("and ![img](https://a.com/x.png) after", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("already bold", TextType.BOLD),
                TextNode("and ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://a.com/x.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_empty_list_returns_empty_list(self):
        self.assertListEqual([], split_nodes_image([]))

    def test_empty_alt_text_is_allowed(self):
        node = TextNode("Look: ![](https://a.com/x.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Look: ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://a.com/x.png"),
            ],
            new_nodes,
        )

    def test_links_function_does_not_capture_images(self):
        # Sin el (?<!\!) en extract_markdown_links, esto fallaría:
        # el regex de link también matchea la parte "[alt](url)"
        # de un "![alt](url)".
        node = TextNode(
            "An image ![pic](https://a.com/pic.png) and a [real link](https://a.com/page)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "An image ![pic](https://a.com/pic.png) and a ",
                    TextType.TEXT,
                ),
                TextNode("real link", TextType.LINK, "https://a.com/page"),
            ],
            new_nodes,
        )

    def test_image_function_ignores_plain_links(self):
        node = TextNode(
            "A [plain link](https://a.com/page) with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)


if __name__ == "__main__":
    unittest.main()

