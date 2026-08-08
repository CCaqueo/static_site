import unittest
from block_to_block_type import *


class TestBlockToBlockType(unittest.TestCase):

    # --- Heading ---

    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_seven_hashes_is_paragraph(self):
        # Más de 6 '#' ya no es un heading válido
        self.assertEqual(
            block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH
        )

    def test_heading_without_space_is_paragraph(self):
        # Falta el espacio después de '#'
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_heading_with_no_text_after_hash(self):
        # '#' seguido de espacio pero sin texto no matchea (requiere .+)
        self.assertEqual(block_to_block_type("# "), BlockType.PARAGRAPH)

    def test_heading_hash_in_middle_of_text_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is # not a heading"), BlockType.PARAGRAPH
        )

    # --- Code ---

    def test_code_block_basic(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_multiline(self):
        block = "```\ndef foo():\n    return 42\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_only_opening_backticks_is_paragraph(self):
        # No cierra con ```
        block = "```\nprint('hello')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_single_line_six_backticks(self):
        # "``````" cumple startswith y endswith con ``` pero no es
        # realmente un code block multilinea válido según el enunciado
        # (debe empezar con ``` + salto de línea). Este test documenta
        # el comportamiento actual de la implementación simple.
        block = "``````"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_inline_backticks_not_a_code_block(self):
        # Un solo par de backticks (code inline) no es un code block
        block = "This has `inline code` in it"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Quote ---

    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

    def test_quote_multiline(self):
        block = "> Line one\n> Line two\n> Line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_without_space_after_gt(self):
        # El espacio después de '>' es opcional
        block = ">No space here"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_one_line_missing_gt_is_paragraph(self):
        # Si UNA sola línea no tiene '>', ya no es un quote válido
        block = "> Line one\nLine two without gt"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_empty_line_breaks_quote(self):
        block = "> Line one\n\n> Line two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Unordered list ---

    def test_unordered_list_single_item(self):
        self.assertEqual(block_to_block_type("- item one"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple_items(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_without_space_is_paragraph(self):
        # "-item" sin espacio no cuenta
        block = "-item one\n-item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_one_line_missing_dash_is_paragraph(self):
        block = "- item one\nitem two without dash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_with_asterisk_is_paragraph(self):
        # El enunciado exige '-' específicamente, no '*'
        block = "* item one\n* item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Ordered list ---

    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. item one"), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple_items(self):
        block = "1. item one\n2. item two\n3. item three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_not_starting_at_one_is_paragraph(self):
        block = "2. item one\n3. item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_skipping_number_is_paragraph(self):
        # 1, 2, 4 -> rompe la secuencia
        block = "1. item one\n2. item two\n4. item three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_out_of_order_is_paragraph(self):
        block = "1. item one\n3. item two\n2. item three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_without_space_is_paragraph(self):
        block = "1.item one\n2.item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_double_digit_numbers(self):
        block = "\n".join(f"{i}. item {i}" for i in range(1, 12))
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    # --- Paragraph (default) ---

    def test_plain_paragraph(self):
        block = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        block = "This is line one\nand this is line two\nof the same paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_string_is_paragraph(self):
        # Caso borde: string vacío no matchea ninguna regla especial
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    # --- Ambigüedad entre tipos ---

    def test_block_starting_like_ordered_but_mixed_with_unordered(self):
        # Mezcla de list markers: no cumple ninguna regla al 100%
        block = "1. item one\n- item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_takes_precedence_check(self):
        # Un bloque que parece heading no debería colarse en otra categoría
        self.assertEqual(block_to_block_type("# > not a quote"), BlockType.HEADING)


if __name__ == "__main__":
    unittest.main()