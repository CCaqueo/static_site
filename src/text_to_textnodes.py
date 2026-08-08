from textnode import *
from split_images_links import *
from split_nodes_delimiter import *

def text_to_textnodes(text: str) -> list[TextNode]:
    '''

    A function that converts a raw string of markdown-flavored text into a list of TextNode objects.
    Parameters:
    text (str): a markdown text. For example: This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev).

    '''    

    # The order in which you call the split functions matter: IMAGE -> Link & Bold -> Italic
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes