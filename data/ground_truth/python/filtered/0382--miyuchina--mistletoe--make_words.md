https://github.com/miyuchina/mistletoe/blob/0860a8662d386b0b9bee2512e8a078715703f980/./mistletoe/markdown_renderer.py#L462-L488
```
🈚️

yield
```
```
@icontract.ensure(lambda result, cls, fragments: 'word = ""' in __import__('inspect').getsource(cls.make_words))
@icontract.ensure(lambda result, cls, fragments: 'getattr(fragment, "wordwrap", False)' in __import__('inspect').getsource(cls.make_words))
@icontract.ensure(lambda result, cls, fragments: 'cls._whitespace.split(fragment.text)' in __import__('inspect').getsource(cls.make_words))
@icontract.ensure(lambda result, cls, fragments: 'getattr(fragment, "hard_line_break", False)' in __import__('inspect').getsource(cls.make_words))
@icontract.ensure(lambda result, cls, fragments: 'yield from (word + fragment.text[:-1], "\\n")' in __import__('inspect').getsource(cls.make_words))
@icontract.ensure(lambda result, cls, fragments: ('if word:' in __import__('inspect').getsource(cls.make_words)) and ('yield word' in __import__('inspect').getsource(cls.make_words)) )
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 34, 35, 36, 37, 38]
===== 0 =====
```
         which do not contain breakable spaces or line breaks. The exception is
         hard line breaks, which are represented by the string `\n`.
         """
-        word = ""
+        word = "XXXX"
         for fragment in fragments:
             if getattr(fragment, "wordwrap", False):
                 first = True
@@ -24,4 +24,4 @@                 word += fragment.text
 
         if word:
-            yield word+            yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = "XXXX"
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word

```
===== 1 =====
```
         hard line breaks, which are represented by the string `\n`.
         """
         word = ""
-        for fragment in fragments:
+        for fragment in []:  # This line iterates over an empty list, resulting in no processing of fragments.
             if getattr(fragment, "wordwrap", False):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in []:  # This line iterates over an empty list, resulting in no processing of fragments.
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 2 =====
```
         """
         word = ""
         for fragment in fragments:
-            if getattr(fragment, "wordwrap", False):
+            if getattr(None, "wordwrap", False):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
                     if first:
@@ -24,4 +24,4 @@                 word += fragment.text
 
         if word:
-            yield word+            yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(None, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word

```
===== 3 =====
```
         """
         word = ""
         for fragment in fragments:
-            if getattr(fragment, "wordwrap", False):
+            if getattr(fragment, "WORDWRAP", False):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
                     if first:
@@ -24,4 +24,4 @@                 word += fragment.text
 
         if word:
-            yield word+            yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "WORDWRAP", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word

```
===== 4 =====
```
         """
         word = ""
         for fragment in fragments:
-            if getattr(fragment, "wordwrap", False):
+            if getattr(fragment, "XXwordwrapXX", False):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
                     if first:
@@ -24,4 +24,4 @@                 word += fragment.text
 
         if word:
-            yield word+            yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "XXwordwrapXX", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word

```
===== 5 =====
```
         """
         word = ""
         for fragment in fragments:
-            if getattr(fragment, "wordwrap", False):
+            if getattr(fragment, "hard_line_break", False):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
                     if first:
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "hard_line_break", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 6 =====
```
         """
         word = ""
         for fragment in fragments:
-            if getattr(fragment, "wordwrap", False):
+            if getattr(fragment, "wordwrap", True) and fragment.text.startswith(" "):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
                     if first:
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", True) and fragment.text.startswith(" "):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 7 =====
```
         """
         word = ""
         for fragment in fragments:
-            if getattr(fragment, "wordwrap", False):
+            if getattr(fragment, "wordwrap", True) and fragment.text.strip() == "":
                 first = True
                 for item in cls._whitespace.split(fragment.text):
                     if first:
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", True) and fragment.text.strip() == "":
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 8 =====
```
         """
         word = ""
         for fragment in fragments:
-            if getattr(fragment, "wordwrap", False):
+            if getattr(fragment, "wordwrap", True):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
                     if first:
@@ -24,4 +24,4 @@                 word += fragment.text
 
         if word:
-            yield word+            yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", True):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word

```
===== 9 =====
```
         """
         word = ""
         for fragment in fragments:
-            if getattr(fragment, "wordwrap", False):
+            if not getattr(fragment, "wordwrap", False) and fragment.text:
                 first = True
                 for item in cls._whitespace.split(fragment.text):
                     if first:
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if not getattr(fragment, "wordwrap", False) and fragment.text:
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 10 =====
```
         """
         word = ""
         for fragment in fragments:
-            if getattr(fragment, "wordwrap", False):
+            if not getattr(fragment, "wordwrap", True):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
                     if first:
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if not getattr(fragment, "wordwrap", True):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 11 =====
```
         word = ""
         for fragment in fragments:
             if getattr(fragment, "wordwrap", False):
-                first = True
+                first = False
                 for item in cls._whitespace.split(fragment.text):
                     if first:
                         word += item
@@ -24,4 +24,4 @@                 word += fragment.text
 
         if word:
-            yield word+            yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = False
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word

```
===== 12 =====
```
         word = ""
         for fragment in fragments:
             if getattr(fragment, "wordwrap", False):
-                first = True
+                first = None
                 for item in cls._whitespace.split(fragment.text):
                     if first:
                         word += item
@@ -24,4 +24,4 @@                 word += fragment.text
 
         if word:
-            yield word+            yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = None
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word

```
===== 13 =====
```
         for fragment in fragments:
             if getattr(fragment, "wordwrap", False):
                 first = True
-                for item in cls._whitespace.split(fragment.text):
+                for item in cls._whitespace.findall(fragment.text):  # Uses findall instead of split, which may not yield expected results
                     if first:
                         word += item
                         first = False
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.findall(fragment.text):  # Uses findall instead of split, which may not yield expected results
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 14 =====
```
         for fragment in fragments:
             if getattr(fragment, "wordwrap", False):
                 first = True
-                for item in cls._whitespace.split(fragment.text):
+                for item in cls._whitespace.split(fragment.text.strip()):  # Strips whitespace before splitting, potentially losing important spaces
                     if first:
                         word += item
                         first = False
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text.strip()):  # Strips whitespace before splitting, potentially losing important spaces
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 15 =====
```
         for fragment in fragments:
             if getattr(fragment, "wordwrap", False):
                 first = True
-                for item in cls._whitespace.split(fragment.text):
+                for item in fragment.text.split(" "):  # Splits only by spaces, ignoring other whitespace
                     if first:
                         word += item
                         first = False
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in fragment.text.split(" "):  # Splits only by spaces, ignoring other whitespace
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 16 =====
```
         for fragment in fragments:
             if getattr(fragment, "wordwrap", False):
                 first = True
-                for item in cls._whitespace.split(fragment.text):
+                for item in fragment.text.split():  # Splits by any whitespace but does not preserve the original whitespace structure
                     if first:
                         word += item
                         first = False
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in fragment.text.split():  # Splits by any whitespace but does not preserve the original whitespace structure
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 17 =====
```
         for fragment in fragments:
             if getattr(fragment, "wordwrap", False):
                 first = True
-                for item in cls._whitespace.split(fragment.text):
+                for item in fragment.text.splitlines():  # Splits by lines instead of whitespace, leading to incorrect word handling
                     if first:
                         word += item
                         first = False
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in fragment.text.splitlines():  # Splits by lines instead of whitespace, leading to incorrect word handling
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 18 =====
```
             if getattr(fragment, "wordwrap", False):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
-                    if first:
+                    if first and word != "":
                         word += item
                         first = False
                     else:
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first and word != "":
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 19 =====
```
             if getattr(fragment, "wordwrap", False):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
-                    if first:
+                    if item == "":
                         word += item
                         first = False
                     else:
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if item == "":
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 20 =====
```
             if getattr(fragment, "wordwrap", False):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
-                    if first:
+                    if len(item) > 0:
                         word += item
                         first = False
                     else:
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if len(item) > 0:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 21 =====
```
             if getattr(fragment, "wordwrap", False):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
-                    if first:
+                    if not first:
                         word += item
                         first = False
                     else:
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if not first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 22 =====
```
             if getattr(fragment, "wordwrap", False):
                 first = True
                 for item in cls._whitespace.split(fragment.text):
-                    if first:
+                    if word == "":
                         word += item
                         first = False
                     else:
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if word == "":
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 23 =====
```
                 first = True
                 for item in cls._whitespace.split(fragment.text):
                     if first:
-                        word += item
+                        word = item
                         first = False
                     else:
                         if word:
@@ -24,4 +24,4 @@                 word += fragment.text
 
         if word:
-            yield word+            yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word = item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word

```
===== 24 =====
```
                 for item in cls._whitespace.split(fragment.text):
                     if first:
                         word += item
-                        first = False
+                        first = True
                     else:
                         if word:
                             yield word
@@ -24,4 +24,4 @@                 word += fragment.text
 
         if word:
-            yield word+            yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = True
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word

```
===== 25 =====
```
                         word += item
                         first = False
                     else:
-                        if word:
+                        if not word:
                             yield word
                         word = item
             elif getattr(fragment, "hard_line_break", False):
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if not word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 26 =====
```
                         word += item
                         first = False
                     else:
-                        if word:
+                        if word == "":
                             yield word
                         word = item
             elif getattr(fragment, "hard_line_break", False):
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word == "":
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 27 =====
```
                         word += item
                         first = False
                     else:
-                        if word:
+                        if word is None:
                             yield word
                         word = item
             elif getattr(fragment, "hard_line_break", False):
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word is None:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 28 =====
```
                         word += item
                         first = False
                     else:
-                        if word:
+                        if word.strip() == "":
                             yield word
                         word = item
             elif getattr(fragment, "hard_line_break", False):
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word.strip() == "":
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 29 =====
```
                         if word:
                             yield word
                         word = item
-            elif getattr(fragment, "hard_line_break", False):
+            elif getattr(fragment, "hard_line_break", True):
                 yield from (word + fragment.text[:-1], "\n")
                 word = ""
             else:
                 word += fragment.text
 
         if word:
-            yield word+            yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", True):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word

```
===== 30 =====
```
                         if word:
                             yield word
                         word = item
-            elif getattr(fragment, "hard_line_break", False):
+            elif getattr(fragment, "wordwrap", True):
                 yield from (word + fragment.text[:-1], "\n")
                 word = ""
             else:
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "wordwrap", True):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word:
            yield word
```
===== 34 =====
```
                         word = item
             elif getattr(fragment, "hard_line_break", False):
                 yield from (word + fragment.text[:-1], "\n")
-                word = ""
+                word = "XXXX"
             else:
                 word += fragment.text
 
         if word:
-            yield word+            yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = "XXXX"
            else:
                word += fragment.text

        if word:
            yield word

```
===== 35 =====
```
                 yield from (word + fragment.text[:-1], "\n")
                 word = ""
             else:
-                word += fragment.text
+                word = fragment.text
 
         if word:
-            yield word+            yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word = fragment.text

        if word:
            yield word

```
===== 36 =====
```
             else:
                 word += fragment.text
 
-        if word:
+        if not word:  # This will skip yielding when word is empty, leading to missing output.
             yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if not word:  # This will skip yielding when word is empty, leading to missing output.
            yield word
```
===== 37 =====
```
             else:
                 word += fragment.text
 
-        if word:
+        if word == "":  # This will only yield if word is an empty string, which is not the intended check.
             yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word == "":  # This will only yield if word is an empty string, which is not the intended check.
            yield word
```
===== 38 =====
```
             else:
                 word += fragment.text
 
-        if word:
+        if word is None:  # This will never be true since 'word' is always a string, causing no output.
             yield word
```
```
    @classmethod
    def make_words(cls, fragments: Iterable[Fragment]) -> Iterable[str]:
        """
        Aggregates and splits a sequence of Fragments into words, i.e., strings
        which do not contain breakable spaces or line breaks. The exception is
        hard line breaks, which are represented by the string `\n`.
        """
        word = ""
        for fragment in fragments:
            if getattr(fragment, "wordwrap", False):
                first = True
                for item in cls._whitespace.split(fragment.text):
                    if first:
                        word += item
                        first = False
                    else:
                        if word:
                            yield word
                        word = item
            elif getattr(fragment, "hard_line_break", False):
                yield from (word + fragment.text[:-1], "\n")
                word = ""
            else:
                word += fragment.text

        if word is None:  # This will never be true since 'word' is always a string, causing no output.
            yield word
```
