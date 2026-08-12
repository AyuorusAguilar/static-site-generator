import unittest
from textnode import TextType, TextNode, text_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a textnode", TextType.bold)
        node2 = TextNode("This is a textnode", TextType.bold)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a textnode", TextType.bold)
        node2 = TextNode("This is a diferent textnode", TextType.italic)
        self.assertNotEqual(node, node2)
    def test_instance(self):
        node = TextNode("This is a textnode", TextType.bold)
        self.assertIsInstance(node, TextNode)


class test_text_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode('example', TextType.plain_text)
        HTMLNode = text_to_html_node(node)
        self.assertEqual(HTMLNode.tag, None)
        self.assertEqual(HTMLNode.value, 'example')
    def test_bold(self):
        node = TextNode('example', TextType.bold)
        HTMLNode = text_to_html_node(node)
        self.assertEqual(HTMLNode.tag, 'b')
        self.assertEqual(HTMLNode.value, 'example')
    def test_italics(self):
        node = TextNode('example', TextType.italic)
        HTMLNode = text_to_html_node(node)
        self.assertEqual(HTMLNode.tag, 'i')
        self.assertEqual(HTMLNode.value, 'example')
    def test_code(self):
        node = TextNode('example', TextType.code)
        HTMLNode = text_to_html_node(node)
        self.assertEqual(HTMLNode.tag, 'code')
        self.assertEqual(HTMLNode.value, 'example')
    def test_link(self):
        node = TextNode('example', TextType.link, 'ismu.com')
        HTMLNode = text_to_html_node(node)
        self.assertEqual(HTMLNode.tag, 'a')
        self.assertEqual(HTMLNode.value, 'example')
        self.assertEqual(HTMLNode.props, {'href' : 'ismu.com'})
    def test_image(self):
        node = TextNode('example', TextType.image, 'ismu.com/ismu.png')
        HTMLNode = text_to_html_node(node)
        self.assertEqual(HTMLNode.tag, 'img')
        self.assertEqual(HTMLNode.value, '')
        self.assertEqual(HTMLNode.props, {'alt' : 'example', 'src' : 'ismu.com/ismu.png'})


class test_split_nodes_delimiter(unittest.TestCase):
    def test_bold(self):
        nodelist = [
            TextNode('Ismael Manzanero come **Manzanas**', TextType.plain_text),
            TextNode('Ismael Manzanero come **Manzanas**', TextType.bold),
            TextNode('Ismael Manzanero come **Manzanas**', TextType.plain_text)
            ]
        expected_output = [
            TextNode('Ismael Manzanero come ', TextType.plain_text),
            TextNode('Manzanas', TextType.bold),
            TextNode('Ismael Manzanero come **Manzanas**', TextType.bold),
            TextNode('Ismael Manzanero come ', TextType.plain_text),
            TextNode('Manzanas', TextType.bold),
            ]
        self.assertEqual(split_nodes_delimiter(nodelist, '**', TextType.bold), expected_output)
        
    def test_italic(self):
        nodelist = [
            TextNode('Ismael Manzanero come _Manzanas_', TextType.plain_text),
            TextNode('Ismael Manzanero come _Manzanas_', TextType.italic),
            TextNode('Ismael Manzanero come _Manzanas_', TextType.plain_text)
            ]
        expected_output = [
            TextNode('Ismael Manzanero come ', TextType.plain_text),
            TextNode('Manzanas', TextType.italic),
            TextNode('Ismael Manzanero come _Manzanas_', TextType.italic),
            TextNode('Ismael Manzanero come ', TextType.plain_text),
            TextNode('Manzanas', TextType.italic),
            ]
        self.assertEqual(split_nodes_delimiter(nodelist, '_', TextType.italic), expected_output)
    def test_code(self):
        nodelist = [
            TextNode('Ismael Manzanero come `Manzanas`', TextType.plain_text),
            TextNode('Ismael Manzanero come `Manzanas`', TextType.code),
            TextNode('Ismael Manzanero come `Manzanas`', TextType.plain_text)
            ]
        expected_output = [
            TextNode('Ismael Manzanero come ', TextType.plain_text),
            TextNode('Manzanas', TextType.code),
            TextNode('Ismael Manzanero come `Manzanas`', TextType.code),
            TextNode('Ismael Manzanero come ', TextType.plain_text),
            TextNode('Manzanas', TextType.code),
            ]
        self.assertEqual(split_nodes_delimiter(nodelist, '`', TextType.code), expected_output)
    def test_start(self):
        nodelist = [
            TextNode('_Ismael_ Manzanero come Manzanas', TextType.plain_text),
            ]
        expected_output = [
            TextNode('Ismael', TextType.italic),
            TextNode(' Manzanero come Manzanas', TextType.plain_text),
            ]
        self.assertEqual(split_nodes_delimiter(nodelist, '_', TextType.italic), expected_output)
    def test_several(self):
        nodelist = [
            TextNode('Ismael _Manzanero_ _come_ _Manzanas_', TextType.plain_text),
            ]
        expected_output = [
            TextNode('Ismael ', TextType.plain_text),
            TextNode('Manzanero', TextType.italic),
            TextNode(' ', TextType.plain_text),
            TextNode('come', TextType.italic),
            TextNode(' ', TextType.plain_text),
            TextNode('Manzanas', TextType.italic),
            ]
        self.assertEqual(split_nodes_delimiter(nodelist, '_', TextType.italic), expected_output)


class test_extract_markdown_images(unittest.TestCase):
    def test_one_link(self):
        text = 'This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)'
        expected_output = [
            ("image", "https://i.imgur.com/zjjcJKZ.png")
            ]
        self.assertEqual(extract_markdown_images(text), expected_output)
        
    def test_several_links(self):
        text = 'This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). This is text with an ![image](https://i.imgur.com/zjjcJKZ.png).'
        expected_output = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("image", "https://i.imgur.com/zjjcJKZ.png")
            ]
        self.assertEqual(extract_markdown_images(text), expected_output)

        
class test_extract_markdown_links(unittest.TestCase):
    def test_one_link(self):
        text = 'This is text with a ![link](https://i.imgur.com/zjjcJKZ.png)'
        expected_output = [
            ("link", "https://i.imgur.com/zjjcJKZ.png")
            ]
        self.assertEqual(extract_markdown_images(text), expected_output)
        
    def test_several_links(self):
        text = 'This is text with a ![link](https://i.imgur.com/zjjcJKZ.png). This is text with a ![link](https://i.imgur.com/zjjcJKZ.png). This is text with a ![link](https://i.imgur.com/zjjcJKZ.png). This is text with a ![link](https://i.imgur.com/zjjcJKZ.png). '
        expected_output = [
            ("link", "https://i.imgur.com/zjjcJKZ.png"),
            ("link", "https://i.imgur.com/zjjcJKZ.png"),
            ("link", "https://i.imgur.com/zjjcJKZ.png"),
            ("link", "https://i.imgur.com/zjjcJKZ.png")
            ]
        self.assertEqual(extract_markdown_images(text), expected_output)

        
class test_split_nodes_image(unittest.TestCase):
    def test_two_images(self):
        node1 =  TextNode('hola mundo ![alt_text](imahen.com) hola mundo ![alt_text](iahen.com)', TextType.plain_text)
        expected_output = [
            TextNode('hola mundo ', TextType.plain_text),
            TextNode('alt_text', TextType.image, 'imahen.com'),
            TextNode(' hola mundo ', TextType.plain_text),
            TextNode('alt_text', TextType.image, 'iahen.com')
        ]
        self.assertEqual(split_nodes_image([node1]), expected_output)

    def test_two_images_same_link(self):
        node1 =  TextNode('hola mundo ![alt_text](imahen.com) hola mundo ![alt_text](imahen.com)', TextType.plain_text)
        expected_output = [
            TextNode('hola mundo ', TextType.plain_text),
            TextNode('alt_text', TextType.image, 'imahen.com'),
            TextNode(' hola mundo ', TextType.plain_text),
            TextNode('alt_text', TextType.image, 'imahen.com')
        ]
        self.assertEqual(split_nodes_image([node1]), expected_output)

    def test_images_at_start(self):
        node1 =  TextNode('![alt_text](imahen.com) hola mundo ![alt_text](imahen.com)', TextType.plain_text)
        expected_output = [
            TextNode('alt_text', TextType.image, 'imahen.com'),
            TextNode(' hola mundo ', TextType.plain_text),
            TextNode('alt_text', TextType.image, 'imahen.com')
        ]
        self.assertEqual(split_nodes_image([node1]), expected_output)

    def test_images_at_end(self):
        node1 =  TextNode('hola mundo ![alt_text](imahen.com)', TextType.plain_text)
        expected_output = [
            TextNode('hola mundo ', TextType.plain_text),
            TextNode('alt_text', TextType.image, 'imahen.com')
        ]
        self.assertEqual(split_nodes_image([node1]), expected_output)

    def test_images_at_edges_and_middle(self):
        node1 =  TextNode('![alt_text](imahens.com) hola mundo ![alt_text](imahen.com) hola mundo ![alt_text](imahen.com)', TextType.plain_text)
        expected_output = [
            TextNode('alt_text', TextType.image, 'imahens.com'),
            TextNode(' hola mundo ', TextType.plain_text),
            TextNode('alt_text', TextType.image, 'imahen.com'),
            TextNode(' hola mundo ', TextType.plain_text),
            TextNode('alt_text', TextType.image, 'imahen.com')
        ]
        self.assertEqual(split_nodes_image([node1]), expected_output)

    def test_images_together(self):
        node1 =  TextNode('![alt_text](imahens.com)![alt_text](imahen.com)![alt_text](imahen.com)', TextType.plain_text)
        expected_output = [
            TextNode('alt_text', TextType.image, 'imahens.com'),
            TextNode('alt_text', TextType.image, 'imahen.com'),
            TextNode('alt_text', TextType.image, 'imahen.com')
        ]
        self.assertEqual(split_nodes_image([node1]), expected_output)

        
class test_split_nodes_link(unittest.TestCase):
    def test_two_images(self):
        node1 =  TextNode('hola mundo [link_text](imahen.com) hola mundo [link_text](iahen.com)', TextType.plain_text)
        expected_output = [
            TextNode('hola mundo ', TextType.plain_text),
            TextNode('link_text', TextType.link, 'imahen.com'),
            TextNode(' hola mundo ', TextType.plain_text),
            TextNode('link_text', TextType.link, 'iahen.com')
        ]
        self.assertEqual(split_nodes_link([node1]), expected_output)

    def test_two_links_same_link(self):
        node1 =  TextNode('hola mundo [link_text](imahen.com) hola mundo [link_text](imahen.com)', TextType.plain_text)
        expected_output = [
            TextNode('hola mundo ', TextType.plain_text),
            TextNode('link_text', TextType.link, 'imahen.com'),
            TextNode(' hola mundo ', TextType.plain_text),
            TextNode('link_text', TextType.link, 'imahen.com')
        ]
        self.assertEqual(split_nodes_link([node1]), expected_output)

    def test_links_at_start(self):
        node1 =  TextNode('[link_text](imahen.com) hola mundo [link_text](imahen.com)', TextType.plain_text)
        expected_output = [
            TextNode('link_text', TextType.link, 'imahen.com'),
            TextNode(' hola mundo ', TextType.plain_text),
            TextNode('link_text', TextType.link, 'imahen.com')
        ]
        self.assertEqual(split_nodes_link([node1]), expected_output)

    def test_links_at_end(self):
        node1 =  TextNode('hola mundo [link_text](imahen.com)', TextType.plain_text)
        expected_output = [
            TextNode('hola mundo ', TextType.plain_text),
            TextNode('link_text', TextType.link, 'imahen.com')
        ]
        self.assertEqual(split_nodes_link([node1]), expected_output)

    def test_links_at_edges_and_middle(self):
        node1 =  TextNode('[link_text](imahens.com) hola mundo [link_text](imahen.com) hola mundo [link_text](imahen.com)', TextType.plain_text)
        expected_output = [
            TextNode('link_text', TextType.link, 'imahens.com'),
            TextNode(' hola mundo ', TextType.plain_text),
            TextNode('link_text', TextType.link, 'imahen.com'),
            TextNode(' hola mundo ', TextType.plain_text),
            TextNode('link_text', TextType.link, 'imahen.com')
        ]
        self.assertEqual(split_nodes_link([node1]), expected_output)

    def test_links_together(self):
        node1 =  TextNode('[link_text](imahens.com)[link_text](imahen.com)[link_text](imahen.com)', TextType.plain_text)
        expected_output = [
            TextNode('link_text', TextType.link, 'imahens.com'),
            TextNode('link_text', TextType.link, 'imahen.com'),
            TextNode('link_text', TextType.link, 'imahen.com')
        ]
        self.assertEqual(split_nodes_link([node1]), expected_output)


if __name__ == "__main__":
    unittest.main()