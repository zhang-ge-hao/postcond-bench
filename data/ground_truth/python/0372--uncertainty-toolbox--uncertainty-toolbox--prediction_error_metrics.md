https://github.com/uncertainty-toolbox/uncertainty-toolbox/blob/6ea1fed6591923a95d49d8049a197e33d4d8092d/./uncertainty_toolbox/metrics_accuracy.py#L16-L52
```
@icontract.snapshot(lambda y_pred: y_pred.copy(), name="OLD_yp")
@icontract.snapshot(lambda y_true: y_true.copy(), name="OLD_yt")
@icontract.ensure(lambda result: isinstance(result, dict))
@icontract.ensure(
    lambda result: isinstance(result, dict)
    and set(result.keys()) == {"mae", "rmse", "mdae", "marpd", "r2", "corr"}
)
@icontract.ensure(lambda OLD, y_pred: np.array_equal(OLD.OLD_yp, y_pred))
@icontract.ensure(lambda OLD, y_true: np.array_equal(OLD.OLD_yt, y_true))
@icontract.ensure(
    lambda result: isinstance(result, dict)
    and "mae" in result
    and isinstance(result["mae"], (int, float, np.floating))
    and np.isfinite(result["mae"])
    and result["mae"] >= 0
)
@icontract.ensure(
    lambda result, y_pred, y_true: isinstance(result, dict)
    and "mae" in result
    and isinstance(result["mae"], (int, float, np.floating))
    and np.isclose(result["mae"], np.mean(np.abs(y_true - y_pred)))
)
@icontract.ensure(
    lambda result: isinstance(result, dict)
    and "rmse" in result
    and isinstance(result["rmse"], (int, float, np.floating))
    and np.isfinite(result["rmse"])
    and result["rmse"] >= 0
)
@icontract.ensure(
    lambda result, y_pred, y_true: isinstance(result, dict)
    and "rmse" in result
    and isinstance(result["rmse"], (int, float, np.floating))
    and np.isclose(
        result["rmse"], np.sqrt(np.mean((y_true - y_pred) ** 2))
    )
)
@icontract.ensure(
    lambda result: isinstance(result, dict)
    and "mdae" in result
    and isinstance(result["mdae"], (int, float, np.floating))
    and np.isfinite(result["mdae"])
    and result["mdae"] >= 0
)
@icontract.ensure(
    lambda result, y_pred, y_true: isinstance(result, dict)
    and "mdae" in result
    and isinstance(result["mdae"], (int, float, np.floating))
    and np.isclose(
        result["mdae"], np.median(np.abs(y_true - y_pred))
    )
)
@icontract.ensure(
    lambda result: isinstance(result, dict)
    and "marpd" in result
    and isinstance(result["marpd"], (int, float, np.floating))
    and np.isfinite(result["marpd"])
    and result["marpd"] >= 0
)
@icontract.ensure(
    lambda result, y_pred, y_true: isinstance(result, dict)
    and "marpd" in result
    and isinstance(result["marpd"], (int, float, np.floating))
    and np.isclose(
        result["marpd"],
        np.abs(
            2 * (y_true - y_pred) / (np.abs(y_pred) + np.abs(y_true))
        ).mean()
        * 100,
    )
)
@icontract.ensure(
    lambda result: isinstance(result, dict)
    and "r2" in result
    and isinstance(result["r2"], (int, float, np.floating))
    and (np.isfinite(result["r2"]) or np.isnan(result["r2"]))
)
@icontract.ensure(
    lambda result, y_pred, y_true: isinstance(result, dict)
    and "r2" in result
    and isinstance(result["r2"], (int, float, np.floating))
    and (
        (np.isnan(result["r2"]) and np.isnan(r2_score(y_true, y_pred)))
        or np.isclose(result["r2"], r2_score(y_true, y_pred))
    )
)
@icontract.ensure(
    lambda result: isinstance(result, dict)
    and "corr" in result
    and isinstance(result["corr"], (int, float, np.floating))
    and (np.isfinite(result["corr"]) or np.isnan(result["corr"]))
)
@icontract.ensure(
    lambda result, y_pred, y_true: isinstance(result, dict)
    and "corr" in result
    and isinstance(result["corr"], (int, float, np.floating))
    and (
        (
            np.isnan(result["corr"])
            and np.isnan(np.corrcoef(y_true, y_pred)[0, 1])
        )
        or np.isclose(
            result["corr"],
            np.corrcoef(y_true, y_pred)[0, 1],
        )
    )
)
```
```
@icontract.snapshot(lambda y_pred: y_pred.copy(), name="OLD_yp")
@icontract.snapshot(lambda y_true: y_true.copy(), name="OLD_yt")
@icontract.ensure(lambda result: isinstance(result, dict))
@icontract.ensure(lambda result: set(result.keys()) == {"mae", "rmse", "mdae", "marpd", "r2", "corr"})
@icontract.ensure(lambda OLD, y_pred: np.array_equal(OLD.OLD_yp, y_pred))
@icontract.ensure(lambda OLD, y_true: np.array_equal(OLD.OLD_yt, y_true))
@icontract.ensure(lambda result: isinstance(result["mae"], (int, float, np.floating)) and np.isfinite(result["mae"]) and result["mae"] >= 0)
@icontract.ensure(lambda result, y_pred, y_true: np.isclose(result["mae"], np.mean(np.abs(y_true - y_pred))))
@icontract.ensure(lambda result: isinstance(result["rmse"], (int, float, np.floating)) and np.isfinite(result["rmse"]) and result["rmse"] >= 0)
@icontract.ensure(lambda result, y_pred, y_true: np.isclose(result["rmse"], np.sqrt(np.mean((y_true - y_pred) ** 2))))
@icontract.ensure(lambda result: isinstance(result["mdae"], (int, float, np.floating)) and np.isfinite(result["mdae"]) and result["mdae"] >= 0)
@icontract.ensure(lambda result, y_pred, y_true: np.isclose(result["mdae"], np.median(np.abs(y_true - y_pred))))
@icontract.ensure(lambda result: isinstance(result["marpd"], (int, float, np.floating)) and np.isfinite(result["marpd"]) and result["marpd"] >= 0)
@icontract.ensure(lambda result, y_pred, y_true: np.isclose(result["marpd"], np.abs(2 * (y_true - y_pred) / (np.abs(y_pred) + np.abs(y_true))).mean() * 100))
@icontract.ensure(lambda result: isinstance(result["r2"], (int, float, np.floating)) and (np.isfinite(result["r2"]) or np.isnan(result["r2"])))
@icontract.ensure(lambda result, y_pred, y_true: (np.isnan(result["r2"]) and np.isnan(r2_score(y_true, y_pred))) or np.isclose(result["r2"], r2_score(y_true, y_pred)))
@icontract.ensure(lambda result: isinstance(result["corr"], (int, float, np.floating)) and (np.isfinite(result["corr"]) or np.isnan(result["corr"])))
@icontract.ensure(lambda result, y_pred, y_true: (np.isnan(result["corr"]) and np.isnan(np.corrcoef(y_true, y_pred)[0, 1])) or np.isclose(result["corr"], np.corrcoef(y_true, y_pred)[0, 1]))
```
[0, 3, 8, 15, 25, 30, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
===== 0 =====
```
     assert_is_flat_same_shape(y_pred, y_true)
 
     # Compute metrics
-    mae = mean_absolute_error(y_true, y_pred)
+    mae = None
     rmse = np.sqrt(mean_squared_error(y_true, y_pred))
     mdae = median_absolute_error(y_true, y_pred)
     residuals = y_true - y_pred
@@ -34,4 +34,4 @@         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = None
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 3 =====
```
 
     # Compute metrics
     mae = mean_absolute_error(y_true, y_pred)
-    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
+    rmse = None
     mdae = median_absolute_error(y_true, y_pred)
     residuals = y_true - y_pred
     marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
@@ -34,4 +34,4 @@         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = None
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 8 =====
```
     # Compute metrics
     mae = mean_absolute_error(y_true, y_pred)
     rmse = np.sqrt(mean_squared_error(y_true, y_pred))
-    mdae = median_absolute_error(y_true, y_pred)
+    mdae = None
     residuals = y_true - y_pred
     marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
     r2 = r2_score(y_true, y_pred)
@@ -34,4 +34,4 @@         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = None
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 15 =====
```
     rmse = np.sqrt(mean_squared_error(y_true, y_pred))
     mdae = median_absolute_error(y_true, y_pred)
     residuals = y_true - y_pred
-    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
+    marpd = None
     r2 = r2_score(y_true, y_pred)
     corr = np.corrcoef(y_true, y_pred)[0, 1]
     prediction_metrics = {
@@ -34,4 +34,4 @@         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = None
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 25 =====
```
     mdae = median_absolute_error(y_true, y_pred)
     residuals = y_true - y_pred
     marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
-    r2 = r2_score(y_true, y_pred)
+    r2 = None
     corr = np.corrcoef(y_true, y_pred)[0, 1]
     prediction_metrics = {
         "mae": mae,
@@ -34,4 +34,4 @@         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = None
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 30 =====
```
     residuals = y_true - y_pred
     marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
     r2 = r2_score(y_true, y_pred)
-    corr = np.corrcoef(y_true, y_pred)[0, 1]
+    corr = None
     prediction_metrics = {
         "mae": mae,
         "rmse": rmse,
@@ -34,4 +34,4 @@         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = None
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 35 =====
```
     marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
     r2 = r2_score(y_true, y_pred)
     corr = np.corrcoef(y_true, y_pred)[0, 1]
-    prediction_metrics = {
-        "mae": mae,
-        "rmse": rmse,
-        "mdae": mdae,
-        "marpd": marpd,
-        "r2": r2,
-        "corr": corr,
-    }
+    prediction_metrics = None
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = None

    return prediction_metrics

```
===== 36 =====
```
     r2 = r2_score(y_true, y_pred)
     corr = np.corrcoef(y_true, y_pred)[0, 1]
     prediction_metrics = {
-        "mae": mae,
+        "MAE": mae,
         "rmse": rmse,
         "mdae": mdae,
         "marpd": marpd,
@@ -34,4 +34,4 @@         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "MAE": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 37 =====
```
     r2 = r2_score(y_true, y_pred)
     corr = np.corrcoef(y_true, y_pred)[0, 1]
     prediction_metrics = {
-        "mae": mae,
+        "XXmaeXX": mae,
         "rmse": rmse,
         "mdae": mdae,
         "marpd": marpd,
@@ -34,4 +34,4 @@         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "XXmaeXX": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 38 =====
```
     corr = np.corrcoef(y_true, y_pred)[0, 1]
     prediction_metrics = {
         "mae": mae,
-        "rmse": rmse,
+        "RMSE": rmse,
         "mdae": mdae,
         "marpd": marpd,
         "r2": r2,
         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "RMSE": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 39 =====
```
     corr = np.corrcoef(y_true, y_pred)[0, 1]
     prediction_metrics = {
         "mae": mae,
-        "rmse": rmse,
+        "XXrmseXX": rmse,
         "mdae": mdae,
         "marpd": marpd,
         "r2": r2,
         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "XXrmseXX": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 40 =====
```
     prediction_metrics = {
         "mae": mae,
         "rmse": rmse,
-        "mdae": mdae,
+        "MDAE": mdae,
         "marpd": marpd,
         "r2": r2,
         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "MDAE": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 41 =====
```
     prediction_metrics = {
         "mae": mae,
         "rmse": rmse,
-        "mdae": mdae,
+        "XXmdaeXX": mdae,
         "marpd": marpd,
         "r2": r2,
         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "XXmdaeXX": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 42 =====
```
         "mae": mae,
         "rmse": rmse,
         "mdae": mdae,
-        "marpd": marpd,
+        "MARPD": marpd,
         "r2": r2,
         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "MARPD": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 43 =====
```
         "mae": mae,
         "rmse": rmse,
         "mdae": mdae,
-        "marpd": marpd,
+        "XXmarpdXX": marpd,
         "r2": r2,
         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "XXmarpdXX": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 44 =====
```
         "rmse": rmse,
         "mdae": mdae,
         "marpd": marpd,
-        "r2": r2,
+        "R2": r2,
         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "R2": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 45 =====
```
         "rmse": rmse,
         "mdae": mdae,
         "marpd": marpd,
-        "r2": r2,
+        "XXr2XX": r2,
         "corr": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "XXr2XX": r2,
        "corr": corr,
    }

    return prediction_metrics

```
===== 46 =====
```
         "mdae": mdae,
         "marpd": marpd,
         "r2": r2,
-        "corr": corr,
+        "CORR": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "CORR": corr,
    }

    return prediction_metrics

```
===== 47 =====
```
         "mdae": mdae,
         "marpd": marpd,
         "r2": r2,
-        "corr": corr,
+        "XXcorrXX": corr,
     }
 
-    return prediction_metrics+    return prediction_metrics
```
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "XXcorrXX": corr,
    }

    return prediction_metrics

```
