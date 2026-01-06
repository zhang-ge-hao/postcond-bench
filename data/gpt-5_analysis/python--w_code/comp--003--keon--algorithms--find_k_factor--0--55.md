https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/dp/k_factor.py#L33-L85
```
@icontract.ensure(lambda result: isinstance(result, int))
@icontract.ensure(lambda result: result >= 0)
@icontract.ensure(lambda length, result: result <= 26 ** length)
@icontract.ensure(lambda length, k_factor, result: not (3 * k_factor + 1 > length) or result == 0)
@icontract.ensure(lambda length, k_factor, result: not (length == 3 * k_factor + 1 and k_factor >= 1) or result == 1)
@icontract.ensure(lambda length, k_factor, result: not (1 <= length < 4 and k_factor == 0) or result == 26 ** length)
```
```
No direct verification.
```
passed
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
===== 55 =====
failed
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
