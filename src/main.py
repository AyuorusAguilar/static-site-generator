import os
from move_files_idk import recursive_copy
from text_to_html import generate_page

from textnode import TextNode, TextType
def main():

    dir1 = os.path.abspath('static')
    dir2 = os.path.abspath('public')
    template = os.path.abspath('template.html')
    content_dir = os.path.abspath('content')
    content_content = os.listdir(content_dir)

    if not os.path.exists(dir1):
        raise Exception('Static directory does not exist')
    if not os.path.exists(template):
        raise Exception('No template found! Make sure there is a template.html document in the root of the app')
    if not os.path.exists(dir2):
        os.mkdir(dir2)
    if not os.path.exists(dir2):
        os.mkdir(dir2)
    if len(content_content) < 1:
         raise Exception('The content directory is empty! Write some nasty Markdown and mister engine would convert it for ya! :D')

    recursive_copy(dir1, dir2)
    
    for content in content_content:
        source_dir = f"{content_dir}/{content}"
        dest_dir = f"{dir2}/{content}"
        generate_page(source_dir, template, dest_dir)

if __name__ == '__main__':
    main()
    