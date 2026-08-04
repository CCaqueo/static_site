from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):        
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return f"{self.value}"
        if self.props:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
        
        
        