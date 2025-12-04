https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/lsusb.py#L365-L383
```
@icontract.snapshot(
    lambda self, bus_idx, output_line: {
        "non_attr": {
            key: {
                k: v
                for k, v in entry.items()
                if k != "_state"
            }
            for item in self.list
            for key, entry in [
                (tuple(item.keys())[0], list(item.values())[0])
            ]
            if isinstance(entry, dict)
            and "_state" in entry
            and entry["_state"]["bus_idx"] == bus_idx
            and not entry["_state"]["attribute_value"]
        },
        "attr": [
            (
                entry["_state"]["last_item"],
                f"{key} {entry.get('value', '')} {entry.get('description', '')}".strip()
            )
            for item in self.list
            for key, entry in [
                (tuple(item.keys())[0], list(item.values())[0])
            ]
            if isinstance(entry, dict)
            and "_state" in entry
            and entry["_state"]["bus_idx"] == bus_idx
            and entry["_state"]["attribute_value"]
        ]
    },
    name="entries_for_bus"
)
@icontract.ensure(
    lambda self, bus_idx, output_line, result, OLD:
    all(
        key in output_line[self.name]
        and isinstance(output_line[self.name][key], dict)
        and "_state" not in output_line[self.name][key]
        and all(
            k in output_line[self.name][key]
            and output_line[self.name][key][k] == v
            for k, v in expected_entry.items()
        )
        for key, expected_entry in OLD.entries_for_bus["non_attr"].items()
    )
)
@icontract.ensure(
    lambda self, bus_idx, output_line, result, OLD:
    all(
        last_item in output_line[self.name]
        and isinstance(output_line[self.name][last_item], dict)
        and (
            all(
                attr_str in output_line[self.name][last_item].get("attributes", [])
                for attr_str in [
                    attr_str2
                    for li2, attr_str2 in OLD.entries_for_bus["attr"]
                    if li2 == last_item
                ]
            )
            and all(
                output_line[self.name][last_item].get("attributes", []).index(exps_i)
                < output_line[self.name][last_item].get("attributes", []).index(exps_j)
                for idx_i, exps_i in enumerate(
                    [
                        attr_str2
                        for li2, attr_str2 in OLD.entries_for_bus["attr"]
                        if li2 == last_item
                    ]
                )
                for idx_j, exps_j in enumerate(
                    [
                        attr_str2
                        for li2, attr_str2 in OLD.entries_for_bus["attr"]
                        if li2 == last_item
                    ]
                )
                if idx_i < idx_j and exps_i != exps_j
            )
        )
        for last_item in {li for (li, _) in OLD.entries_for_bus["attr"]}
    )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
===== 0 =====
```
     def _update_output(self, bus_idx, output_line):
         """modifies output_line dictionary for the corresponding bus index.
         output_line is the self.output_line attribute from the _lsusb object."""
-        for item in self.list:
+        for item in self.list[1:]:  # Skipping the first item in the list, potentially missing important data.
             keyname = tuple(item.keys())[0]
 
             if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list[1:]:  # Skipping the first item in the list, potentially missing important data.
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 1 =====
```
     def _update_output(self, bus_idx, output_line):
         """modifies output_line dictionary for the corresponding bus index.
         output_line is the self.output_line attribute from the _lsusb object."""
-        for item in self.list:
+        for item in self.list[::-1]:  # Iterating in reverse order, which may not align with expected processing order.
             keyname = tuple(item.keys())[0]
 
             if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list[::-1]:  # Iterating in reverse order, which may not align with expected processing order.
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 2 =====
```
         for item in self.list:
             keyname = tuple(item.keys())[0]
 
-            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
+            if 'XX_stateXX' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                 # is this a top level value or an attribute?
                 if item[keyname]['_state']['attribute_value']:
                     last_item = item[keyname]['_state']['last_item']
@@ -16,4 +16,4 @@                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if 'XX_stateXX' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 3 =====
```
         for item in self.list:
             keyname = tuple(item.keys())[0]
 
-            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
+            if '_STATE' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                 # is this a top level value or an attribute?
                 if item[keyname]['_state']['attribute_value']:
                     last_item = item[keyname]['_state']['last_item']
@@ -16,4 +16,4 @@                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_STATE' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 4 =====
```
         for item in self.list:
             keyname = tuple(item.keys())[0]
 
-            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
+            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] != bus_idx:
                 # is this a top level value or an attribute?
                 if item[keyname]['_state']['attribute_value']:
                     last_item = item[keyname]['_state']['last_item']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] != bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 5 =====
```
         for item in self.list:
             keyname = tuple(item.keys())[0]
 
-            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
+            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] != bus_idx:
                 # is this a top level value or an attribute?
                 if item[keyname]['_state']['attribute_value']:
                     last_item = item[keyname]['_state']['last_item']
@@ -16,4 +16,4 @@                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] != bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 6 =====
```
         for item in self.list:
             keyname = tuple(item.keys())[0]
 
-            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
+            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx + 1:
                 # is this a top level value or an attribute?
                 if item[keyname]['_state']['attribute_value']:
                     last_item = item[keyname]['_state']['last_item']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx + 1:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 7 =====
```
         for item in self.list:
             keyname = tuple(item.keys())[0]
 
-            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
+            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] is None:
                 # is this a top level value or an attribute?
                 if item[keyname]['_state']['attribute_value']:
                     last_item = item[keyname]['_state']['last_item']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] is None:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 8 =====
```
         for item in self.list:
             keyname = tuple(item.keys())[0]
 
-            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
+            if '_state' not in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                 # is this a top level value or an attribute?
                 if item[keyname]['_state']['attribute_value']:
                     last_item = item[keyname]['_state']['last_item']
@@ -16,4 +16,4 @@                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' not in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 9 =====
```
 
             if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                 # is this a top level value or an attribute?
-                if item[keyname]['_state']['attribute_value']:
+                if 'attribute_value' in item[keyname]['_state']:
                     last_item = item[keyname]['_state']['last_item']
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if 'attribute_value' in item[keyname]['_state']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 10 =====
```
 
             if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                 # is this a top level value or an attribute?
-                if item[keyname]['_state']['attribute_value']:
+                if item[keyname]['_state']['attribute_value'] == False:
                     last_item = item[keyname]['_state']['last_item']
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value'] == False:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 11 =====
```
 
             if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                 # is this a top level value or an attribute?
-                if item[keyname]['_state']['attribute_value']:
+                if item[keyname]['_state']['attribute_value'] is not None:
                     last_item = item[keyname]['_state']['last_item']
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value'] is not None:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 12 =====
```
 
             if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                 # is this a top level value or an attribute?
-                if item[keyname]['_state']['attribute_value']:
+                if not item[keyname]['_state']['attribute_value']:
                     last_item = item[keyname]['_state']['last_item']
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if not item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 13 =====
```
             if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                 # is this a top level value or an attribute?
                 if item[keyname]['_state']['attribute_value']:
-                    last_item = item[keyname]['_state']['last_item']
+                    last_item = None
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
@@ -16,4 +16,4 @@                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = None
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 14 =====
```
                 # is this a top level value or an attribute?
                 if item[keyname]['_state']['attribute_value']:
                     last_item = item[keyname]['_state']['last_item']
-                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
+                    if 'ATTRIBUTES' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
                     this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
@@ -16,4 +16,4 @@                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'ATTRIBUTES' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 15 =====
```
                 # is this a top level value or an attribute?
                 if item[keyname]['_state']['attribute_value']:
                     last_item = item[keyname]['_state']['last_item']
-                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
+                    if 'XXattributesXX' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
                     this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
@@ -16,4 +16,4 @@                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'XXattributesXX' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 16 =====
```
                 # is this a top level value or an attribute?
                 if item[keyname]['_state']['attribute_value']:
                     last_item = item[keyname]['_state']['last_item']
-                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
+                    if 'attributes' not in output_line[f'{self.name}']:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
                     this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}']:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 17 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = None
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = None
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 18 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 19 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("")} {item[keyname].get("description", "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 20 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("VALUE", "")} {item[keyname].get("description", "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("VALUE", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 21 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("XXvalueXX", "")} {item[keyname].get("description", "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("XXvalueXX", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 22 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("description", "")} {item[keyname].get("value", "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("description", "")} {item[keyname].get("value", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 23 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 24 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("DESCRIPTION", "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("DESCRIPTION", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 25 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("XXdescriptionXX", "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("XXdescriptionXX", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 26 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "No description available")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "No description available")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 27 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "XXXX")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "XXXX")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 28 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", )}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", )}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 29 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", None)}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", None)}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 30 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get(None, "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get(None, "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 31 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("value", "N/A")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "N/A")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 32 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("value", "XXXX")} {item[keyname].get("description", "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "XXXX")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 33 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("value", )} {item[keyname].get("description", "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", )} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 34 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get("value", None)} {item[keyname].get("description", "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", None)} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 35 =====
```
                     if 'attributes' not in output_line[f'{self.name}'][last_item]:
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
-                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
+                    this_attribute = f'{keyname} {item[keyname].get(None, "")} {item[keyname].get("description", "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get(None, "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 36 =====
```
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
                     this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
-                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
+                    output_line[f'{self.name}'][last_item]['attributes'] = this_attribute
                     continue
 
                 output_line[f'{self.name}'].update(item)
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'] = this_attribute
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 37 =====
```
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
                     this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
-                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
+                    output_line[f'{self.name}'][last_item]['attributes'].append(None)
                     continue
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(None)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 38 =====
```
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
                     this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
-                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
+                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute + " (added)")
                     continue
 
                 output_line[f'{self.name}'].update(item)
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute + " (added)")
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 39 =====
```
                         output_line[f'{self.name}'][last_item]['attributes'] = []
 
                     this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
-                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
+                    output_line[f'{self.name}'][last_item]['attributes'].insert(0, this_attribute)
                     continue
 
                 output_line[f'{self.name}'].update(item)
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].insert(0, this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
===== 40 =====
```
 
                     this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
-                    continue
+                    break
 
                 output_line[f'{self.name}'].update(item)
-                del output_line[f'{self.name}'][keyname]['_state']+                del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    break

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']

```
===== 41 =====
```
                     output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                     continue
 
-                output_line[f'{self.name}'].update(item)
+                output_line[f'{self.name}'] = item  # This will overwrite the entire entry instead of updating it.
                 del output_line[f'{self.name}'][keyname]['_state']
```
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'] = item  # This will overwrite the entire entry instead of updating it.
                del output_line[f'{self.name}'][keyname]['_state']
```
