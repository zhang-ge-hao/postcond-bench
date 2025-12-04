https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/dp/k_factor.py#L33-L85
```
@icontract.ensure(
    lambda result, length, k_factor:
        result
        == (
            0
            if 3 * k_factor + 1 > length
            else sum(
                (
                    (lambda max_j:
                        (lambda f: f(f, length))(
                            lambda self, i:
                                [
                                    [1, 0, 0, 25] if j == 0 else [0, 0, 0, 0]
                                    for j in range(max_j)
                                ]
                                if i == 1
                                else
                                (lambda prev_row:
                                    [
                                        (
                                            [
                                                prev_row[j][0] + prev_row[j][1] + prev_row[j][3],
                                                prev_row[j][0],
                                                prev_row[j][1],
                                                prev_row[j][0] * 24
                                                + prev_row[j][1] * 24
                                                + prev_row[j][2] * 25
                                                + prev_row[j][3] * 25,
                                            ]
                                            if j == 0
                                            else (
                                                [
                                                    prev_row[j][0]
                                                    + prev_row[j][1]
                                                    + prev_row[j][3]
                                                    + prev_row[j - 1][2],
                                                    prev_row[j][0],
                                                    prev_row[j][1],
                                                    prev_row[j][0] * 24
                                                    + prev_row[j][1] * 24
                                                    + prev_row[j][2] * 25
                                                    + prev_row[j][3] * 25,
                                                ]
                                                if 3 * j + 1 < i
                                                else (
                                                    [1, 0, 0, 0]
                                                    if 3 * j + 1 == i
                                                    else [0, 0, 0, 0]
                                                )
                                            )
                                        )
                                        for j in range(max_j)
                                    ]
                                )(self(self, i - 1))
                        )
                    )((length - 1) // 3 + 2)[k_factor]
                )
            )
        )
)
```
```
@icontract.snapshot(lambda length: length, name="length")
@icontract.snapshot(lambda k_factor: k_factor, name="k_factor")
@icontract.ensure(lambda result, length, k_factor: (3 * k_factor + 1 > length) == (result == 0))
@icontract.ensure(lambda result: isinstance(result, int) and result >= 0)
@icontract.ensure(lambda result, length: result <= 26 ** length)
@icontract.ensure(lambda result, length, k_factor: (not (length == 1 and k_factor == 0)) or result == 26)
@icontract.ensure(lambda result, length, k_factor: (not (length == 2 and k_factor == 0)) or result == 676)
@icontract.ensure(lambda result, length, k_factor: (not (length == 3 and k_factor == 0)) or result == 17576)
@icontract.ensure(lambda result, length, k_factor: (not (length == 4 and k_factor == 1)) or result == 1)
@icontract.ensure(lambda result, length, k_factor: (not (length == 4 and k_factor == 0)) or result == 456975)
@icontract.ensure(lambda result, length, k_factor: (not (length == 5 and k_factor == 1)) or result == 52)
@icontract.ensure(lambda result, length, k_factor: (not (length == 6 and k_factor == 1)) or result == 2028)
@icontract.ensure(lambda result, length, k_factor: (not (length == 7 and k_factor == 2)) or result == 1)
```
[7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 21, 22, 23, 26, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 49, 51, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 86, 88, 90, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 113]
===== 7 =====
```
     if 3*k_factor+1>length:
         return 0
     #base cases
-    mat[1][0][0]=1
+    mat[1][0][0]=2
     mat[1][0][1]=0
     mat[1][0][2]=0
     mat[1][0][3]=25
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=2
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 8 =====
```
     if 3*k_factor+1>length:
         return 0
     #base cases
-    mat[1][0][0]=1
+    mat[1][0][1]=1
     mat[1][0][1]=0
     mat[1][0][2]=0
     mat[1][0][3]=25
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][1]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 9 =====
```
     if 3*k_factor+1>length:
         return 0
     #base cases
-    mat[1][0][0]=1
+    mat[1][1][0]=1
     mat[1][0][1]=0
     mat[1][0][2]=0
     mat[1][0][3]=25
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][1][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 10 =====
```
     if 3*k_factor+1>length:
         return 0
     #base cases
-    mat[1][0][0]=1
+    mat[2][0][0]=1
     mat[1][0][1]=0
     mat[1][0][2]=0
     mat[1][0][3]=25
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[2][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 11 =====
```
         return 0
     #base cases
     mat[1][0][0]=1
-    mat[1][0][1]=0
+    mat[1][0][1]=1
     mat[1][0][2]=0
     mat[1][0][3]=25
 
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=1
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 12 =====
```
     #base cases
     mat[1][0][0]=1
     mat[1][0][1]=0
-    mat[1][0][2]=0
+    mat[1][0][2]=1
     mat[1][0][3]=25
 
     for i in range(2,length+1):
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=1
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 13 =====
```
     mat[1][0][0]=1
     mat[1][0][1]=0
     mat[1][0][2]=0
-    mat[1][0][3]=25
+    mat[1][0][3]=26
 
     for i in range(2,length+1):
         for j in range((length-1)//3+2):
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=26

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 14 =====
```
     mat[1][0][0]=1
     mat[1][0][1]=0
     mat[1][0][2]=0
-    mat[1][0][3]=25
+    mat[1][1][3]=25
 
     for i in range(2,length+1):
         for j in range((length-1)//3+2):
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][1][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 15 =====
```
     mat[1][0][0]=1
     mat[1][0][1]=0
     mat[1][0][2]=0
-    mat[1][0][3]=25
+    mat[2][0][3]=25
 
     for i in range(2,length+1):
         for j in range((length-1)//3+2):
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[2][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 16 =====
```
     mat[1][0][2]=0
     mat[1][0][3]=25
 
-    for i in range(2,length+1):
+    for i in range(1, length+1):
         for j in range((length-1)//3+2):
             if j==0:
                 #adding a at the end
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(1, length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])
```
===== 21 =====
```
     mat[1][0][2]=0
     mat[1][0][3]=25
 
-    for i in range(2,length+1):
+    for i in range(3, length+1):
         for j in range((length-1)//3+2):
             if j==0:
                 #adding a at the end
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(3, length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])
```
===== 22 =====
```
     mat[1][0][2]=0
     mat[1][0][3]=25
 
-    for i in range(2,length+1):
+    for i in range(3,length+1):
         for j in range((length-1)//3+2):
             if j==0:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(3,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 23 =====
```
     mat[1][0][2]=0
     mat[1][0][3]=25
 
-    for i in range(2,length+1):
+    for i in range(length+1):
         for j in range((length-1)//3+2):
             if j==0:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 26 =====
```
     mat[1][0][3]=25
 
     for i in range(2,length+1):
-        for j in range((length-1)//3+2):
+        for j in range(1, (length-1)//3+2):  # This will start from 1, missing the case for k_factor = 0.
             if j==0:
                 #adding a at the end
                 mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range(1, (length-1)//3+2):  # This will start from 1, missing the case for k_factor = 0.
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])
```
===== 32 =====
```
         for j in range((length-1)//3+2):
             if j==0:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
+                mat[i][j][0]=mat[i-1][j][0] - mat[i-1][j][1]+mat[i-1][j][3]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0] - mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 34 =====
```
         for j in range((length-1)//3+2):
             if j==0:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
+                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-2][j][3]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-2][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 35 =====
```
         for j in range((length-1)//3+2):
             if j==0:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
+                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][2]+mat[i-1][j][3]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][2]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 36 =====
```
         for j in range((length-1)//3+2):
             if j==0:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
+                mat[i][j][0]=mat[i-1][j][0]+mat[i-2][j][1]+mat[i-1][j][3]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-2][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 37 =====
```
         for j in range((length-1)//3+2):
             if j==0:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
+                mat[i][j][0]=mat[i-1][j][1]+mat[i-1][j][1]+mat[i-1][j][3]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][1]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 38 =====
```
         for j in range((length-1)//3+2):
             if j==0:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
+                mat[i][j][0]=mat[i-2][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-2][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 39 =====
```
         for j in range((length-1)//3+2):
             if j==0:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
+                mat[i][j][1]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][1]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 40 =====
```
                 mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
 
                 #adding b at the end
-                mat[i][j][1]=mat[i-1][j][0]
+                mat[i][j][1]=mat[i-1][j][1]
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][1]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 41 =====
```
                 mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
 
                 #adding b at the end
-                mat[i][j][1]=mat[i-1][j][0]
+                mat[i][j][1]=mat[i-2][j][0]
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-2][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 42 =====
```
                 mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]
 
                 #adding b at the end
-                mat[i][j][1]=mat[i-1][j][0]
+                mat[i][j][2]=mat[i-1][j][0]
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][2]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 43 =====
```
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
-                mat[i][j][2]=mat[i-1][j][1]
+                mat[i][j][2]=mat[i-1][j][2]
 
                 #adding any other lowercase character
                 mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][2]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 44 =====
```
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
-                mat[i][j][2]=mat[i-1][j][1]
+                mat[i][j][2]=mat[i-2][j][1]
 
                 #adding any other lowercase character
                 mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-2][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 45 =====
```
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
-                mat[i][j][2]=mat[i-1][j][1]
+                mat[i][j][3]=mat[i-1][j][1]
 
                 #adding any other lowercase character
                 mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][3]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 47 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24 - mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24 - mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 49 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24 - mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24 - mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 51 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25 - mat[i-1][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25 - mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 53 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*26
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*26

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 54 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-2][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-2][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 55 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*26+mat[i-1][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*26+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 56 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][3]*25+mat[i-1][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][3]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 57 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-2][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-2][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 58 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*25+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*25+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 59 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][2]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][2]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 60 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-2][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-2][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 61 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*25+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*25+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 62 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][1]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][1]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 63 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-2][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1<i:
                 #adding a at the end
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-2][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 64 =====
```
                 #adding any other lowercase character
                 mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
-            elif 3*j+1<i:
+            elif 3*j+2<i:
                 #adding a at the end
                 mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
 
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+2<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 65 =====
```
                 #adding any other lowercase character
                 mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
-            elif 3*j+1<i:
+            elif 4*j+1<i:
                 #adding a at the end
                 mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
 
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 4*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 66 =====
```
 
             elif 3*j+1<i:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
+                mat[i][j][0]=mat[i-1][j][0] - mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0] - mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 67 =====
```
 
             elif 3*j+1<i:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
+                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1] - mat[i-1][j][3]+mat[i-1][j-1][2]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1] - mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 69 =====
```
 
             elif 3*j+1<i:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
+                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j + 1][2]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j + 1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 70 =====
```
 
             elif 3*j+1<i:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
+                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][3]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 71 =====
```
 
             elif 3*j+1<i:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
+                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-2][2]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-2][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 72 =====
```
 
             elif 3*j+1<i:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
+                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-2][j-1][2]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-2][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 73 =====
```
 
             elif 3*j+1<i:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
+                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-2][j][3]+mat[i-1][j-1][2]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-2][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 74 =====
```
 
             elif 3*j+1<i:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
+                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][2]+mat[i-1][j][3]+mat[i-1][j-1][2]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][2]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 75 =====
```
 
             elif 3*j+1<i:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
+                mat[i][j][0]=mat[i-1][j][0]+mat[i-2][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-2][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 76 =====
```
 
             elif 3*j+1<i:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
+                mat[i][j][0]=mat[i-1][j][1]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][1]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 77 =====
```
 
             elif 3*j+1<i:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
+                mat[i][j][0]=mat[i-2][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-2][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 78 =====
```
 
             elif 3*j+1<i:
                 #adding a at the end
-                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
+                mat[i][j][1]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][1]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 79 =====
```
                 mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
 
                 #adding b at the end
-                mat[i][j][1]=mat[i-1][j][0]
+                mat[i][j][1]=mat[i-1][j][1]
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][1]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 80 =====
```
                 mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
 
                 #adding b at the end
-                mat[i][j][1]=mat[i-1][j][0]
+                mat[i][j][1]=mat[i-2][j][0]
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-2][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 81 =====
```
                 mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]
 
                 #adding b at the end
-                mat[i][j][1]=mat[i-1][j][0]
+                mat[i][j][2]=mat[i-1][j][0]
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][2]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 82 =====
```
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
-                mat[i][j][2]=mat[i-1][j][1]
+                mat[i][j][2]=mat[i-1][j][2]
 
                 #adding any other lowercase character
                 mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][2]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 83 =====
```
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
-                mat[i][j][2]=mat[i-1][j][1]
+                mat[i][j][2]=mat[i-2][j][1]
 
                 #adding any other lowercase character
                 mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-2][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 84 =====
```
 
                 #adding b at the end
                 mat[i][j][1]=mat[i-1][j][0]
-                mat[i][j][2]=mat[i-1][j][1]
+                mat[i][j][3]=mat[i-1][j][1]
 
                 #adding any other lowercase character
                 mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][3]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 86 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24 - mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24 - mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 88 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24 - mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24 - mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 90 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25 - mat[i-1][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25 - mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 92 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*26
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*26

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 93 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-2][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-2][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 94 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*26+mat[i-1][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*26+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 95 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][3]*25+mat[i-1][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][3]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 96 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-2][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-2][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 97 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*25+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*25+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 98 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][2]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][2]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 99 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-2][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-2][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 100 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][0]*25+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*25+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 101 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-1][j][1]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][1]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 102 =====
```
                 mat[i][j][2]=mat[i-1][j][1]
 
                 #adding any other lowercase character
-                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
+                mat[i][j][3]=mat[i-2][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
             elif 3*j+1==i:
                 mat[i][j][0]=1
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-2][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 103 =====
```
                 #adding any other lowercase character
                 mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25
 
-            elif 3*j+1==i:
+            elif 3 / j+1==i:
                 mat[i][j][0]=1
                 mat[i][j][1]=0
                 mat[i][j][2]=0
@@ -50,4 +50,4 @@                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return sum(mat[length][k_factor])
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3 / j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])

```
===== 113 =====
```
                 mat[i][j][2]=0
                 mat[i][j][3]=0
 
-    return sum(mat[length][k_factor])+    return mat[length][k_factor][0]  # Only returns the count of strings ending with 'a'
```
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return mat[length][k_factor][0]  # Only returns the count of strings ending with 'a'
```
