import unittest
from markdown_to_blocks import markdown_to_blocks, block_type_detector, BlockType

class test_markdown_to_blocks(unittest.TestCase):
    def test_global(self):
        input = """



Ismael Manzanero   

Se come su **Manzana**

Ismael te lo ruego

Guarda tu banana

"""
        expected = [
            "Ismael Manzanero",
            "Se come su **Manzana**",
            "Ismael te lo ruego",
            "Guarda tu banana"
        ]
        self.assertEqual(markdown_to_blocks(input), expected)

class text_block_type_detector(unittest.TestCase):
    def test_one_by_one(self):
        text = """Hola ismael
Manzanero"""
        self.assertEqual(block_type_detector(text), BlockType.paragraph)

        text = """###### Hola ismael
Manzanero"""
        self.assertEqual(block_type_detector(text), BlockType.heading)

        text = """####### Hola ismael
Manzanero"""
        self.assertEqual(block_type_detector(text), BlockType.paragraph)

        text = """```ismu
Hola ismael
Manzanero
```"""
        self.assertEqual(block_type_detector(text), BlockType.code)

        text = """>ismu
>Hola ismael
>Manzanero"""
        self.assertEqual(block_type_detector(text), BlockType.quote)

        text = """>ismu
>Hola ismael
Manzanero"""
        self.assertEqual(block_type_detector(text), BlockType.paragraph)

        text = """-ismu
-Hola ismael
-Manzanero"""
        self.assertEqual(block_type_detector(text), BlockType.unordered_list)

        text = """-ismu
-Hola ismael
Manzanero"""
        self.assertEqual(block_type_detector(text), BlockType.paragraph)

        text = """.ismu
.Hola ismael
.Manzanero"""
        self.assertEqual(block_type_detector(text), BlockType.ordered_list)

        text = """.ismu
.Hola ismael
Manzanero"""
        self.assertEqual(block_type_detector(text), BlockType.paragraph)

    def test_multiple_types(self):
        text = """### Lista de Compras
- Ismael
- Manzanero"""
        self.assertEqual(block_type_detector(text), BlockType.heading)

        text = """. Lista de Compras
- Ismael
> Manzanero"""
        self.assertEqual(block_type_detector(text), BlockType.paragraph)