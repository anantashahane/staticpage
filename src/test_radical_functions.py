import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from radical_functions import text_node_to_html_node, split_nodes_delimiter

class TestConversion(unittest.TestCase):
    def test_conversion(self):
        print("Testing for all conversion to be translated.")

        textNode1 = TextNode("This is normal text", TextType.NORMAL_TYPE)
        textNode2 = TextNode("This is bold text", TextType.BOLD_TYPE)
        textNode3 = TextNode("This is italic text", TextType.ITALIC_TYPE)
        textNode4 = TextNode("This is code text", TextType.CODE_TYPE)
        textNode5 = TextNode("This is link text", TextType.LINK_TYPE, "www.apple.com")
        textNode6 = TextNode("Anna Williams", TextType.IMAGE_TYPE, "https://tekken.fandom.com/wiki/Anna_Williams?file=Anna_TK8_Render_Large.png")

        self.assertEqual(text_node_to_html_node(textNode1).to_html(), "This is normal text")
        self.assertEqual(text_node_to_html_node(textNode2).to_html(), "<b>This is bold text</b>")
        self.assertEqual(text_node_to_html_node(textNode3).to_html(), "<i>This is italic text</i>")
        self.assertEqual(text_node_to_html_node(textNode4).to_html(), "<code>This is code text</code>")
        self.assertEqual(text_node_to_html_node(textNode5).to_html(), '<a href="www.apple.com">This is link text</a>')
        self.assertEqual(text_node_to_html_node(textNode6).to_html(), '<img src="https://tekken.fandom.com/wiki/Anna_Williams?file=Anna_TK8_Render_Large.png" alt="Anna Williams"></img>')

    def test_conversion_failures(self):
        print("Testing conversion value failure.")
        textNode1 = TextNode("Bruh", None)

        self.assertRaises(Exception, text_node_to_html_node, textNode1)

    def test_split_nodes_delimiter(self):
        print("Testing Delimiter Execution.")
        self.assertEqual(split_nodes_delimiter([TextNode("This is a **bold** text", TextType.NORMAL_TYPE)], "**", TextType.BOLD_TYPE),
        [TextNode("This is a ", TextType.NORMAL_TYPE), TextNode("bold", TextType.BOLD_TYPE), TextNode(" text", TextType.NORMAL_TYPE)])

        self.assertEqual(split_nodes_delimiter([TextNode("This is a _italic_ text", TextType.NORMAL_TYPE)], "_", TextType.ITALIC_TYPE),
        [TextNode("This is a ", TextType.NORMAL_TYPE), TextNode("italic", TextType.ITALIC_TYPE), TextNode(" text", TextType.NORMAL_TYPE)])

        self.assertEqual(split_nodes_delimiter([TextNode("This is a `code` text", TextType.NORMAL_TYPE)], "`", TextType.CODE_TYPE),
        [TextNode("This is a ", TextType.NORMAL_TYPE), TextNode("code", TextType.CODE_TYPE), TextNode(" text", TextType.NORMAL_TYPE)])

    def test_non_recursion(self):
        print("Testing Delimiter Non Recursion.")
        self.assertEqual(split_nodes_delimiter([TextNode("This is a **bold** text", TextType.BOLD_TYPE)], "**", TextType.BOLD_TYPE),
        [TextNode("This is a **bold** text", TextType.BOLD_TYPE)])
