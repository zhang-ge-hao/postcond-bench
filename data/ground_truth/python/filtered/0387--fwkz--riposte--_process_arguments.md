https://github.com/fwkz/riposte/blob/174bded8ccd665556b163e5c5633d0900715740f/./riposte/command.py#L49-L65
```
🈚️

rely on function object

```
```
None
```
[0, 1, 2, 3, 4, 5]
===== 0 =====
```
 
         """
         processed = []
-        for arg in args:
+        for arg in args[1:]:
             for guide in self._guides.get(name, []):
                 arg = guide(arg)
             processed.append(arg)
```
```
    def _process_arguments(self, name: str, *args) -> List:
        """Process each argument according to selected chain of guides

        Process each argument according to selected chain of guides. Each
        guide from the collection is applied to the every argument.
        Guide as input uses output from previous guide e.g.

            guide_3(guide_2(guide_1("scoo")))

        """
        processed = []
        for arg in args[1:]:
            for guide in self._guides.get(name, []):
                arg = guide(arg)
            processed.append(arg)

        return processed
```
===== 1 =====
```
 
         """
         processed = []
-        for arg in args:
+        for arg in processed:
             for guide in self._guides.get(name, []):
                 arg = guide(arg)
             processed.append(arg)
```
```
    def _process_arguments(self, name: str, *args) -> List:
        """Process each argument according to selected chain of guides

        Process each argument according to selected chain of guides. Each
        guide from the collection is applied to the every argument.
        Guide as input uses output from previous guide e.g.

            guide_3(guide_2(guide_1("scoo")))

        """
        processed = []
        for arg in processed:
            for guide in self._guides.get(name, []):
                arg = guide(arg)
            processed.append(arg)

        return processed
```
===== 2 =====
```
         """
         processed = []
         for arg in args:
-            for guide in self._guides.get(name, []):
+            for guide in self._guides.get(None, []):
                 arg = guide(arg)
             processed.append(arg)
 
-        return processed+        return processed
```
```
    def _process_arguments(self, name: str, *args) -> List:
        """Process each argument according to selected chain of guides

        Process each argument according to selected chain of guides. Each
        guide from the collection is applied to the every argument.
        Guide as input uses output from previous guide e.g.

            guide_3(guide_2(guide_1("scoo")))

        """
        processed = []
        for arg in args:
            for guide in self._guides.get(None, []):
                arg = guide(arg)
            processed.append(arg)

        return processed

```
===== 3 =====
```
         processed = []
         for arg in args:
             for guide in self._guides.get(name, []):
-                arg = guide(arg)
+                arg = None
             processed.append(arg)
 
-        return processed+        return processed
```
```
    def _process_arguments(self, name: str, *args) -> List:
        """Process each argument according to selected chain of guides

        Process each argument according to selected chain of guides. Each
        guide from the collection is applied to the every argument.
        Guide as input uses output from previous guide e.g.

            guide_3(guide_2(guide_1("scoo")))

        """
        processed = []
        for arg in args:
            for guide in self._guides.get(name, []):
                arg = None
            processed.append(arg)

        return processed

```
===== 4 =====
```
         for arg in args:
             for guide in self._guides.get(name, []):
                 arg = guide(arg)
-            processed.append(arg)
+            processed.append(None)
 
-        return processed+        return processed
```
```
    def _process_arguments(self, name: str, *args) -> List:
        """Process each argument according to selected chain of guides

        Process each argument according to selected chain of guides. Each
        guide from the collection is applied to the every argument.
        Guide as input uses output from previous guide e.g.

            guide_3(guide_2(guide_1("scoo")))

        """
        processed = []
        for arg in args:
            for guide in self._guides.get(name, []):
                arg = guide(arg)
            processed.append(None)

        return processed

```
===== 5 =====
```
         for arg in args:
             for guide in self._guides.get(name, []):
                 arg = guide(arg)
-            processed.append(arg)
+            processed.append(arg) if isinstance(arg, str) else processed.append("")  # Appends empty string for non-string inputs
 
         return processed
```
```
    def _process_arguments(self, name: str, *args) -> List:
        """Process each argument according to selected chain of guides

        Process each argument according to selected chain of guides. Each
        guide from the collection is applied to the every argument.
        Guide as input uses output from previous guide e.g.

            guide_3(guide_2(guide_1("scoo")))

        """
        processed = []
        for arg in args:
            for guide in self._guides.get(name, []):
                arg = guide(arg)
            processed.append(arg) if isinstance(arg, str) else processed.append("")  # Appends empty string for non-string inputs

        return processed
```
