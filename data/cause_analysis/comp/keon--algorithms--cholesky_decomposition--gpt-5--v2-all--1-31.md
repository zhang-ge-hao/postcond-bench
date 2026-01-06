https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/matrix/cholesky_matrix_decomposition.py#L27-L51
```
@icontract.ensure(lambda A, result: not any(len(row) != len(A) for row in A) or result is None)
@icontract.ensure(lambda A, result: result is None or len(result) == len(A))
@icontract.ensure(lambda A, result: result is None or all(len(row) == len(A) for row in result))
@icontract.ensure(lambda result: result is None or all(result[i][j] == 0.0 for i in range(len(result)) for j in range(i + 1, len(result))))
@icontract.ensure(lambda result: result is None or all(result[i][i] > 0.0 for i in range(len(result))))
@icontract.ensure(lambda A, result: result is None or all(math.isclose(sum(result[i][k] * result[j][k] for k in range(len(result))), A[i][j], rel_tol=1e-9, abs_tol=1e-9) for i in range(len(result)) for j in range(len(result))))
```
```
return value - built-in container of scalars


return value content

built-in container of scalars
```
passed
```
@icontract.ensure(
    lambda A, result:
        all(len(row) == len(A) for row in A)
        or result is None,
)
@icontract.ensure(
    lambda A, result:
        (result is None)
        or (
            all(len(row) == len(A) for row in A)
            and len(result) == len(A)
            and all(len(row) == len(A) for row in result)
            and all(
                result[i][j] == 0.0
                for i in range(len(result))
                for j in range(i + 1, len(result))
            )
            and all(
                result[i][i] > 0.0
                for i in range(len(result))
            )
            and all(
                abs(
                    A[i][j]
                    - sum(
                        result[i][k] * result[j][k]
                        for k in range(len(result))
                    )
                ) < 1e-8
                for i in range(len(A))
                for j in range(len(A))
            )
        ),
)
@icontract.ensure(
    lambda A, result:
        not (
            len(A) > 0
            and all(len(row) == len(A) for row in A)
            and all(
                A[i][j] == A[j][i]
                for i in range(len(A))
                for j in range(len(A))
            )
            and (
                (lambda det:
                    all(
                        det(
                            det,
                            [row[:k + 1] for row in A[:k + 1]]
                        ) > 0
                        for k in range(len(A))
                    )
                )(
                    lambda self, M:
                        M[0][0]
                        if len(M) == 1
                        else sum(
                            ((-1) ** j)
                            * M[0][j]
                            * self(
                                self,
                                [
                                    [
                                        M[r][c]
                                        for c in range(len(M))
                                        if c != j
                                    ]
                                    for r in range(1, len(M))
                                ],
                            )
                            for j in range(len(M))
                        )
                )
            )
        ) or result is not None,
)

```
===== 31: failed =====
```
         for k in range(j):
             sum_diagonal_element = sum_diagonal_element + math.pow(V[j][k], 2)
         sum_diagonal_element = A[j][j] - sum_diagonal_element
-        if sum_diagonal_element <= 0:
+        if sum_diagonal_element >= 0:
             return None
         V[j][j] = math.pow(sum_diagonal_element, 0.5)
         for i in range(j+1, n):
```
```
def cholesky_decomposition(A):
    """
    :param A: Hermitian positive-definite matrix of type List[List[float]]
    :return: matrix of type List[List[float]] if A can be decomposed,
    otherwise None
    """
    n = len(A)
    for ai in A:
        if len(ai) != n:
            return None
    V = [[0.0] * n for _ in range(n)]
    for j in range(n):
        sum_diagonal_element = 0
        for k in range(j):
            sum_diagonal_element = sum_diagonal_element + math.pow(V[j][k], 2)
        sum_diagonal_element = A[j][j] - sum_diagonal_element
        if sum_diagonal_element >= 0:
            return None
        V[j][j] = math.pow(sum_diagonal_element, 0.5)
        for i in range(j+1, n):
            sum_other_element = 0
            for k in range(j):
                sum_other_element += V[i][k]*V[j][k]
            V[i][j] = (A[i][j] - sum_other_element)/V[j][j]
    return V
```
