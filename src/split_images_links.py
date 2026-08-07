from textnode import *
from extract_markdown_images_links import *

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        # Solo dividimos nodos de texto plano; los demás se dejan igual
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)

        # Si no hay imágenes, el nodo se mantiene tal cual
        if not images:
            new_nodes.append(old_node)
            continue

        remaining_text = original_text
        for alt_text, url in images:
            # Dividimos en base al markdown completo de la imagen
            image_markdown = f"![{alt_text}]({url})"
            before, remaining_text = remaining_text.split(image_markdown, 1)

            # Solo agregamos el texto previo si no está vacío
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

        # Agregamos lo que quede de texto después de la última imagen
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        # Solo dividimos nodos de texto plano; los demás se dejan igual
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_links(original_text)

        # Si no hay imágenes, el nodo se mantiene tal cual
        if not images:
            new_nodes.append(old_node)
            continue

        remaining_text = original_text
        for title, url in images:
            # Dividimos en base al markdown completo de la imagen
            link_markdown = f"[{title}]({url})"
            before, remaining_text = remaining_text.split(link_markdown, 1)

            # Solo agregamos el texto previo si no está vacío
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(title, TextType.LINK, url))

        # Agregamos lo que quede de texto después de la última imagen
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes