class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        if children:
            if isinstance(children, list):
                self.children = children
            else:
                self.children = [children]
        else:
            self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Parent Node, not to be implemented.")

    def props_to_html(self):
        if self.props:
            return f' {" ".join(list(map(lambda item: f"{item[0]}=\"{item[1]}\"", self.props.items())))}'
        return ""

    def __repr__(self):
        strings = ["====HTML Node====="]
        if self.tag:
            strings.append(f"\t tag: {self.tag}")
        if self.value:
            strings.append(f"\t value: {self.value}")
        if self.children:
            strings.append(f"\t chidren: {self.children}")
        if self.props:
            strings.append(f"\t props: {self.props_to_html()}")
        return "\n".join(strings)


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(value=value, tag=tag, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node not assigned value.")

        render_string = ""
        if self.tag:
            render_string += f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            render_string = self.value
        return render_string


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent Node must have a tag.")
        if not self.children:
            raise ValueError("Childless Parent is un acceptable.")
        return f"<{self.tag}{self.props_to_html()}>\n{'\n'.join(list(map(lambda object: object.to_html(), self.children)))}\n</{self.tag}>"

if __name__ == "__main__":
    htmlnode = HTMLNode(props={
        "href": "https://www.google.com",
        "target": "_blank",
    })
    print(htmlnode.props_to_html())
    print(htmlnode)
    print(LeafNode("p", "This is a paragraph of text.").to_html())
    print(LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html())

    print("===========PARENT NODE================")
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(node.to_html())
