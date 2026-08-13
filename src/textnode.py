from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    plain_text = 'plain'
    bold = '**'
    italic = '_'
    code = '`'
    link = '[]'
    image = '![]'
    li = '-'


class TextNode:
    def __init__(self, text: str, type: TextType, url: str | None = None):
        self.text: str = text
        self.text_type: TextType = type
        self.url: str | None = url

    def __eq__(self, other) -> bool:
        if isinstance(other, TextNode):
            return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        else: return False

    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'


def textnode_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.plain_text:
            return LeafNode(None, text_node.text)
        case TextType.bold:
            return LeafNode('b', text_node.text)
        case TextType.italic:
            return LeafNode('i', text_node.text)
        case TextType.code:
            return LeafNode('code', text_node.text)
        case TextType.link:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case TextType.image:
            return LeafNode('img','', {'src': text_node.url, 'alt': text_node.text})
        case TextType.li:
            return LeafNode('li', text_node.text)
        case x:
            raise ValueError('Invalid text_type')

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.plain_text or delimiter not in node.text:
            new_nodes.append(node)
            continue
        if (node.text.count(delimiter) % 2) != 0:
            raise Exception(f'Invalid Markdown Syntax: No closing {delimiter} delimiter in:\n{node.text}')
        
        splitted_string = node.text.split(delimiter)
        for i in range(len(splitted_string)):
            if splitted_string[i] == '': continue
            if i % 2 == 0:
                new_nodes.append(TextNode(splitted_string[i], TextType.plain_text))
            else:
                new_nodes.append(TextNode(splitted_string[i], text_type))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)" ,text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)" ,text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.plain_text:
            new_nodes.append(node)
        else:
            splitted_nodes: list[TextNode]  = []
            images: list[tuple[str, str]] = extract_markdown_images(node.text)
            text: str = node.text
            for image in images:
                split = text.split(f"![{image[0]}]({image[1]})", maxsplit=1)
                if split[0] != '':
                    splitted_nodes.append(TextNode(split[0], TextType.plain_text))
                splitted_nodes.append(TextNode(image[0], TextType.image, image[1]))
                text = split[1]
            if text != '':
                splitted_nodes.append(TextNode(text, TextType.plain_text))
            new_nodes.extend(splitted_nodes)
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.plain_text:
            new_nodes.append(node)
        else:
            splitted_nodes: list[TextNode]  = []
            links: list[tuple[str, str]] = extract_markdown_links(node.text)
            text: str = node.text
            for link in links:
                split = text.split(f"[{link[0]}]({link[1]})", maxsplit=1)
                if split[0] != '':
                    splitted_nodes.append(TextNode(split[0], TextType.plain_text))
                splitted_nodes.append(TextNode(link[0], TextType.link, link[1]))
                text = split[1]
            if text != '':
                splitted_nodes.append(TextNode(text, TextType.plain_text))
            new_nodes.extend(splitted_nodes)
    return new_nodes

def split_list_elements(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.plain_text:
                    new_nodes.append(node)
        else:
            lines = node.text.split('\n')
            for line in lines:
                # print(f"DEBUG: processing: {line}, checking: {line[:1]}, comparition: {line[:2] == '- '}")
                if line[:2] == '- ' or line[0] == '.':
                    new_nodes.append(TextNode(line[2:], TextType.li))
                else:
                    new_nodes.append(TextNode(line, TextType.plain_text))
    return new_nodes
  
def text_to_textnodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.plain_text)]
    for type in TextType:
        if type == TextType.link:
            nodes = split_nodes_link(nodes)
        elif type == TextType.image:
            nodes = split_nodes_image(nodes)
        elif type == TextType.li:
            nodes = split_list_elements(nodes)
        else:
            nodes = split_nodes_delimiter(nodes, type.value, type)
    return nodes