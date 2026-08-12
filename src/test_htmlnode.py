import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class test_HTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode('b', 'hola mundo')
        node2 = HTMLNode('b', 'hola mundo', None, None)
        self.assertEqual(node1, node2)
    def test_not_eq(self):
        node1 = HTMLNode('b', 'hola mundo')
        node2 = HTMLNode('p', 'hola mundos', None, None)
        self.assertNotEqual(node1, node2)
    def test_instance(self):
        node1 = HTMLNode('b', 'hola mundo')
        self.assertIsInstance(node1, HTMLNode)


class test_LeafNode(unittest.TestCase):
    def test_eq(self):
        node1 = LeafNode('b', 'hola mundo')
        node2 = LeafNode('b', 'hola mundo', None)
        self.assertEqual(node1, node2)
    def test_leaf_to_html(self):
        node1 = LeafNode('b', 'hola mundo')
        self.assertEqual(node1.to_html(), '<b>hola mundo</b>')
    def test_repr(self):
        node1 = LeafNode('a', 'hola boot', {'href' : 'https://boot.dev'})
        self.assertEqual(node1.__repr__(), "LeafNode(a, hola boot, {'href': 'https://boot.dev'})")


class test_ParentNode(unittest.TestCase):
    def test_nesting_tohtml_pnn(self):
        node1 = LeafNode('span', 'hola ismu')
        node2 = ParentNode('p', [node1, LeafNode('span', 'hola ismu')])
        self.assertEqual(node2.to_html(), '<p><span>hola ismu</span><span>hola ismu</span></p>')
    def test_nesting_tohtml_ppn(self):
        node1 = LeafNode('span', 'hola ismu')
        node2 = ParentNode('p', [node1])
        node3 = ParentNode('p', [node2])
        self.assertEqual(node3.to_html(), '<p><p><span>hola ismu</span></p></p>')
    def test_no_children_error(self):
        node = ParentNode('p', [])
        with self.assertRaises(ValueError):
            node.to_html()
    def test_no_tag_error(self):
        node1 = LeafNode('span', 'hola ismu')
        node2 = ParentNode(None, [node1]) # type: ignore
        with self.assertRaises(ValueError):
            node2.to_html()
if __name__ == "__main__":
    unittest.main()