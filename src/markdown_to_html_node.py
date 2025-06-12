from htmlnode import *
from textnode import *
from radical_functions import *
from markdown_to_blocks import *


def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    html_nodes = list(map(lambda text_node: text_node_to_html_node(text_node), text_nodes))
    return html_nodes

def get_heading_type(text):
    return f"h{len(text.strip().split()[0])}"

def get_heading_title(text):
    return text.split(" ", maxsplit=1)[1].strip()

def get_full_quote(text):
    return " ".join(list(map(lambda line: line[2: ], text.split("\n"))))

def extract_code(text):
    if len(text) <= 6:
        print(text)
        raise ValueError("Unexpected Code Segement.")
    return text[4:-4]

def get_list(text, block_type):
    child_nodes = []
    for line in text.split("\n"):
        html_nodes = []
        if block_type == BlockTypes.Ordered_List:
            _, item = line.split(". ", maxsplit=1)
            text_nodes = text_to_text_nodes(item)
            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                html_nodes.append(html_node)
            child_node = ParentNode(tag="li", children=html_nodes)
            child_nodes.append(child_node)
        elif block_type == BlockTypes.Unordered_List:
            item = line[2:]
            text_nodes = text_to_text_nodes(item)
            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                html_nodes.append(html_node)
            child_node = ParentNode(tag="li", children=html_nodes)
            child_nodes.append(child_node)
        else:
            raise ValueError("Not a list")
    match block_type:
        case BlockTypes.Ordered_List: return ParentNode(tag="ol", children=child_nodes)
        case BlockTypes.Unordered_List: return ParentNode(tag="ul", children=child_nodes)
        case _: raise ValueError("Not a list")



def markdown_to_html_node(document):
    md_blocks = markdown_to_blocks(document)
    html_nodes = []
    for block in md_blocks:
        match (block_type_of(block)):
            case BlockTypes.Heading: html_nodes.append(LeafNode(tag=get_heading_type(block), value=get_heading_title(block)))
            case BlockTypes.Quote:
                text = get_full_quote(block)
                child_nodes = text_to_children(text)
                html_nodes.append(ParentNode(tag="blockquote", children=child_nodes))
            case BlockTypes.Code: html_nodes.append(ParentNode(tag="pre", children=[LeafNode(tag="code", value=extract_code(block))]))
            case BlockTypes.Ordered_List: html_nodes.append(get_list(block, BlockTypes.Ordered_List))
            case BlockTypes.Unordered_List: html_nodes.append(get_list(block, BlockTypes.Unordered_List))
            case _:
                htm_nodes = text_to_children(block)
                html_nodes.append(ParentNode(tag="p", children=htm_nodes))
    return ParentNode("div", html_nodes)






if __name__ == "__main__":
    with open("public/WWDC.md") as f:
        document = f.read()
        html = markdown_to_html_node(document).to_html()
        print(html)
