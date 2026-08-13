from enum import Enum
import re


class BlockType(Enum):
    paragraph = 'p'
    heading = 'h'
    code = 'code'
    quote = 'blockquote'
    unordered_list = 'ul'
    ordered_list = 'ol'

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split('\n\n')
    blocks = [block.strip('\n').strip(' ') for block in blocks if block != '']
    return blocks

def block_type_detector(markdown_text: str) -> BlockType:
    blocks = markdown_text.split('\n\n')
    if len(blocks) > 1:
        raise ValueError("Error: The input markdown_text should be one single block")
    if len(re.findall(r"(?<!#)(#{1,6}\s)", markdown_text[:8])) == 1:
        return BlockType.heading
    if markdown_text[:3] == '```' and markdown_text[-3:] == '```':
        return BlockType.code
    char_at_start_of_every_line: str | None = None
    for line in markdown_text.split('\n'):
        if char_at_start_of_every_line is None:
            char_at_start_of_every_line = line[0]
            continue
        if char_at_start_of_every_line != line[0]:
            return BlockType.paragraph
    match char_at_start_of_every_line:
        case '>':
            return BlockType.quote
        case '-':
            return BlockType.unordered_list
        case '.':
            return BlockType.ordered_list
    return BlockType.paragraph
    
