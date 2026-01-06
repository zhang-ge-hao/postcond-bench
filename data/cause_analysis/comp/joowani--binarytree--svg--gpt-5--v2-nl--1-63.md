https://github.com/joowani/binarytree/blob/74e0c0bf204a0a2789c45a07264718f963db37fe/./binarytree/__init__.py#L521-L588
```
@icontract.snapshot(lambda self: len(self.levelorder), name="node_count")
@icontract.snapshot(lambda self: str(self.val), name="root_value")
@icontract.ensure(lambda result: isinstance(result, str))
@icontract.ensure(lambda result: "<svg" in result and "</svg>" in result)
@icontract.ensure(lambda result: 'xmlns="http://www.w3.org/2000/svg"' in result)
@icontract.ensure(lambda result: '<g stroke="#000000">' in result and "</g>" in result)
@icontract.ensure(lambda result: 'width="' in result and 'height="' in result)
@icontract.ensure(lambda result: ".value {" in result and ".node {" in result)
@icontract.ensure(lambda result: "<circle" in result)
@icontract.ensure(lambda node_radius, result: f'r="{node_radius}"' in result)
@icontract.ensure(lambda OLD, result: result.count("<circle") == OLD.node_count)
@icontract.ensure(lambda OLD, result: f">{OLD.root_value}<" in result or OLD.root_value in result)
```
```
return value - primitive-like/scalar types


return value content

primitive-like/scalar types
```
passed
```
@icontract.snapshot(
    lambda self, node_radius: (
        (lambda nodes, tree_height, scale:
            (lambda coord:
                _SVG_XML_TEMPLATE.format(
                    width=scale * (2 ** tree_height),
                    height=scale * (2 + tree_height),
                    body="\n".join(
                        [
                            '<line x1="{0}" y1="{1}" x2="{2}" y2="{3}"/>'.format(
                                coord((get_index(self, node_child) - 1) // 2)[0],
                                coord((get_index(self, node_child) - 1) // 2)[1],
                                coord(get_index(self, node_child))[0],
                                coord(get_index(self, node_child))[1],
                            )
                            for node_child in nodes[1:]
                        ][::-1]
                        +
                        [
                            s
                            for node in nodes
                            for (cx, cy) in [coord(get_index(self, node))]
                            for s in (
                                '<circle class="node" cx="{0}" cy="{1}" r="{2}"/>'.format(
                                    cx, cy, node_radius
                                ),
                                '<text class="value" x="{0}" y="{1}">{2}</text>'.format(
                                    cx, cy, node.value
                                ),
                            )
                        ]
                    ),
                )
            )(
                lambda idx: (
                    1
                    + node_radius
                    + scale
                    * (
                        (
                            1 << (
                                tree_height
                                - ((idx + 1).bit_length() - 1)
                                + 1
                            )
                        )
                        * (
                            idx
                            - (
                                (1 << ((idx + 1).bit_length() - 1))
                                - 1
                            )
                        )
                        + (
                            1 << (
                                tree_height
                                - ((idx + 1).bit_length() - 1)
                            )
                        )
                        - 1
                    ) / 2,
                    scale * (1 + ((idx + 1).bit_length() - 1)),
                )
            )
        )(
            list(self.levelorder),
            self.height,
            node_radius * 3,
        )
    ),
    name="svg_expected",
)
@icontract.ensure(
    lambda self, node_radius, result, OLD:
        result == OLD.svg_expected,
)

```
===== 63: failed =====
```
         def add_node(node_x: int, node_y: int, node_value: NodeValue) -> None:
             x, y = scale_x(node_x, node_y), scale_y(node_y)
             xml.append(f'<circle class="node" cx="{x}" cy="{y}" r="{node_radius}"/>')
-            xml.append(f'<text class="value" x="{x}" y="{y}">{node_value}</text>')
+            xml.append(f'<text class="value" x="{x}" y="{y}">{node_value} (Node)</text>')
 
         current_nodes = [self.left, self.right]
         has_more_nodes = True
```
```
    def svg(self, node_radius: int = 16) -> str:
        """Generate SVG XML.

        :param node_radius: Node radius in pixels (default: 16).
        :type node_radius: int
        :return: Raw SVG XML.
        :rtype: str
        """
        tree_height = self.height
        scale = node_radius * 3
        xml: Deque[str] = deque()

        def scale_x(x: int, y: int) -> float:
            diff = tree_height - y
            x = 2 ** (diff + 1) * x + 2**diff - 1
            return 1 + node_radius + scale * x / 2

        def scale_y(y: int) -> float:
            return scale * (1 + y)

        def add_edge(parent_x: int, parent_y: int, node_x: int, node_y: int) -> None:
            xml.appendleft(
                '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'.format(
                    x1=scale_x(parent_x, parent_y),
                    y1=scale_y(parent_y),
                    x2=scale_x(node_x, node_y),
                    y2=scale_y(node_y),
                )
            )

        def add_node(node_x: int, node_y: int, node_value: NodeValue) -> None:
            x, y = scale_x(node_x, node_y), scale_y(node_y)
            xml.append(f'<circle class="node" cx="{x}" cy="{y}" r="{node_radius}"/>')
            xml.append(f'<text class="value" x="{x}" y="{y}">{node_value} (Node)</text>')

        current_nodes = [self.left, self.right]
        has_more_nodes = True
        y = 1

        add_node(0, 0, self.value)

        while has_more_nodes:

            has_more_nodes = False
            next_nodes: List[Optional[Node]] = []

            for x, node in enumerate(current_nodes):
                if node is None:
                    next_nodes.append(None)
                    next_nodes.append(None)
                else:
                    if node.left is not None or node.right is not None:
                        has_more_nodes = True

                    add_edge(x // 2, y - 1, x, y)
                    add_node(x, y, node.value)

                    next_nodes.append(node.left)
                    next_nodes.append(node.right)

            current_nodes = next_nodes
            y += 1

        return _SVG_XML_TEMPLATE.format(
            width=scale * (2**tree_height),
            height=scale * (2 + tree_height),
            body="\n".join(xml),
        )
```
