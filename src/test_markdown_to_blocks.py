import unittest
from markdown_to_blocks import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_basic_multiple_blocks(self):
        markdown = (
            "# Heading\n\n"
            "This is a paragraph of text.\n\n"
            "* item 1\n* item 2"
        )
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# Heading",
                "This is a paragraph of text.",
                "* item 1\n* item 2",
            ],
            blocks,
        )

    def test_single_block_no_double_newline(self):
        markdown = "Just one paragraph, nothing more."
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(["Just one paragraph, nothing more."], blocks)

    def test_empty_string_returns_empty_list(self):
        blocks = markdown_to_blocks("")
        self.assertListEqual([], blocks)

    def test_multiple_consecutive_blank_lines_between_blocks(self):
        # Tres o más saltos de línea seguidos generan bloques vacíos
        # que deben ser filtrados
        markdown = "First block\n\n\n\nSecond block"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(["First block", "Second block"], blocks)

    def test_leading_and_trailing_whitespace_in_document(self):
        markdown = "\n\n  First block  \n\nSecond block\n\n"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(["First block", "Second block"], blocks)

    def test_leading_and_trailing_whitespace_within_block(self):
        markdown = "   Indented paragraph with spaces   \n\nAnother one"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            ["Indented paragraph with spaces", "Another one"], blocks
        )

    def test_block_preserves_internal_single_newlines(self):
        # Un bloque de lista con \n simples entre ítems debe
        # mantenerse como un solo bloque, sin dividirse
        markdown = "* item 1\n* item 2\n* item 3"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(["* item 1\n* item 2\n* item 3"], blocks)

    def test_whitespace_only_document_returns_empty_list(self):
        # Un documento que es solo espacios/saltos de línea no debe
        # producir bloques "vacíos" tras el strip()
        markdown = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual([], blocks)

    def test_block_that_is_only_whitespace_between_real_blocks(self):
        # Bloque compuesto solo por espacios (sin ser "") entre dos
        # bloques reales: filter(None, ...) NO lo elimina porque
        # "   " es truthy; recién al hacer .strip() queda como ""
        markdown = "First block\n\n   \n\nSecond block"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(["First block", "Second block"], blocks)

    def test_heading_block(self):
        markdown = "## This is a heading"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(["## This is a heading"], blocks)

    def test_code_block_with_backticks(self):
        markdown = "```\ndef foo():\n    pass\n```\n\nSome text after"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            ["```\ndef foo():\n    pass\n```", "Some text after"], blocks
        )

    def test_many_blocks_in_sequence(self):
        markdown = (
            "# Title\n\n"
            "Intro paragraph.\n\n"
            "## Subheading\n\n"
            "* list item 1\n* list item 2\n\n"
            "Closing paragraph."
        )
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# Title",
                "Intro paragraph.",
                "## Subheading",
                "* list item 1\n* list item 2",
                "Closing paragraph.",
            ],
            blocks,
        )


if __name__ == "__main__":
    unittest.main()