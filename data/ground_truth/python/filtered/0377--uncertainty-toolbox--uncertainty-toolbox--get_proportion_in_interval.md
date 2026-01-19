https://github.com/uncertainty-toolbox/uncertainty-toolbox/blob/6ea1fed6591923a95d49d8049a197e33d4d8092d/./uncertainty_toolbox/metrics_calibration.py#L451-L489
```
🈚️

Timeout

@icontract.ensure(
    lambda result, y_pred, y_std, y_true, quantile:
        # 0) 必要的数值范围约束
        np.isfinite(result)
        and 0.0 <= result <= 1.0
        # 1) 如果没有数据，就只要求在 [0,1] 里即可
        and (
            y_pred.size == 0
            or (
                # 2) 如果样本数不大，直接对全部样本做“精确校验”（向量化实现）
                (
                    y_pred.size <= 512
                    and np.isclose(
                        result,
                        (
                            (
                                (
                                    (y_pred - y_true) / y_std
                                )
                                >= stats.norm(loc=0, scale=1).ppf(
                                    0.5 - quantile / 2.0
                                )
                            )
                            &
                            (
                                (
                                    (y_pred - y_true) / y_std
                                )
                                <= stats.norm(loc=0, scale=1).ppf(
                                    0.5 + quantile / 2.0
                                )
                            )
                        ).mean(),
                        rtol=1e-6,
                        atol=1e-8,
                    )
                )
                or
                # 3) 如果样本数很大，则对“均匀抽样的 512 个点”做近似校验
                (
                    y_pred.size > 512
                    and abs(
                        result
                        - (
                            (
                                (
                                    (
                                        (
                                            y_pred[
                                                np.linspace(
                                                    0,
                                                    y_pred.size - 1,
                                                    num=512,
                                                    dtype=int,
                                                )
                                            ]
                                            - y_true[
                                                np.linspace(
                                                    0,
                                                    y_pred.size - 1,
                                                    num=512,
                                                    dtype=int,
                                                )
                                            ]
                                        )
                                        / y_std[
                                            np.linspace(
                                                0,
                                                y_pred.size - 1,
                                                num=512,
                                                dtype=int,
                                            )
                                        ]
                                    )
                                    >= stats.norm(loc=0, scale=1).ppf(
                                        0.5 - quantile / 2.0
                                    )
                                )
                                &
                                (
                                    (
                                        (
                                            y_pred[
                                                np.linspace(
                                                    0,
                                                    y_pred.size - 1,
                                                    num=512,
                                                    dtype=int,
                                                )
                                            ]
                                            - y_true[
                                                np.linspace(
                                                    0,
                                                    y_pred.size - 1,
                                                    num=512,
                                                    dtype=int,
                                                )
                                            ]
                                        )
                                        / y_std[
                                            np.linspace(
                                                0,
                                                y_pred.size - 1,
                                                num=512,
                                                dtype=int,
                                            )
                                        ]
                                    )
                                    <= stats.norm(loc=0, scale=1).ppf(
                                        0.5 + quantile / 2.0
                                    )
                                )
                            ).mean()
                        )
                    ) <= 0.1  # 对大样本，仅要求近似一致，允许 0.1 的绝对误差
                )
            )
        ),
    "result must represent the proportion of normalized residuals within the "
    "target quantile interval (exact check for small n, approximate check for "
    "large n using evenly spaced samples).",
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
===== 0 =====
```
     assert_is_positive(y_std)
 
     # Computer lower and upper bound for quantile
-    norm = stats.norm(loc=0, scale=1)
+    norm = stats.norm(loc=0, scale=-1)  # Negative standard deviation
     lower_bound = norm.ppf(0.5 - quantile / 2)
     upper_bound = norm.ppf(0.5 + quantile / 2)
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=-1)  # Negative standard deviation
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 1 =====
```
     assert_is_positive(y_std)
 
     # Computer lower and upper bound for quantile
-    norm = stats.norm(loc=0, scale=1)
+    norm = stats.norm(loc=0, scale=0)  # Zero standard deviation
     lower_bound = norm.ppf(0.5 - quantile / 2)
     upper_bound = norm.ppf(0.5 + quantile / 2)
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=0)  # Zero standard deviation
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 2 =====
```
     assert_is_positive(y_std)
 
     # Computer lower and upper bound for quantile
-    norm = stats.norm(loc=0, scale=1)
+    norm = stats.norm(loc=0, scale=1.5)  # Incorrect scale
     lower_bound = norm.ppf(0.5 - quantile / 2)
     upper_bound = norm.ppf(0.5 + quantile / 2)
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1.5)  # Incorrect scale
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 3 =====
```
     assert_is_positive(y_std)
 
     # Computer lower and upper bound for quantile
-    norm = stats.norm(loc=0, scale=1)
+    norm = stats.norm(loc=0, scale=2)
     lower_bound = norm.ppf(0.5 - quantile / 2)
     upper_bound = norm.ppf(0.5 + quantile / 2)
 
@@ -36,4 +36,4 @@             num_within_quantile += 1.0
     proportion = num_within_quantile / len(residuals)
 
-    return proportion+    return proportion
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=2)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion

```
===== 4 =====
```
     assert_is_positive(y_std)
 
     # Computer lower and upper bound for quantile
-    norm = stats.norm(loc=0, scale=1)
+    norm = stats.norm(loc=0, scale=2)  # Incorrect scale
     lower_bound = norm.ppf(0.5 - quantile / 2)
     upper_bound = norm.ppf(0.5 + quantile / 2)
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=2)  # Incorrect scale
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 5 =====
```
     assert_is_positive(y_std)
 
     # Computer lower and upper bound for quantile
-    norm = stats.norm(loc=0, scale=1)
+    norm = stats.norm(loc=1, scale=1)
     lower_bound = norm.ppf(0.5 - quantile / 2)
     upper_bound = norm.ppf(0.5 + quantile / 2)
 
@@ -36,4 +36,4 @@             num_within_quantile += 1.0
     proportion = num_within_quantile / len(residuals)
 
-    return proportion+    return proportion
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=1, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion

```
===== 6 =====
```
     assert_is_positive(y_std)
 
     # Computer lower and upper bound for quantile
-    norm = stats.norm(loc=0, scale=1)
+    norm = stats.norm(loc=1, scale=1)  # Incorrect mean
     lower_bound = norm.ppf(0.5 - quantile / 2)
     upper_bound = norm.ppf(0.5 + quantile / 2)
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=1, scale=1)  # Incorrect mean
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 7 =====
```
 
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
-    lower_bound = norm.ppf(0.5 - quantile / 2)
+    lower_bound = norm.ppf(0.5 + quantile / 2)
     upper_bound = norm.ppf(0.5 + quantile / 2)
 
     # Compute proportion of normalized residuals within lower to upper bound
@@ -36,4 +36,4 @@             num_within_quantile += 1.0
     proportion = num_within_quantile / len(residuals)
 
-    return proportion+    return proportion
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 + quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion

```
===== 8 =====
```
 
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
-    lower_bound = norm.ppf(0.5 - quantile / 2)
+    lower_bound = norm.ppf(0.5 + quantile / 2)  # Incorrectly uses addition instead of subtraction
     upper_bound = norm.ppf(0.5 + quantile / 2)
 
     # Compute proportion of normalized residuals within lower to upper bound
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 + quantile / 2)  # Incorrectly uses addition instead of subtraction
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 9 =====
```
 
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
-    lower_bound = norm.ppf(0.5 - quantile / 2)
+    lower_bound = norm.ppf(0.5 - (quantile / 2) + 0.1)  # Introduces an arbitrary offset, distorting the bound
     upper_bound = norm.ppf(0.5 + quantile / 2)
 
     # Compute proportion of normalized residuals within lower to upper bound
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - (quantile / 2) + 0.1)  # Introduces an arbitrary offset, distorting the bound
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 10 =====
```
 
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
-    lower_bound = norm.ppf(0.5 - quantile / 2)
+    lower_bound = norm.ppf(0.5 - quantile * 2)
     upper_bound = norm.ppf(0.5 + quantile / 2)
 
     # Compute proportion of normalized residuals within lower to upper bound
@@ -36,4 +36,4 @@             num_within_quantile += 1.0
     proportion = num_within_quantile / len(residuals)
 
-    return proportion+    return proportion
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile * 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion

```
===== 11 =====
```
 
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
-    lower_bound = norm.ppf(0.5 - quantile / 2)
+    lower_bound = norm.ppf(0.5 - quantile / 4)  # Incorrectly divides the quantile by 4 instead of 2
     upper_bound = norm.ppf(0.5 + quantile / 2)
 
     # Compute proportion of normalized residuals within lower to upper bound
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 4)  # Incorrectly divides the quantile by 4 instead of 2
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 12 =====
```
 
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
-    lower_bound = norm.ppf(0.5 - quantile / 2)
+    lower_bound = norm.ppf(0.5 - quantile)  # Incorrectly subtracts the entire quantile instead of halving it
     upper_bound = norm.ppf(0.5 + quantile / 2)
 
     # Compute proportion of normalized residuals within lower to upper bound
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile)  # Incorrectly subtracts the entire quantile instead of halving it
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 13 =====
```
 
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
-    lower_bound = norm.ppf(0.5 - quantile / 2)
+    lower_bound = norm.ppf(1.5 - quantile / 2)
     upper_bound = norm.ppf(0.5 + quantile / 2)
 
     # Compute proportion of normalized residuals within lower to upper bound
@@ -36,4 +36,4 @@             num_within_quantile += 1.0
     proportion = num_within_quantile / len(residuals)
 
-    return proportion+    return proportion
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(1.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion

```
===== 14 =====
```
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
     lower_bound = norm.ppf(0.5 - quantile / 2)
-    upper_bound = norm.ppf(0.5 + quantile / 2)
+    upper_bound = norm.ppf(0.5 + quantile * 2)
 
     # Compute proportion of normalized residuals within lower to upper bound
     residuals = y_pred - y_true
@@ -36,4 +36,4 @@             num_within_quantile += 1.0
     proportion = num_within_quantile / len(residuals)
 
-    return proportion+    return proportion
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile * 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion

```
===== 15 =====
```
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
     lower_bound = norm.ppf(0.5 - quantile / 2)
-    upper_bound = norm.ppf(0.5 + quantile / 2)
+    upper_bound = norm.ppf(0.5 + quantile / 2 + 0.1)  # Incorrect: adds an arbitrary constant
 
     # Compute proportion of normalized residuals within lower to upper bound
     residuals = y_pred - y_true
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2 + 0.1)  # Incorrect: adds an arbitrary constant

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 16 =====
```
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
     lower_bound = norm.ppf(0.5 - quantile / 2)
-    upper_bound = norm.ppf(0.5 + quantile / 2)
+    upper_bound = norm.ppf(0.5 + quantile / 2 + 0.5 * quantile)  # Incorrect: adds a fraction of quantile
 
     # Compute proportion of normalized residuals within lower to upper bound
     residuals = y_pred - y_true
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2 + 0.5 * quantile)  # Incorrect: adds a fraction of quantile

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 17 =====
```
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
     lower_bound = norm.ppf(0.5 - quantile / 2)
-    upper_bound = norm.ppf(0.5 + quantile / 2)
+    upper_bound = norm.ppf(0.5 + quantile / 3)
 
     # Compute proportion of normalized residuals within lower to upper bound
     residuals = y_pred - y_true
@@ -36,4 +36,4 @@             num_within_quantile += 1.0
     proportion = num_within_quantile / len(residuals)
 
-    return proportion+    return proportion
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 3)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion

```
===== 18 =====
```
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
     lower_bound = norm.ppf(0.5 - quantile / 2)
-    upper_bound = norm.ppf(0.5 + quantile / 2)
+    upper_bound = norm.ppf(0.5 + quantile / 3)  # Incorrect: divides quantile by 3 instead of 2
 
     # Compute proportion of normalized residuals within lower to upper bound
     residuals = y_pred - y_true
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 3)  # Incorrect: divides quantile by 3 instead of 2

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 19 =====
```
     # Computer lower and upper bound for quantile
     norm = stats.norm(loc=0, scale=1)
     lower_bound = norm.ppf(0.5 - quantile / 2)
-    upper_bound = norm.ppf(0.5 + quantile / 2)
+    upper_bound = norm.ppf(0.5 + quantile)  # Incorrect: does not divide quantile by 2
 
     # Compute proportion of normalized residuals within lower to upper bound
     residuals = y_pred - y_true
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile)  # Incorrect: does not divide quantile by 2

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 20 =====
```
     # Compute proportion of normalized residuals within lower to upper bound
     residuals = y_pred - y_true
 
-    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)
+    normalized_residuals = residuals.reshape(-1) * y_std.reshape(-1)
 
     num_within_quantile = 0
     for resid in normalized_residuals:
@@ -36,4 +36,4 @@             num_within_quantile += 1.0
     proportion = num_within_quantile / len(residuals)
 
-    return proportion+    return proportion
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) * y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion

```
===== 21 =====
```
     normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)
 
     num_within_quantile = 0
-    for resid in normalized_residuals:
+    for resid in normalized_residuals[:5]:  # Only iterates over the first 5 elements
         if lower_bound <= resid and resid <= upper_bound:
             num_within_quantile += 1.0
     proportion = num_within_quantile / len(residuals)
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals[:5]:  # Only iterates over the first 5 elements
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals)

    return proportion
```
===== 22 =====
```
     for resid in normalized_residuals:
         if lower_bound <= resid and resid <= upper_bound:
             num_within_quantile += 1.0
-    proportion = num_within_quantile / len(residuals)
+    proportion = None
 
-    return proportion+    return proportion
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = None

    return proportion

```
===== 23 =====
```
     for resid in normalized_residuals:
         if lower_bound <= resid and resid <= upper_bound:
             num_within_quantile += 1.0
-    proportion = num_within_quantile / len(residuals)
+    proportion = num_within_quantile / len(residuals) * 2  # Incorrectly doubles the proportion, leading to values greater than 1.
 
     return proportion
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals) * 2  # Incorrectly doubles the proportion, leading to values greater than 1.

    return proportion
```
===== 24 =====
```
     for resid in normalized_residuals:
         if lower_bound <= resid and resid <= upper_bound:
             num_within_quantile += 1.0
-    proportion = num_within_quantile / len(residuals)
+    proportion = num_within_quantile / len(residuals) + 0.1  # Incorrectly adds a constant, skewing the proportion upwards.
 
     return proportion
```
```
def get_proportion_in_interval(
    y_pred: np.ndarray, y_std: np.ndarray, y_true: np.ndarray, quantile: float
) -> float:
    """For a specified quantile, return the proportion of points falling into
    an interval corresponding to that quantile.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        quantile: a specified quantile level

    Returns:
        A single scalar which is the proportion of the true labels falling into the
        prediction interval for the specified quantile.
    """

    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)
    # Check that input std is positive
    assert_is_positive(y_std)

    # Computer lower and upper bound for quantile
    norm = stats.norm(loc=0, scale=1)
    lower_bound = norm.ppf(0.5 - quantile / 2)
    upper_bound = norm.ppf(0.5 + quantile / 2)

    # Compute proportion of normalized residuals within lower to upper bound
    residuals = y_pred - y_true

    normalized_residuals = residuals.reshape(-1) / y_std.reshape(-1)

    num_within_quantile = 0
    for resid in normalized_residuals:
        if lower_bound <= resid and resid <= upper_bound:
            num_within_quantile += 1.0
    proportion = num_within_quantile / len(residuals) + 0.1  # Incorrectly adds a constant, skewing the proportion upwards.

    return proportion
```
