import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown: str) -> BlockType:

    block_type: BlockType = BlockType.PARAGRAPH

    if markdown:

        match markdown[0]:
            case "#":

                # We find the sequence of "#"
                matches = re.findall(r"\#+ ", markdown)

                # if there is a sequence of "# " AND if the sequence of # is shorter than 7 AND if there is text after the "# " sequence
                if matches and len(matches[0].strip()) < 7 and markdown.split(matches[0], 1)[1]:
                    block_type = BlockType.HEADING

            case "`":

                # If the block starts with ```\n and ends with ``` it is a CODE
                if markdown[:4] == "```\n" and markdown[-3:] == "```":
                    block_type = BlockType.CODE

            case ">":
                # Base Case
                block_type = BlockType.QUOTE

                # We split the block in the different lines.
                block = markdown.split("\n")

                # If the line is empty, or it doesn't start with a ">", then it is not a QUOTE block.
                for line in block:
                    if not line or line[0] != ">":
                        block_type = BlockType.PARAGRAPH
                        
            case "-":
                # Base Case
                block_type = BlockType.UNORDERED_LIST

                block = markdown.split("\n")

                # If every line starts with a "- " then the block type remains. Otherwise it changes.
                for item in block:
                    if not item[:2] == "- ":
                        block_type = BlockType.PARAGRAPH
                        
            case "1":
                # Base Case
                block_type = BlockType.ORDERED_LIST

                block = markdown.split("\n")

                # We create a list to keep track of the indexes of the list.
                digits: list[int] = []

                # If every line starts with a number followed by a dot and a space, the block type remains. If at least one line doesnt meet the requirements, the type changes.
                for i in range(len(block)):

                    # We match to see if the condition for the digit + dot + space is met.
                    matches = re.findall(r"\d+\. ", block[i])
                    # We match to extract the index and then we add it to to digits list.
                    digit = re.findall(r"\d+", block[i])
                    if digit:
                        digits.append(int(digit[0]))
                    if not matches or not block[i].startswith(matches[0]):
                        block_type = BlockType.PARAGRAPH

                # We check if the digit list is sorted.
                is_sorted = all(digits[i] + 1 == digits[i + 1] for i in range(len(digits) - 1))
                if not is_sorted:
                    block_type = BlockType.PARAGRAPH
                
    return block_type

if __name__ == "__main__":
    block = "> Line one\n\n> Line two"
    print(block_to_block_type(block))