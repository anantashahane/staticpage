import unittest
from markdown_to_html_node import markdown_to_html_node

class TestFramework(unittest.TestCase):
    def integration_test(self):
        self.maxDiff = None
        print("Framework Testin")
        result="""<div>
<h1>Apple</h1>
<p>
This year, the
<b>WWDC</b>
 was the biggest event, with top
<code>DEVELOPERS</code>

contributing the very best they have to offer, and Apple providing the
most informationally
<i>dense</i>
 Keynote in recent memory.
</p>
<blockquote cite="">
Stay Hungry, Stay Foolish.
</blockquote>
<h2>Macs</h2>
<ul>
<li>MacBook Air</li>
<li>MacBook Pro</li>
<li>Mac Mini</li>
<li>Mac Studio</li>
<li>Mac Pro</li>
</ul>
<h2>Best Shows</h2>
<ol>
<li value="3">Ted Mosbey</li>
<li value="2">Foundation</li>
<li value="1">See</li>
</ol>
<h2>Swift is Swifter than you think.</h2>
<pre>
<code>func Factorial(n : Int) -> Int {
    return n <= 0 ? 1 : (1...n).reduce(1, *)
</code>
</pre>
</div>"""
        input="""# Apple

This year, the **WWDC** was the biggest event, with top `DEVELOPERS`
contributing the very best they have to offer, and Apple providing the
most informationally _dense_ Keynote in recent memory.

> Stay Hungry,
> Stay Foolish.

## Macs

- MacBook Air
- MacBook Pro
- Mac Mini
- Mac Studio
- Mac Pro

## Best Shows

3. Ted Mosbey
2. Foundation
1. See

## Swift is Swifter than you think.

```
func Factorial(n : Int) -> Int {
    return n <= 0 ? 1 : (1...n).reduce(1, *)
}```"""
        self.assertEqual(markdown_to_html_node(input).to_html(), result)
