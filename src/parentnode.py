from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag attribute is mandatory")
        if self.children is None:
            raise ValueError("Children attribute is mandatory")
        result = f"<{self.tag}>"
        for child in self.children:
            result += child.to_html()
        return f"{result}</{self.tag}>"
        

