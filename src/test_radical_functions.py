import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from radical_functions import *

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

    def test_link_extractor(self):
        print("Testing Link Extraction.")
        matches = extract_image_link("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_link("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_link_node_splitter(self):
        print("Testing Link splitting.")
        nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                            TextType.NORMAL_TYPE)]
        matches = split_nodes_link(nodes)
        self.assertEqual(
            [TextNode("This is text with a link ", TextType.NORMAL_TYPE),
            TextNode("to boot dev", TextType.LINK_TYPE, url="https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL_TYPE),
            TextNode("to youtube", TextType.LINK_TYPE, url="https://www.youtube.com/@bootdotdev")], matches)

    def test_image_node_splitter(self):
        print("Testing Image splitting.")
        nodes = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                            TextType.NORMAL_TYPE)]
        matches = split_nodes_image(nodes)
        self.assertEqual(
            [TextNode("This is text with an ", TextType.NORMAL_TYPE),
            TextNode("image", TextType.IMAGE_TYPE, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.NORMAL_TYPE),
            TextNode("second image", TextType.IMAGE_TYPE, url="https://i.imgur.com/3elNhQu.png")], matches)

    def test_text_to_text_node(self):
        print("Testing integrity.")
        nodes = text_to_text_nodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected = [
            TextNode("This is ", TextType.NORMAL_TYPE),
            TextNode("text", TextType.BOLD_TYPE),
            TextNode(" with an ", TextType.NORMAL_TYPE),
            TextNode("italic", TextType.ITALIC_TYPE),
            TextNode(" word and a ", TextType.NORMAL_TYPE),
            TextNode("code block", TextType.CODE_TYPE),
            TextNode(" and an ", TextType.NORMAL_TYPE),
            TextNode("obi wan image", TextType.IMAGE_TYPE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL_TYPE),
            TextNode("link", TextType.LINK_TYPE, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)
