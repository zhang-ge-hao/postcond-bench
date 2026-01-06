https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/cli.py#L132-L177
```
@icontract.ensure(lambda self: not PYGMENTS_INSTALLED or len(self.custom_colors) == 4)
@icontract.ensure(lambda self: not PYGMENTS_INSTALLED or Name.Tag in self.custom_colors)
@icontract.ensure(lambda self: not PYGMENTS_INSTALLED or Keyword in self.custom_colors)
@icontract.ensure(lambda self: not PYGMENTS_INSTALLED or Number in self.custom_colors)
@icontract.ensure(lambda self: not PYGMENTS_INSTALLED or String in self.custom_colors)
@icontract.ensure(lambda self: not PYGMENTS_INSTALLED or all(isinstance(v, str) for v in self.custom_colors.values()))
```
```
missing attribute validation

self.custom_colors
```
passed
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
===== 5: failed =====
```
         """
         if PYGMENTS_INSTALLED:
             input_error = False
-            env_colors = os.getenv('JC_COLORS')
+            env_colors = os.getenv('XXJC_COLORSXX')
 
             if env_colors:
                 color_list = env_colors.split(',')
@@ -43,4 +43,4 @@                 Keyword: PYGMENT_COLOR[color_list[1]] if color_list[1] != 'default' else PYGMENT_COLOR['brightblack'],                 # true, false, null
                 Number: PYGMENT_COLOR[color_list[2]] if color_list[2] != 'default' else PYGMENT_COLOR['magenta'],                      # numbers
                 String: PYGMENT_COLOR[color_list[3]] if color_list[3] != 'default' else PYGMENT_COLOR['green']                         # strings
-            }+            }
```
```
    def set_custom_colors(self) -> None:
        """
        Sets the custom_colors dictionary to be used in Pygments custom style class.

        Grab custom colors from JC_COLORS environment variable. JC_COLORS env
        variable takes 4 comma separated string values and should be in the
        format of:

        JC_COLORS=<keyname_color>,<keyword_color>,<number_color>,<string_color>

        Where colors are: black, red, green, yellow, blue, magenta, cyan, gray,
        brightblack, brightred, brightgreen, brightyellow, brightblue, brightmagenta,
        brightcyan, white, default

        Default colors:
        JC_COLORS=blue,brightblack,magenta,green
        JC_COLORS=default,default,default,default
        """
        if PYGMENTS_INSTALLED:
            input_error = False
            env_colors = os.getenv('XXJC_COLORSXX')

            if env_colors:
                color_list = env_colors.split(',')
            else:
                color_list = ['default', 'default', 'default', 'default']

            if len(color_list) != 4:
                input_error = True

            for color in color_list:
                if color != 'default' and color not in PYGMENT_COLOR:
                    input_error = True

            # if there is an issue with the env variable, just set all colors to default and move on
            if input_error:
                utils.warning_message(['Could not parse JC_COLORS environment variable'])
                color_list = ['default', 'default', 'default', 'default']

            # Try the color set in the JC_COLORS env variable first. If it is set to default, then fall back to default colors
            self.custom_colors = {
                Name.Tag: f'bold {PYGMENT_COLOR[color_list[0]]}' if color_list[0] != 'default' else f"bold {PYGMENT_COLOR['blue']}",   # key names
                Keyword: PYGMENT_COLOR[color_list[1]] if color_list[1] != 'default' else PYGMENT_COLOR['brightblack'],                 # true, false, null
                Number: PYGMENT_COLOR[color_list[2]] if color_list[2] != 'default' else PYGMENT_COLOR['magenta'],                      # numbers
                String: PYGMENT_COLOR[color_list[3]] if color_list[3] != 'default' else PYGMENT_COLOR['green']                         # strings
            }

```
