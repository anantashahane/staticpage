import re
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

def extract_image_link(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_link(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(text_nodes):
    new_nodes = []
    for node in text_nodes:
        text = node.text
        pre_text = ""
        links = extract_image_link(text)
        if links:
            for (alt, url) in links:
                md_link = f"![{alt}]({url})"
                try:
                    pre_text, text = text.split(md_link)
                except:
                    text = ""
                if pre_text:
                    new_nodes.append(TextNode(pre_text, node.text_type))
                new_nodes.append(TextNode(alt, TextType.IMAGE_TYPE, url=url))
            if text:
                new_nodes.append(TextNode(text, node.text_type))

        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(text_nodes):
    new_nodes = []
    for node in text_nodes:
        text = node.text
        pre_text = ""
        links = extract_link(text)
        if links:
            for (alt, url) in links:
                md_link = f"[{alt}]({url})"
                try:
                    pre_text, text = text.split(md_link)
                except:
                    text = ""
                if pre_text:
                    new_nodes.append(TextNode(pre_text, node.text_type))
                new_nodes.append(TextNode(alt, TextType.LINK_TYPE, url=url))
            if text:
                new_nodes.append(TextNode(text, node.text_type))

        else:
            new_nodes.append(node)
    return new_nodes

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.NORMAL_TYPE)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TYPE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TYPE)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TYPE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes




if __name__ == "__main__":
    text = "This is **bold font** with an _italic font_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    for node in text_to_text_nodes(text):
        print(node)
