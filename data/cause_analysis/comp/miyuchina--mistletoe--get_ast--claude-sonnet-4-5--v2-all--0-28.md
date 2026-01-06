https://github.com/miyuchina/mistletoe/blob/0860a8662d386b0b9bee2512e8a078715703f980/./mistletoe/ast_renderer.py#L22-L47
```
@icontract.ensure(lambda result: isinstance(result, dict))
@icontract.ensure(lambda result: 'type' in result)
@icontract.ensure(lambda token, result: result['type'] == token.__class__.__name__)
@icontract.ensure(lambda token, result: 'content' not in vars(token) or 'content' in result)
@icontract.ensure(lambda token, result: 'footnotes' not in vars(token) or 'footnotes' in result)
@icontract.ensure(lambda token, result: 'header' not in vars(token) or 'header' in result)
@icontract.ensure(lambda token, result: token.children is None or 'children' in result)
@icontract.ensure(lambda token, result: token.children is None or isinstance(result.get('children'), list))
@icontract.ensure(lambda token, result: token.children is None or len(result['children']) == len(token.children))
```
```
return value - inner repository type


return value content

repository defined type
```
passed
```
@icontract.ensure(lambda result, token: isinstance(result, dict))
@icontract.ensure(lambda result, token: 'type' in result and result['type'] == token.__class__.__name__)
@icontract.ensure(lambda result, token: set(result.keys()) == ({'type'} | set(token.repr_attributes) | ({'content'} if 'content' in vars(token) else set()) | ({'footnotes'} if 'footnotes' in vars(token) else set()) | ({'header'} if 'header' in vars(token) else set()) | ({'children'} if getattr(token, 'children', None) is not None else set())))
@icontract.ensure(lambda result, token: all(((attr in vars(token) and result.get(attr) == getattr(token, attr)) or (attr not in vars(token) and attr not in result)) for attr in ('content', 'footnotes')))
@icontract.ensure(lambda result, token: all(result[attr] == getattr(token, attr) for attr in token.repr_attributes))
@icontract.ensure(lambda result, token: (('header' in vars(token) and 'header' in result and result['header'] == get_ast(getattr(token, 'header'))) or ('header' not in vars(token) and 'header' not in result)))
@icontract.ensure(lambda result, token: ((getattr(token, 'children', None) is not None and 'children' in result and result['children'] == [get_ast(child) for child in token.children]) or (getattr(token, 'children', None) is None and 'children' not in result)))
```
===== 28: failed =====
```
     for attrname in token.repr_attributes:
         node[attrname] = getattr(token, attrname)
     if 'header' in vars(token):
-        node['header'] = get_ast(getattr(token, 'header'))
+        node['XXheaderXX'] = get_ast(getattr(token, 'header'))
     if token.children is not None:
         node['children'] = [get_ast(child) for child in token.children]
-    return node+    return node
```
```
def get_ast(token):
    """
    Recursively unrolls token attributes into dictionaries (token.children
    into lists).

    Returns:
        a dictionary of token's attributes.
    """
    node = {}
    # Python 3.6 uses [ordered dicts] [1].
    # Put in 'type' entry first to make the final tree format somewhat
    # similar to [MDAST] [2].
    #
    #   [1]: https://docs.python.org/3/whatsnew/3.6.html
    #   [2]: https://github.com/syntax-tree/mdast
    node['type'] = token.__class__.__name__
    for attrname in ['content', 'footnotes']:
        if attrname in vars(token):
            node[attrname] = getattr(token, attrname)
    for attrname in token.repr_attributes:
        node[attrname] = getattr(token, attrname)
    if 'header' in vars(token):
        node['XXheaderXX'] = get_ast(getattr(token, 'header'))
    if token.children is not None:
        node['children'] = [get_ast(child) for child in token.children]
    return node

```
