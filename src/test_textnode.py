import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("Testing equality for TextNode.")
        node1 = TextNode("This is a text node", TextType.BOLD_TYPE)
        node2 = TextNode("This is a text node", TextType.BOLD_TYPE)
        self.assertEqual(node1, node2)

    def test_inequality(self):
        print("Testing inequality for TextNode.")
        node1 = TextNode("This is a text node", TextType.ITALIC_TYPE)
        node2 = TextNode("This is a text node", TextType.BOLD_TYPE)
        node3 = TextNode("This is a text node..", TextType.BOLD_TYPE)
        node4 = TextNode("This is a text node..", TextType.BOLD_TYPE)

        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node2, node3)
        self.assertEqual(node3, node4)

    def test_hasUrl(self):
        print("Testing URL for TextNode.")
        node1 = TextNode("link", TextType.LINK_TYPE, "apple.com")
        self.assertEqual("apple.com", node1.url)

        node2 = TextNode("Hello Boot", TextType.BOLD_TYPE)
        self.assertIsNone(node2.url)



if __name__ == "__main__":
    unittest.main()
