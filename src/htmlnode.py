class HTMLNode():
    """

    Parameters:
    tag (str): A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
    value (str): A string representing the value of the HTML tag (e.g. the text inside a paragraph)
    children (list[HTMLNode]): A list of HTMLNode objects representing the children of this node
    props (dict[str, str]): A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    """
    def __init__(self, tag=None, value=None, children=None, props=None ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        if self.props is None:
            return result
        else:
            for key in self.props:
                result += f' {key}="{self.props[key]}"'
            return result

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    