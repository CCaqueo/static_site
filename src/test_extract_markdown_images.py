import unittest
from extract_markdown_images_links import *

class TestExtractMarkdownImagesLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [title](https://www.example.com)"
        )
        self.assertEqual(matches, [('title', 'https://www.example.com')])

    def test_many_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            )
        self.assertEqual(matches, [('to boot dev', 'https://www.boot.dev'),('to youtube', 'https://www.youtube.com/@bootdotdev')])

if __name__ == "__main__":
    unittest.main()