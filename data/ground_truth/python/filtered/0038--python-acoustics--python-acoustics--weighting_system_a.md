https://github.com/python-acoustics/python-acoustics/blob/99d79206159b822ea2f4e9d27c8b2fbfeb704d38/./acoustics/standards/iec_61672_1_2013.py#L314-L333
```
🈚️

E   ModuleNotFoundError: No module named 'icontract'

@icontract.ensure(
    lambda result:
        # result 是 (num, den)
        np.allclose(
            result[0],
            np.array([
                (2.0 * np.pi * _POLE_FREQUENCIES[4]) ** 2.0
                * (10 ** (-_NORMALIZATION_CONSTANTS['A'] / 20.0)),
                0.0,
                0.0,
                0.0,
                0.0,
            ])
        )
        and np.allclose(
            result[1],
            np.convolve(
                np.convolve(
                    np.convolve(
                        [1.0,
                         4.0 * np.pi * _POLE_FREQUENCIES[4],
                         (2.0 * np.pi * _POLE_FREQUENCIES[4]) ** 2.0],
                        [1.0,
                         4.0 * np.pi * _POLE_FREQUENCIES[1],
                         (2.0 * np.pi * _POLE_FREQUENCIES[1]) ** 2.0],
                    ),
                    [1.0, 2.0 * np.pi * _POLE_FREQUENCIES[3]],
                ),
                [1.0, 2.0 * np.pi * _POLE_FREQUENCIES[2]],
            )
        )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]
===== 0 =====
```
     See equation E.6 of the standard.
 
     """
-    f1 = _POLE_FREQUENCIES[1]
+    f1 = _POLE_FREQUENCIES[2]
     f2 = _POLE_FREQUENCIES[2]
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
@@ -17,4 +17,4 @@     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[2]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 1 =====
```
 
     """
     f1 = _POLE_FREQUENCIES[1]
-    f2 = _POLE_FREQUENCIES[2]
+    f2 = _POLE_FREQUENCIES[3]
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
@@ -17,4 +17,4 @@     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[3]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 2 =====
```
     """
     f1 = _POLE_FREQUENCIES[1]
     f2 = _POLE_FREQUENCIES[2]
-    f3 = _POLE_FREQUENCIES[3]
+    f3 = _POLE_FREQUENCIES[4]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
@@ -17,4 +17,4 @@     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[4]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 3 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = None
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = None
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 4 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array(None)
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array(None)
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 5 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array([(2.0 * np.pi * f4) * 2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4) * 2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 6 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10 * (-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10 * (-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 7 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(+offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(+offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 8 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset * 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset * 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 9 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator
```
===== 10 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator
```
===== 11 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (11**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (11**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 12 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array([(2.0 * np.pi * f4)**2.0 / (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 / (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 13 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array([(2.0 * np.pi * f4)**3.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**3.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 14 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array([(2.0 * np.pi / f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi / f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 15 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array([(2.0 / np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 / np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 16 =====
```
     f3 = _POLE_FREQUENCIES[3]
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
-    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
+    numerator = np.array([(3.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(3.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 17 =====
```
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
-    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
+    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4) * 2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4) * 2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 18 =====
```
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
-    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
+    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**3.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**3.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 19 =====
```
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
-    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
+    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi / f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi / f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 20 =====
```
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
-    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
+    part1 = [1.0, 4.0 * np.pi * f4, (2.0 / np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 / np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 21 =====
```
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
-    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
+    part1 = [1.0, 4.0 * np.pi * f4, (3.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (3.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 22 =====
```
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
-    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
+    part1 = [1.0, 4.0 * np.pi / f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi / f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 23 =====
```
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
-    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
+    part1 = [1.0, 4.0 / np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 / np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 24 =====
```
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
-    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
+    part1 = [1.0, 5.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 5.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 25 =====
```
     f4 = _POLE_FREQUENCIES[4]
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
-    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
+    part1 = [2.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [2.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 26 =====
```
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
-    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
+    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1) * 2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1) * 2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 27 =====
```
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
-    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
+    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**3.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**3.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 28 =====
```
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
-    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
+    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi / f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi / f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 29 =====
```
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
-    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
+    part2 = [1.0, 4.0 * np.pi * f1, (2.0 / np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 / np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 30 =====
```
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
-    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
+    part2 = [1.0, 4.0 * np.pi * f1, (3.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (3.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 31 =====
```
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
-    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
+    part2 = [1.0, 4.0 * np.pi / f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi / f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 32 =====
```
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
-    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
+    part2 = [1.0, 4.0 / np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 / np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 33 =====
```
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
-    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
+    part2 = [1.0, 5.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 5.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 34 =====
```
     offset = _NORMALIZATION_CONSTANTS['A']
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
-    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
+    part2 = [2.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [2.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 35 =====
```
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
-    part3 = [1.0, 2.0 * np.pi * f3]
+    part3 = [1.0, 2.0 * np.pi / f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi / f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 36 =====
```
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
-    part3 = [1.0, 2.0 * np.pi * f3]
+    part3 = [1.0, 2.0 / np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 / np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 37 =====
```
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
-    part3 = [1.0, 2.0 * np.pi * f3]
+    part3 = [1.0, 3.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 3.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 38 =====
```
     numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
-    part3 = [1.0, 2.0 * np.pi * f3]
+    part3 = [2.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [2.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 39 =====
```
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
-    part4 = [1.0, 2.0 * np.pi * f2]
+    part4 = [1.0, 2.0 * np.pi / f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi / f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 40 =====
```
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
-    part4 = [1.0, 2.0 * np.pi * f2]
+    part4 = [1.0, 2.0 / np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 / np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 41 =====
```
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
-    part4 = [1.0, 2.0 * np.pi * f2]
+    part4 = [1.0, 3.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 3.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 42 =====
```
     part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
-    part4 = [1.0, 2.0 * np.pi * f2]
+    part4 = [2.0, 2.0 * np.pi * f2]
     denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [2.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
    return numerator, denomenator

```
===== 43 =====
```
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
-    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
-    return numerator, denomenator+    denomenator = None
+    return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = None
    return numerator, denomenator

```
===== 44 =====
```
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
-    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
+    denomenator = np.convolve(np.convolve(part1, part2), part1)  # Incorrectly using part1 twice instead of part3 and part4
     return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(part1, part2), part1)  # Incorrectly using part1 twice instead of part3 and part4
    return numerator, denomenator
```
===== 45 =====
```
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
-    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
+    denomenator = np.convolve(np.convolve(part1, part2), part3)  # Missing convolution with part4
     return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(np.convolve(part1, part2), part3)  # Missing convolution with part4
    return numerator, denomenator
```
===== 46 =====
```
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
-    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
+    denomenator = np.convolve(part1, part2)  # Missing convolution with part3 and part4
     return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(part1, part2)  # Missing convolution with part3 and part4
    return numerator, denomenator
```
===== 47 =====
```
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
-    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
+    denomenator = np.convolve(part1, part3)  # Incorrectly using part1 and part3 only
     return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(part1, part3)  # Incorrectly using part1 and part3 only
    return numerator, denomenator
```
===== 48 =====
```
     part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
     part3 = [1.0, 2.0 * np.pi * f3]
     part4 = [1.0, 2.0 * np.pi * f2]
-    denomenator = np.convolve(np.convolve(np.convolve(part1, part2), part3), part4)
+    denomenator = np.convolve(part2, part4)  # Incorrectly using part2 and part4 only
     return numerator, denomenator
```
```
def weighting_system_a():
    """A-weighting filter represented as polynomial transfer function.

    :returns: Tuple of `num` and `den`.

    See equation E.6 of the standard.

    """
    f1 = _POLE_FREQUENCIES[1]
    f2 = _POLE_FREQUENCIES[2]
    f3 = _POLE_FREQUENCIES[3]
    f4 = _POLE_FREQUENCIES[4]
    offset = _NORMALIZATION_CONSTANTS['A']
    numerator = np.array([(2.0 * np.pi * f4)**2.0 * (10**(-offset / 20.0)), 0.0, 0.0, 0.0, 0.0])
    part1 = [1.0, 4.0 * np.pi * f4, (2.0 * np.pi * f4)**2.0]
    part2 = [1.0, 4.0 * np.pi * f1, (2.0 * np.pi * f1)**2.0]
    part3 = [1.0, 2.0 * np.pi * f3]
    part4 = [1.0, 2.0 * np.pi * f2]
    denomenator = np.convolve(part2, part4)  # Incorrectly using part2 and part4 only
    return numerator, denomenator
```
