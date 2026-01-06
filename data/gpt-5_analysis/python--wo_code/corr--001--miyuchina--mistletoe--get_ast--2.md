https://github.com/miyuchina/mistletoe/blob/0860a8662d386b0b9bee2512e8a078715703f980/./mistletoe/ast_renderer.py#L22-L47
```
@icontract.ensure(lambda result: isinstance(result, dict))
@icontract.ensure(lambda result, token: 'type' in result and result['type'] == type(token).__name__)
@icontract.ensure(lambda result, token: (not hasattr(token, 'children')) or ('children' in result and isinstance(result['children'], list) and len(result['children']) == len(token.children)))
@icontract.ensure(lambda result, token: (not hasattr(token, 'children')) or all(isinstance(child_ast, dict) for child_ast in result['children']))
@icontract.ensure(lambda result, token: (not hasattr(token, 'children')) or all('type' in result['children'][i] and result['children'][i]['type'] == type(token.children[i]).__name__ for i in range(len(token.children))))
@icontract.ensure(lambda result, token: all((k in result) and (
    (not hasattr(v, '__dict__') and not isinstance(v, list) and result[k] == v) or
    (hasattr(v, '__dict__') and isinstance(result[k], dict) and 'type' in result[k] and result[k]['type'] == type(v).__name__) or
    (isinstance(v, list) and isinstance(result[k], list) and len(result[k]) == len(v) and all(
        (hasattr(v[i], '__dict__') and isinstance(result[k][i], dict) and 'type' in result[k][i] and result[k][i]['type'] == type(v[i]).__name__) or
        (not hasattr(v[i], '__dict__') and result[k][i] == v[i])
        for i in range(len(v))
    ))
) for (k, v) in getattr(token, '__dict__', {}).items() if k != 'children'))
```
```
Hallucination.

The last postcondition validate all attributes.
But the implementation only involves type, content, footnotes, etc.
LLM has hallucination that no other attributes exist, while _parent, _children, etc. also exist.
```
icontract_fail
```
@icontract.ensure(lambda result, token: isinstance(result, dict))
@icontract.ensure(lambda result, token: 'type' in result and result['type'] == token.__class__.__name__)
@icontract.ensure(lambda result, token: set(result.keys()) == ({'type'} | set(token.repr_attributes) | ({'content'} if 'content' in vars(token) else set()) | ({'footnotes'} if 'footnotes' in vars(token) else set()) | ({'header'} if 'header' in vars(token) else set()) | ({'children'} if getattr(token, 'children', None) is not None else set())))
@icontract.ensure(lambda result, token: all(((attr in vars(token) and result.get(attr) == getattr(token, attr)) or (attr not in vars(token) and attr not in result)) for attr in ('content', 'footnotes')))
@icontract.ensure(lambda result, token: all(result[attr] == getattr(token, attr) for attr in token.repr_attributes))
@icontract.ensure(lambda result, token: (('header' in vars(token) and 'header' in result and result['header'] == get_ast(getattr(token, 'header'))) or ('header' not in vars(token) and 'header' not in result)))
@icontract.ensure(lambda result, token: ((getattr(token, 'children', None) is not None and 'children' in result and result['children'] == [get_ast(child) for child in token.children]) or (getattr(token, 'children', None) is None and 'children' not in result)))
```
