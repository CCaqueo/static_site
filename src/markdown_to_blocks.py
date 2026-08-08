def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")

    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()

    blocks = list(filter(None, blocks))

    return blocks