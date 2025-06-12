import re
from enum import Enum

class BlockTypes(Enum):
    Paragraph = "paragraph"
    Heading = "heading"
    Code = "code"
    Quote = "quote"
    Unordered_List = "unordered-list"
    Ordered_List = "ordered-list"

def markdown_to_blocks(document):
    return list(map(lambda block: block.strip(), document.split("\n\n")))


def block_type_of(block):
    def check_for_consistent_types(start_op):
        for line in block.split("\n"):
            if not line.startswith(start_op):
                return False
        return True

    def check_for_ordered_list():
        for line in block.split("\n"):
            if len(re.findall(r"^[0-9]+.\ ", line)) == 0:
                return False
        return True

    def is_heading():
        found = re.findall(r"^#+", block)
        if found:
            return len(found[0]) in range(1, 7)
        return False

    if is_heading():
        return BlockTypes.Heading
    elif block.startswith("```") and block.endswith("```"):
        return BlockTypes.Code
    elif check_for_consistent_types(">"):
        return BlockTypes.Quote
    elif check_for_consistent_types("-"):
        return BlockTypes.Unordered_List
    elif check_for_ordered_list():
        return BlockTypes.Ordered_List
    else:
        return BlockTypes.Paragraph

def extract_title(document):
    for block in document.split("\n\n"):
        if block_type_of(block) == BlockTypes.Heading:
            return block.split(" ", maxsplit=1)[1].strip()
    raise Exception("Markdown without heading.")
# if __name__ == "__main__":
#     print(markdown_to_blocks("""
# This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line

# - This is a list
# - with items
# """))

# print(block_type_of("A # Heading 1"))
# print(block_type_of("## Heading 2"))
# print(block_type_of("### Heading 3"))
# print(block_type_of("#### Heading 4"))
# print(block_type_of("##### Heading 5"))
# print(block_type_of("###### Heading 6"))
# print(block_type_of("####### Heading 6"))
# print(block_type_of("""```
# Swift is god language
# ```"""))
