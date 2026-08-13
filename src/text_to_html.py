import re

from markdown_to_blocks import markdown_to_blocks, block_type_detector, BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, textnode_to_html_node, text_to_textnodes

def markdown_to_html_node(markdown, debug = False) -> str:
	blocks = markdown_to_blocks(markdown)
	nodes: list[HTMLNode] = []
	for block in blocks:
		tag : BlockType | str = block_type_detector(block).value
		if tag == 'h':
			markdown = re.findall(r"(?<!#)(#{1,6}\s)", block[:7])[0].count('#')
			block = block[markdown + 1:]
			tag = 'h' + str(markdown)
		if tag == 'blockquote':
					lines = block.split('\n')
					new_content = ''
					for line in lines:
						new_content += line[1:]
					block = new_content
		content: list[TextNode] = text_to_textnodes(block)
		children = [textnode_to_html_node(node) for node in content]
		nodes.append(ParentNode(tag, children, None))

	root_node = ParentNode('div', nodes)
	return root_node.to_html()

def extract_title(markdown):
	return re.findall(r"(?<!#)(#{1}\s)(?!#)(.*)(\n|$)", markdown)[0][1]

def generate_page(from_path, template_path, dest_path):
	# print(f"Generating pafe from {from_path} to {dest_path} using {template_path}")
	with open(from_path, 'r') as file:
		markdown_source = file.read()
	with open(template_path, 'r') as file:
		template_source = file.read()
	html_string = markdown_to_html_node(markdown_source)
	title = extract_title(markdown_source)
	template_source = template_source.replace('{{ Title }}', title)
	template_source = template_source.replace('{{ Content }}', html_string)
	with open(f"{dest_path[:-2]}html", 'w') as file:
		file.write(template_source)
	