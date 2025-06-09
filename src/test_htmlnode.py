import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        print("Testing HTML Class Initialisation")
        node1 = HTMLNode(tag="h1", value="Burning Soul", props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node1.tag, "h1")
        self.assertEqual(node1.value, "Burning Soul")
        self.assertEqual(node1.props, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertIsNone(node1.children)

    def test_children_is_list(self):
        print("Testing HTML Children is always list | None")
        node1 = HTMLNode(tag="h1", value="Burning Soul", props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        node2 = HTMLNode(tag="div", props={"color":"#AEAEAE"}, children=node1)
        self.assertIsInstance(node2.children, list)
        self.assertIsNone(node1.children)

    def test_leaf_to_html_p(self):
        print("Testing HTML Leaf Node")
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_raises_error(self):
        print("Testing HTML Leaf Node, Missing value")
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_adds_props(self):
        print("Testing prop, assignment in HTML Leaf Node")
        self.assertEqual(LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        print("Parent Node: Testing children rendering")
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div>\n<span>child</span>\n</div>")

    def test_to_html_with_grandchildren(self):
        print("Parent Node: Testing recurrsive children rendering")
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),"<div>\n<span>\n<b>grandchild</b>\n</span>\n</div>"
        )

    def test_parent_value_error(self):
        print("Parent Node: Raises error for missing values.")
        child_node = LeafNode("b", "grandchild")
        parent_node_1 = ParentNode("span", None)
        parent_node_2 = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node_1.to_html)
        self.assertRaises(ValueError, parent_node_2.to_html)
