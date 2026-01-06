https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/cli.py#L132-L177
```
@icontract.snapshot(lambda self: dict(self.custom_colors), name="old_colors")
@icontract.ensure(lambda self, OLD: (not PYGMENTS_INSTALLED) or (PYGMENTS_INSTALLED and len(self.custom_colors) == 4 and Name.Tag in self.custom_colors and Keyword in self.custom_colors and Number in self.custom_colors and String in self.custom_colors))
@icontract.ensure(lambda self, OLD: (not PYGMENTS_INSTALLED) or (self.custom_colors[Name.Tag] == ('bold ' + ((lambda env: (lambda lst: (['default'] * 4 if ((len(lst) != 4) or any((c != 'default') and (c not in PYGMENT_COLOR) for c in lst)) else lst))(env.split(',') if env is not None else ['default'] * 4))(os.getenv('JC_COLORS'))[0] != 'default' and PYGMENT_COLOR[(lambda env: (lambda lst: (['default'] * 4 if ((len(lst) != 4) or any((c != 'default') and (c not in PYGMENT_COLOR) for c in lst)) else lst))(env.split(',') if env is not None else ['default'] * 4))(os.getenv('JC_COLORS'))[0]] or PYGMENT_COLOR['blue']))))
@icontract.ensure(lambda self, OLD: (not PYGMENTS_INSTALLED) or (self.custom_colors[Keyword] == ((lambda env: (lambda lst: (['default'] * 4 if ((len(lst) != 4) or any((c != 'default') and (c not in PYGMENT_COLOR) for c in lst)) else lst))(env.split(',') if env is not None else ['default'] * 4))(os.getenv('JC_COLORS'))[1] != 'default' and PYGMENT_COLOR[(lambda env: (lambda lst: (['default'] * 4 if ((len(lst) != 4) or any((c != 'default') and (c not in PYGMENT_COLOR) for c in lst)) else lst))(env.split(',') if env is not None else ['default'] * 4))(os.getenv('JC_COLORS'))[1]] or PYGMENT_COLOR['brightblack']))
@icontract.ensure(lambda self, OLD: (not PYGMENTS_INSTALLED) or (self.custom_colors[Number] == ((lambda env: (lambda lst: (['default'] * 4 if ((len(lst) != 4) or any((c != 'default') and (c not in PYGMENT_COLOR) for c in lst)) else lst))(env.split(',') if env is not None else ['default'] * 4))(os.getenv('JC_COLORS'))[2] != 'default' and PYGMENT_COLOR[(lambda env: (lambda lst: (['default'] * 4 if ((len(lst) != 4) or any((c != 'default') and (c not in PYGMENT_COLOR) for c in lst)) else lst))(env.split(',') if env is not None else ['default'] * 4))(os.getenv('JC_COLORS'))[2]] or PYGMENT_COLOR['magenta']))
@icontract.ensure(lambda self, OLD: (not PYGMENTS_INSTALLED) or (self.custom_colors[String] == ((lambda env: (lambda lst: (['default'] * 4 if ((len(lst) != 4) or any((c != 'default') and (c not in PYGMENT_COLOR) for c in lst)) else lst))(env.split(',') if env is not None else ['default'] * 4))(os.getenv('JC_COLORS'))[3] != 'default' and PYGMENT_COLOR[(lambda env: (lambda lst: (['default'] * 4 if ((len(lst) != 4) or any((c != 'default') and (c not in PYGMENT_COLOR) for c in lst)) else lst))(env.split(',') if env is not None else ['default'] * 4))(os.getenv('JC_COLORS'))[3]] or PYGMENT_COLOR['green']))
@icontract.ensure(lambda self, OLD: (PYGMENTS_INSTALLED) or (self.custom_colors == OLD.old_colors))
```
```
Syntax error.

SyntaxError: '(' was never closed
```
syntax_error
```
@icontract.snapshot(lambda self: os.getenv('JC_COLORS'), name='env')
@icontract.snapshot(lambda self: getattr(self, 'custom_colors', None), name='old_custom_colors')
@icontract.snapshot(lambda self: dict(PYGMENT_COLOR) if PYGMENTS_INSTALLED else None, name='pc')
@icontract.ensure(lambda self, OLD: (
    (not PYGMENTS_INSTALLED and self.custom_colors == OLD.old_custom_colors)
    or
    (
        PYGMENTS_INSTALLED
        and isinstance(self.custom_colors, dict)
        and set(self.custom_colors.keys()) == {Name.Tag, Keyword, Number, String}
        and (lambda defaults, env, pc: (
            (lambda lst:
                (lambda valid, final:
                    final and
                    self.custom_colors[Name.Tag] == ('bold ' + pc[final[0]] if final[0] != 'default' else 'bold ' + pc['blue'])
                    and self.custom_colors[Keyword] == (pc[final[1]] if final[1] != 'default' else pc['brightblack'])
                    and self.custom_colors[Number] == (pc[final[2]] if final[2] != 'default' else pc['magenta'])
                    and self.custom_colors[String] == (pc[final[3]] if final[3] != 'default' else pc['green'])
                )(
                    (len(lst) == 4 and all((c == 'default' or c in pc) for c in lst)),
                    (lst if (len(lst) == 4 and all((c == 'default' or c in pc) for c in lst)) else defaults)
                )
            )((env.split(',') if env else defaults))
        ))(
            ['default', 'default', 'default', 'default'],
            OLD.env,
            OLD.pc or {}
        )
    )
))
```
