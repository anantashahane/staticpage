from calendar import c
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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL_TYPE:
            text_segments = node.text.split(delimiter)
            delimiter_active = False
            for text_segment in text_segments:
                if text_segment != "":
                    if delimiter_active:
                        new_node = TextNode(text_segment, text_type)
                        new_nodes.append(new_node)
                    else:
                        new_node = TextNode(text_segment, node.text_type, node.url)
                        new_nodes.append(new_node)
                delimiter_active = not delimiter_active
        else:
            new_nodes.append(node)
    return new_nodes


if __name__ == "__main__":
    print(split_nodes_delimiter([TextNode("This is text with a `code block` word.", TextType.NORMAL_TYPE),
    TextNode("`func Factorial(n : Int) -> Int` returns `Int` which is a factorial of the input parameter.", TextType.NORMAL_TYPE)],
    "`", TextType.CODE_TYPE))
