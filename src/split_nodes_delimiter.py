from textnode import TextNode, TextType, text_node_to_html_node

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:

    allowed_delimiters: list[str] = ["**", "`", "_"]
    new_nodes: list[TextNode] = []

    if delimiter not in allowed_delimiters:
        raise ValueError("Invalid Markdown syntax: delimiter")

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:

            temp = old_node.text.split(delimiter)

            for idx in range(len(temp)):
                if (idx % 2 == 0) and (temp[idx] != ""):
                    new_nodes.append(TextNode(temp[idx], TextType.TEXT))
                elif idx % 2 != 0:
                    new_nodes.append(TextNode(temp[idx], text_type))

    return new_nodes