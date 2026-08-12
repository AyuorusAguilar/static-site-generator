from functools import reduce

class HTMLNode:
    def __init__(self,
                 tag: str | None = None, 
                 value: str  | None = None, 
                 children: list[HTMLNode]  | None = None, 
                 props: dict[str, str | None]  | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props= props

    def to_html(self) -> None | str:
        raise NotImplemented()
    def props_to_html(self):
        output = ''
        if self.props is not None and len(self.props) > 1:
            for prop in self.props.keys():
                output += f' {prop}="{self.props[prop]}"'
        return output
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    def __eq__(self, value: object) -> bool:
        if isinstance(value, HTMLNode):
            return self.tag == value.tag and  self.value == value.value and  self.children == value.children and  self.props == value.props
        else: return False


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str | None]  | None = None) -> None:
        super().__init__(tag, value, props= props)

    def to_html(self) -> str:
        if self.value is None or self.value == '' :
            raise ValueError("Value property can't be empty for LeafNodes xP")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self) -> str:
            return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str | None]  | None = None) -> None:
        super().__init__(tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None or self.tag == '' :
            raise ValueError("tag property can't be empty xP for ParentNodes")
        if self.children is None or self.children == [] :
            raise ValueError("children property can't be empty xP for ParentNodes")
        
        content = reduce(lambda x, y: str(x) + str(y.to_html()), self.children, '')

        return f"<{self.tag}{self.props_to_html()}>{content}</{self.tag}>"