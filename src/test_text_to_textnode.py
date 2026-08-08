import unittest
from text_to_textnodes import *


class TestTextToTextNodes(unittest.TestCase):

    def test_full_example_all_types(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_plain_text_no_markdown(self):
        text = "Just plain text, nothing special here."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("Just plain text, nothing special here.", TextType.TEXT)],
            new_nodes,
        )

    def test_empty_string(self):
        new_nodes = text_to_textnodes("")
        # split("") de un string vacío da [""], que se filtra -> lista vacía
        self.assertListEqual([], new_nodes)

    def test_only_image(self):
        text = "![alt](https://a.com/x.png)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "https://a.com/x.png")],
            new_nodes,
        )

    def test_only_link(self):
        text = "[click here](https://a.com)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("click here", TextType.LINK, "https://a.com")],
            new_nodes,
        )

    def test_image_not_confused_with_link(self):
        # Caso clave: la imagen no debe generar un LINK duplicado
        text = "An image: ![pic](https://a.com/pic.png)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("An image: ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://a.com/pic.png"),
            ],
            new_nodes,
        )

    def test_code_block_not_affected_by_bold_or_italic_chars(self):
        # El contenido dentro de `...` no debe ser reinterpretado
        # como bold/italic aunque tenga _ o ** dentro
        text = "Use `snake_case` and `**not_bold**` in your code"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("snake_case", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("**not_bold**", TextType.CODE),
                TextNode(" in your code", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_bold_and_italic_mixed(self):
        text = "**a** _b_ **c** _d_"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("a", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("b", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("c", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("d", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_multiple_images_and_links_together(self):
        text = "![img1](https://a.com/1.png) then [link1](https://a.com/p1) then ![img2](https://a.com/2.png) then [link2](https://a.com/p2)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "https://a.com/1.png"),
                TextNode(" then ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://a.com/p1"),
                TextNode(" then ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://a.com/2.png"),
                TextNode(" then ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://a.com/p2"),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main() 