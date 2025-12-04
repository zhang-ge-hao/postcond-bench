https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/search/ternary_search.py#L14-L42
```
@icontract.ensure(
    lambda result, left, right, key, arr:
        (
            result != -1
            and 0 <= result < len(arr)
            and left <= result < right
            and arr[result] == key
        )
        or (
            result == -1
            and all(
                arr[i] != key
                for i in range(max(left, 0), min(right, len(arr)))
            )
        )
)
```
```
@icontract.snapshot(lambda left: left, name="left0")
@icontract.snapshot(lambda right: right, name="right0")
@icontract.snapshot(lambda key: key, name="key0")
@icontract.snapshot(lambda arr: arr[:], name="arr0")
@icontract.ensure(lambda result, OLD: (result == -1) or (OLD.left0 <= result <= OLD.right0 and OLD.arr0[result] == OLD.key0))
```
[0, 1, 2, 3, 4, 5, 6, 10, 11, 18, 20, 21, 22, 23, 24, 25]
===== 0 =====
```
     If the index is not in the range left..right (ie. left <= index < right) returns -1.
     """
 
-    while right >= left:
+    while left < right - 1:  # This will prematurely exit the loop and miss potential matches
         mid1 = left + (right-left) // 3
         mid2 = right - (right-left) // 3
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while left < right - 1:  # This will prematurely exit the loop and miss potential matches
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1
```
===== 1 =====
```
     If the index is not in the range left..right (ie. left <= index < right) returns -1.
     """
 
-    while right >= left:
+    while left < right:  # This will cause an infinite loop if left is ever equal to right
         mid1 = left + (right-left) // 3
         mid2 = right - (right-left) // 3
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while left < right:  # This will cause an infinite loop if left is ever equal to right
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1
```
===== 2 =====
```
     If the index is not in the range left..right (ie. left <= index < right) returns -1.
     """
 
-    while right >= left:
+    while right > left + 1:  # This will skip checking the last element in some cases
         mid1 = left + (right-left) // 3
         mid2 = right - (right-left) // 3
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right > left + 1:  # This will skip checking the last element in some cases
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1
```
===== 3 =====
```
     If the index is not in the range left..right (ie. left <= index < right) returns -1.
     """
 
-    while right >= left:
+    while right > left:
         mid1 = left + (right-left) // 3
         mid2 = right - (right-left) // 3
 
@@ -26,4 +26,4 @@             right = mid2 - 1
 
     # key not found
-    return -1+    return -1
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right > left:
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1

```
===== 4 =====
```
     If the index is not in the range left..right (ie. left <= index < right) returns -1.
     """
 
-    while right >= left:
+    while right > left:  # This will skip the case when left equals right
         mid1 = left + (right-left) // 3
         mid2 = right - (right-left) // 3
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right > left:  # This will skip the case when left equals right
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1
```
===== 5 =====
```
     """
 
     while right >= left:
-        mid1 = left + (right-left) // 3
+        mid1 = left + (right-left) // 4
         mid2 = right - (right-left) // 3
 
         if key == arr[mid1]:
@@ -26,4 +26,4 @@             right = mid2 - 1
 
     # key not found
-    return -1+    return -1
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right >= left:
        mid1 = left + (right-left) // 4
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1

```
===== 6 =====
```
     """
 
     while right >= left:
-        mid1 = left + (right-left) // 3
+        mid1 = left - (right-left) // 3
         mid2 = right - (right-left) // 3
 
         if key == arr[mid1]:
@@ -26,4 +26,4 @@             right = mid2 - 1
 
     # key not found
-    return -1+    return -1
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right >= left:
        mid1 = left - (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1

```
===== 10 =====
```
         mid1 = left + (right-left) // 3
         mid2 = right - (right-left) // 3
 
-        if key == arr[mid1]:
+        if key < arr[mid1]:
             return mid1
         if key == mid2:
             return mid2
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right >= left:
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key < arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1
```
===== 11 =====
```
         mid1 = left + (right-left) // 3
         mid2 = right - (right-left) // 3
 
-        if key == arr[mid1]:
+        if key == arr[mid2]:
             return mid1
         if key == mid2:
             return mid2
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right >= left:
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid2]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1
```
===== 18 =====
```
 
         if key == arr[mid1]:
             return mid1
-        if key == mid2:
+        if key == arr[mid1] or key == arr[mid2]:  # Incorrect logic, should only check mid2
             return mid2
 
         if key < arr[mid1]:
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right >= left:
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == arr[mid1] or key == arr[mid2]:  # Incorrect logic, should only check mid2
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1
```
===== 20 =====
```
         if key == mid2:
             return mid2
 
-        if key < arr[mid1]:
+        if key < arr[mid2]:  # Incorrectly compares with mid2 instead of mid1
             # key lies between l and mid1
             right = mid1 - 1
         elif key > arr[mid2]:
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right >= left:
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid2]:  # Incorrectly compares with mid2 instead of mid1
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1
```
===== 21 =====
```
         if key == mid2:
             return mid2
 
-        if key < arr[mid1]:
+        if key > arr[mid1]:  # Incorrectly checks for greater than instead of less than
             # key lies between l and mid1
             right = mid1 - 1
         elif key > arr[mid2]:
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right >= left:
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key > arr[mid1]:  # Incorrectly checks for greater than instead of less than
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1
```
===== 22 =====
```
             left = mid2 + 1
         else:
             # key lies between mid1 and mid2
-            left = mid1 + 1
+            left = mid1 + 2
             right = mid2 - 1
 
     # key not found
-    return -1+    return -1
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right >= left:
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 2
            right = mid2 - 1

    # key not found
    return -1

```
===== 23 =====
```
             left = mid2 + 1
         else:
             # key lies between mid1 and mid2
-            left = mid1 + 1
+            left = mid1 - 1
             right = mid2 - 1
 
     # key not found
-    return -1+    return -1
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right >= left:
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 - 1
            right = mid2 - 1

    # key not found
    return -1

```
===== 24 =====
```
         else:
             # key lies between mid1 and mid2
             left = mid1 + 1
-            right = mid2 - 1
+            right = mid2 + 1
 
     # key not found
-    return -1+    return -1
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right >= left:
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 + 1

    # key not found
    return -1

```
===== 25 =====
```
         else:
             # key lies between mid1 and mid2
             left = mid1 + 1
-            right = mid2 - 1
+            right = mid2 - 2
 
     # key not found
-    return -1+    return -1
```
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right >= left:
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 2

    # key not found
    return -1

```
