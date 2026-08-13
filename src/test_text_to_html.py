from text_to_html import markdown_to_html_node
import unittest

class test_text_text_to_html(unittest.TestCase):
    def test_bold_list_two_p(self):
        text="""
Hola, soy ismael manzanero, vengo del **futuro** para robarme tus manzanas >:D

- Ismu = hola
- Manzanero = diablo
"""
        expected = "<div><p>Hola, soy ismael manzanero, vengo del <b>futuro</b> para robarme tus manzanas >:D</p><ul><li>Ismu = hola</li><li>Manzanero = diablo</li></ul></div>"
        self.assertEqual(markdown_to_html_node(text), expected)

    def test_italics_img_two_p(self):
        text="""
Hola, soy ismael _manzanero_

imagen épica: ![hola](ismu.com)
"""
        expected = "<div><p>Hola, soy ismael <i>manzanero</i></p><p>imagen épica: <img src=\"ismu.com\" alt=\"hola\"></img></p></div>"
        self.assertEqual(markdown_to_html_node(text), expected)

    def test_code_link_two_p(self):
        text="""
Hola, soy ismael `manzanero`

link épico: [hola](ismu.com)
"""
        expected = "<div><p>Hola, soy ismael <code>manzanero</code></p><p>link épico: <a href=\"ismu.com\">hola</a></p></div>"
        self.assertEqual(markdown_to_html_node(text), expected)

    def test_headers(self):
        text="""
### hola

# hola
"""
        expected = "<div><h3>hola</h3><h1>hola</h1></div>"
        self.assertEqual(markdown_to_html_node(text), expected)
    def test_quotes(self):
        text="""
> Hola
> esta es una cita
"""
        expected = "<div><blockquote> Hola esta es una cita</blockquote></div>"
        self.assertEqual(markdown_to_html_node(text,True), expected)