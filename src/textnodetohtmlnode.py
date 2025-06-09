from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.NORMAL_TYPE: return LeafNode(None, text_node.text)
        case TextType.BOLD_TYPE: return LeafNode("b", text_node.text)
        case TextType.ITALIC_TYPE: return LeafNode("i", text_node.text)
        case TextType.CODE_TYPE: return LeafNode("code", text_node.text)
        case TextType.LINK_TYPE: return LeafNode("a", text_node.text, props={"href" : text_node.url})
        case TextType.IMAGE_TYPE: return LeafNode("img", "", props={"src" : text_node.url, "alt": text_node.text})
        case _: raise Exception(f"Unknown text type {text_node.text_type}.")
