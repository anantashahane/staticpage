import unittest
from markdown_to_blocks import block_type_of, extract_title, markdown_to_blocks, BlockTypes


class TestMarkdowntoBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        print("Testing markdown to blocks.")
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks2(self):
        print("Testing markdown to blocks.")
        md = """
# Quantum Computing

- Quantum Computing is just like traditional computing,
- hence, it can only work on problems that traditional computers can work on.

- However, it distinguishes itself, by the compute time,
    - Thanks to **super position** and **entanglement**.

    - It is the **hype** now.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
            [
            "# Quantum Computing",
            "- Quantum Computing is just like traditional computing,\n- hence, it can only work on problems that traditional computers can work on.",
            "- However, it distinguishes itself, by the compute time,\n    - Thanks to **super position** and **entanglement**.", "- It is the **hype** now."
        ])

    def test_BlockTypesOfHeadings(self):
        print("Testing block type of : Headings")

        h1 = "# Heading 1"
        h2 = "## Heading 2"
        h3 = "### Heading 3"
        h4 = "#### Heading 4"
        h5 = "##### Heading 5"
        h6 = "###### Heading 6"
        h7 = "####### Heading 7"

        self.assertEqual(block_type_of(h1), BlockTypes.Heading)
        self.assertEqual(block_type_of(h2), BlockTypes.Heading)
        self.assertEqual(block_type_of(h3), BlockTypes.Heading)
        self.assertEqual(block_type_of(h4), BlockTypes.Heading)
        self.assertEqual(block_type_of(h5), BlockTypes.Heading)
        self.assertEqual(block_type_of(h6), BlockTypes.Heading)
        self.assertEqual(block_type_of(h7), BlockTypes.Paragraph)

    def test_BlockTypesofCode(self):
        print("Testing block type of : Code")
        code = """```
            Swift is the best language out there.
        ```"""
        inline = "```rm -rf /```"
        not_code = """``Bruh``"""

        self.assertEqual(block_type_of(code), BlockTypes.Code)
        self.assertEqual(block_type_of(inline), BlockTypes.Code)
        self.assertEqual(block_type_of(not_code), BlockTypes.Paragraph)

    def test_BlockTypesofQuote(self):
        print("Testing block type of : Quote")
        quote = """> Idiocy, is doing
> the same thing again
> and again and expecting
> something different."""
        inline = """> Idiocy, is doing
> the same thing again
> and again.....
    > and again and expecting
    > something different.
"""
        not_code = "+> Meh"

        self.assertEqual(block_type_of(quote), BlockTypes.Quote)
        self.assertEqual(block_type_of(inline), BlockTypes.Paragraph)
        self.assertEqual(block_type_of(not_code), BlockTypes.Paragraph)

    def test_BlockTypesofUL(self):
        print("Testing block type of : Unordered List")
        quote = """- Idiocy, is doing
- the same thing again
- and again and expecting
- something different."""
        inline = """- Idiocy, is doing
- the same thing again
- and again.....
+ and again and expecting
+ something different.
"""
        not_code = "+ Meh"

        self.assertEqual(block_type_of(quote), BlockTypes.Unordered_List)
        self.assertEqual(block_type_of(inline), BlockTypes.Paragraph)
        self.assertEqual(block_type_of(not_code), BlockTypes.Paragraph)

    def test_BlockTypesofOL(self):
        print("Testing block type of : Unordered List")
        quote = """1. Anna Williams
2. Nina Williams
3. Emilie De Rochefort
4. Zafina"""
        inline = """1. Kazuya Mishima
2. Jin Kazama
3. Heihachi Mishima
*. Reina Mishima.
+ something different.
"""
        not_code = "+ Meh"

        self.assertEqual(block_type_of(quote), BlockTypes.Ordered_List)
        self.assertEqual(block_type_of(inline), BlockTypes.Paragraph)
        self.assertEqual(block_type_of(not_code), BlockTypes.Paragraph)

    def test_extract_title(self):
        self.assertEqual(extract_title("# I am batman "), "I am batman")
        self.assertEqual(extract_title("#  I am catwoman "), "I am catwoman")
        self.assertRaises(Exception, extract_title, ("Man, fuck that."))
