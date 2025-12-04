https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/maths/num_perfect_squares.py#L17-L47
```
@icontract.ensure(
    lambda result, number:
        1 <= result <= 4
        and
        result == (
            1
            if (math.isqrt(number) ** 2 == number)
            else (
                4
                if (
                    (lambda n:
                        0
                        if n == 0
                        else n >> (
                            2 * (
                                ((n & -n).bit_length() - 1) // 2
                            )
                        )
                    )(number)
                    % 8 == 7
                )
                else (
                    2
                    if any(
                        (lambda x: math.isqrt(x) ** 2 == x)(number - i * i)
                        for i in range(1, math.isqrt(number) + 1)
                    )
                    else 3
                )
            )
        )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
===== 0 =====
```
     :return: int between 1 - 4
     """
     # If the number is a perfect square then we only need 1 number.
-    if int(math.sqrt(number))**2 == number:
+    if int(math.sqrt(number)) * 2 == number:
         return 1
 
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number)) * 2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 1 =====
```
     :return: int between 1 - 4
     """
     # If the number is a perfect square then we only need 1 number.
-    if int(math.sqrt(number))**2 == number:
+    if int(math.sqrt(number))**2 != number:
         return 1
 
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 != number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 2 =====
```
     :return: int between 1 - 4
     """
     # If the number is a perfect square then we only need 1 number.
-    if int(math.sqrt(number))**2 == number:
+    if int(math.sqrt(number))**2 != number:
         return 1
 
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 != number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 3 =====
```
     :return: int between 1 - 4
     """
     # If the number is a perfect square then we only need 1 number.
-    if int(math.sqrt(number))**2 == number:
+    if int(math.sqrt(number))**3 == number:
         return 1
 
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**3 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 4 =====
```
     :return: int between 1 - 4
     """
     # If the number is a perfect square then we only need 1 number.
-    if int(math.sqrt(number))**2 == number:
+    if number % 2 == 0:
         return 1
 
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if number % 2 == 0:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 5 =====
```
     :return: int between 1 - 4
     """
     # If the number is a perfect square then we only need 1 number.
-    if int(math.sqrt(number))**2 == number:
+    if number < 0:
         return 1
 
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if number < 0:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 6 =====
```
     :return: int between 1 - 4
     """
     # If the number is a perfect square then we only need 1 number.
-    if int(math.sqrt(number))**2 == number:
+    if number < 1:
         return 1
 
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if number < 1:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 7 =====
```
     :return: int between 1 - 4
     """
     # If the number is a perfect square then we only need 1 number.
-    if int(math.sqrt(number))**2 == number:
+    if number == 0:
         return 1
 
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if number == 0:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 8 =====
```
     """
     # If the number is a perfect square then we only need 1 number.
     if int(math.sqrt(number))**2 == number:
-        return 1
+        return 2
 
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
     # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 2

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 9 =====
```
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
     # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
     # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
-    while number > 0 and number % 4 == 0:
+    while number > 0 and number % 4 != 0:
         number /= 4
 
     # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 != 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 10 =====
```
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
     # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
     # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
-    while number > 0 and number % 4 == 0:
+    while number > 0 and number % 4 != 0:
         number /= 4
 
     # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 != 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 11 =====
```
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
     # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
     # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
-    while number > 0 and number % 4 == 0:
+    while number > 0 and number % 4 == 1:
         number /= 4
 
     # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 1:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 12 =====
```
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
     # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
     # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
-    while number > 0 and number % 4 == 0:
+    while number > 0 and number % 4 == 1:
         number /= 4
 
     # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 1:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 13 =====
```
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
     # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
     # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
-    while number > 0 and number % 4 == 0:
+    while number > 0 and number % 4 == 2:
         number /= 4
 
     # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 2:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 14 =====
```
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
     # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
     # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
-    while number > 0 and number % 4 == 0:
+    while number > 0 and number % 4 == 3:
         number /= 4
 
     # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 3:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 15 =====
```
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
     # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
     # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
-    while number > 0 and number % 4 == 0:
+    while number > 0 and number % 5 == 0:
         number /= 4
 
     # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 5 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 16 =====
```
     # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
     # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
     # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
-    while number > 0 and number % 4 == 0:
+    while number > 0 and number / 4 == 0:
         number /= 4
 
     # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number / 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 17 =====
```
     # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
     # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
     while number > 0 and number % 4 == 0:
-        number /= 4
+        number /= 5
 
     # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
     # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 5

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 18 =====
```
     # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
     # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
     # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
-    if number % 8 == 7:
+    if number % 2 == 1:
         return 4
 
     # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 2 == 1:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 19 =====
```
     # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
     # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
     # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
-    if number % 8 == 7:
+    if number % 4 == 0:
         return 4
 
     # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 4 == 0:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 20 =====
```
     # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
     # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
     # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
-    if number % 8 == 7:
+    if number % 8 != 7:
         return 4
 
     # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 != 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 21 =====
```
     # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
     # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
     # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
-    if number % 8 == 7:
+    if number % 8 == 0:
         return 4
 
     # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 0:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 22 =====
```
     # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
     # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
     # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
-    if number % 8 == 7:
+    if number % 8 == 6:
         return 4
 
     # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 6:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 23 =====
```
     # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
     # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
     # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
-    if number % 8 == 7:
+    if number % 8 == 8:
         return 4
 
     # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 8:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 24 =====
```
     # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
     # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
     # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
-    if number % 8 == 7:
+    if number % 9 == 7:
         return 4
 
     # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 9 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 25 =====
```
     # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
     # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
     # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
-    if number % 8 == 7:
+    if number / 8 == 7:
         return 4
 
     # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number / 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 26 =====
```
     # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
     # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
     # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
-    if number % 8 == 7:
+    if number < 0:
         return 4
 
     # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number < 0:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
===== 27 =====
```
     # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
     # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
     if number % 8 == 7:
-        return 4
+        return 5
 
     # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
@@ -28,4 +28,4 @@         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 5

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 28 =====
```
     # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
-    for i in range(1, int(math.sqrt(number)) + 1):
+    for i in range(1, ):
         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, ):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 29 =====
```
     # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
-    for i in range(1, int(math.sqrt(number)) + 1):
+    for i in range(1, int(math.sqrt(number)) - 1):
         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) - 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 30 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number + i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number + i**2))**2 == number - i**2:
            return 2

    return 3

```
===== 31 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number - i * 2))**2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i * 2))**2 == number - i**2:
            return 2

    return 3

```
===== 32 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number - i**2)) * 2 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2)) * 2 == number - i**2:
            return 2

    return 3

```
===== 33 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number - i**2))**2 != number - i**2:
             return 2
 
     return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 != number - i**2:
            return 2

    return 3
```
===== 34 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number - i**2))**2 != number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 != number - i**2:
            return 2

    return 3

```
===== 35 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number - i**2))**2 < number - i**2:
             return 2
 
     return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 < number - i**2:
            return 2

    return 3
```
===== 36 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number - i**2))**2 == number + i**2:
             return 2
 
     return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number + i**2:
            return 2

    return 3
```
===== 37 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number - i**2))**2 == number + i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number + i**2:
            return 2

    return 3

```
===== 38 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number - i**2))**2 == number - (i**2 + 1):
             return 2
 
     return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - (i**2 + 1):
            return 2

    return 3
```
===== 39 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number - i**2))**2 == number - i * 2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i * 2:
            return 2

    return 3

```
===== 40 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number - i**2))**2 == number - i**3:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**3:
            return 2

    return 3

```
===== 41 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number - i**2))**2 > number - i**2:
             return 2
 
     return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 > number - i**2:
            return 2

    return 3
```
===== 42 =====
```
     # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
-        if int(math.sqrt(number - i**2))**2 == number - i**2:
+        if int(math.sqrt(number - i**2))**3 == number - i**2:
             return 2
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**3 == number - i**2:
            return 2

    return 3

```
===== 43 =====
```
     # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
     for i in range(1, int(math.sqrt(number)) + 1):
         if int(math.sqrt(number - i**2))**2 == number - i**2:
-            return 2
+            return 3
 
-    return 3+    return 3
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 3

    return 3

```
===== 44 =====
```
         if int(math.sqrt(number - i**2))**2 == number - i**2:
             return 2
 
-    return 3+    return 4
```
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 4

```
