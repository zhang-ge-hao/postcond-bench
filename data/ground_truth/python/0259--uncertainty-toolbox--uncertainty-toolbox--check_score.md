https://github.com/uncertainty-toolbox/uncertainty-toolbox/blob/6ea1fed6591923a95d49d8049a197e33d4d8092d/./uncertainty_toolbox/metrics_scoring_rule.py#L92-L142
```
@icontract.snapshot(lambda y_pred: y_pred.copy(), name="y_pred_")
@icontract.snapshot(lambda y_std: y_std.copy(), name="y_std_")
@icontract.snapshot(lambda y_true: y_true.copy(), name="y_true_")
@icontract.snapshot(lambda scaled: scaled, name="scaled_")
@icontract.snapshot(lambda start_q: start_q, name="start_q_")
@icontract.snapshot(lambda end_q: end_q, name="end_q_")
@icontract.snapshot(lambda resolution: resolution, name="resolution_")
@icontract.ensure(
    lambda result, OLD: result and np.allclose(
        result,
        np.sum(
            [
                np.mean(
                    (
                        (stats.norm.ppf(q, loc=OLD.y_pred_, scale=OLD.y_std_) - OLD.y_true_)
                        >= 0
                    ).astype(float)
                    * (stats.norm.ppf(q, loc=OLD.y_pred_, scale=OLD.y_std_) - OLD.y_true_)
                    - q
                    * (stats.norm.ppf(q, loc=OLD.y_pred_, scale=OLD.y_std_) - OLD.y_true_)
                )
                for q in np.linspace(OLD.start_q_, OLD.end_q_, OLD.resolution_)
            ]
        )
        / (OLD.resolution_ if OLD.scaled_ else 1),
        atol=1e-12,
        rtol=1e-8,
    )
)
@icontract.ensure(lambda result: result and np.isfinite(result))
```
```
@icontract.snapshot(lambda y_pred: y_pred.copy(), name="y_pred_")
@icontract.snapshot(lambda y_std: y_std.copy(), name="y_std_")
@icontract.snapshot(lambda y_true: y_true.copy(), name="y_true_")
@icontract.snapshot(lambda scaled: scaled, name="scaled_")
@icontract.snapshot(lambda start_q: start_q, name="start_q_")
@icontract.snapshot(lambda end_q: end_q, name="end_q_")
@icontract.snapshot(lambda resolution: resolution, name="resolution_")
@icontract.ensure(
    lambda result, OLD: np.allclose(
        result,
        np.sum(
            [
                np.mean(
                    (
                        (stats.norm.ppf(q, loc=OLD.y_pred_, scale=OLD.y_std_) - OLD.y_true_)
                        >= 0
                    ).astype(float)
                    * (stats.norm.ppf(q, loc=OLD.y_pred_, scale=OLD.y_std_) - OLD.y_true_)
                    - q
                    * (stats.norm.ppf(q, loc=OLD.y_pred_, scale=OLD.y_std_) - OLD.y_true_)
                )
                for q in np.linspace(OLD.start_q_, OLD.end_q_, OLD.resolution_)
            ]
        )
        / (OLD.resolution_ if OLD.scaled_ else 1),
        atol=1e-12,
        rtol=1e-8,
    )
)
@icontract.ensure(lambda result: np.isfinite(result))
```
[41]
===== 41 =====
```
     check_score = np.sum(check_list)
 
     if scaled:
-        check_score = check_score / len(check_list)
+        check_score = None
 
-    return check_score+    return check_score
```
```
def check_score(
    y_pred: np.ndarray,
    y_std: np.ndarray,
    y_true: np.ndarray,
    scaled: bool = True,
    start_q: float = 0.01,
    end_q: float = 0.99,
    resolution: int = 99,
) -> float:
    """The negatively oriented check score.

    Computes the negatively oriented check score for held out data (y_true)
    given predictive uncertainty with mean (y_pred) and standard-deviation (y_std).
    Each test point and each quantile is given equal weight in the overall score
    over the test set and list of quantiles.

    The score is computed by scanning over a sequence of quantiles of the predicted
    distributions, starting at (start_q) and ending at (end_q).

    Negatively oriented means a smaller value is more desirable.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        scaled: Whether to scale the score by size of held out set.
        start_q: The lower bound of the quantiles to use for computation.
        end_q: The upper bound of the quantiles to use for computation.
        resolution: The number of quantiles to use for computation.

    Returns:
        The check score.
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)

    test_qs = np.linspace(start_q, end_q, resolution)

    check_list = []
    for q in test_qs:
        q_level = stats.norm.ppf(q, loc=y_pred, scale=y_std)  # pred quantile
        diff = q_level - y_true
        mask = (diff >= 0).astype(float) - q
        score_per_q = np.mean(mask * diff)
        check_list.append(score_per_q)
    check_score = np.sum(check_list)

    if scaled:
        check_score = None

    return check_score

```
