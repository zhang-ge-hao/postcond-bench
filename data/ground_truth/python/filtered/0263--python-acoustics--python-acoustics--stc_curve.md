https://github.com/python-acoustics/python-acoustics/blob/99d79206159b822ea2f4e9d27c8b2fbfeb704d38/./acoustics/building.py#L63-L82
```
🈚️

E   ModuleNotFoundError: No module named 'icontract'

@icontract.ensure(
    lambda result, tl: (
        # 1. 标准 STC 参考曲线（125 Hz - 4 kHz）
        (ref_curve := np.array(
            [0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20],
            dtype=float
        )),
        # 2. 搜索的平移量范围（dB），范围可以按需调整
        (offsets := np.arange(-200, 201, dtype=float)),
        # 3. 所有候选曲线：每个 offset 对应一条曲线
        (curves := ref_curve[None, :] + offsets[:, None]),
        # 4. 计算每条候选曲线相对于 tl 的偏差
        (diff := tl[None, :] - curves),
        # 5. 只保留负偏差（正偏差记为 0）
        (residuals := np.minimum(diff, 0.0)),
        # 6. 每个候选曲线的总负偏差和 & 最小负偏差
        (sum_res := residuals.sum(axis=1)),
        (min_res := residuals.min(axis=1)),
        # 7. 选出满足标准条件的所有 offset
        (mask := (sum_res >= -32.0) & (min_res >= -8.0)),
        # 8. 取满足条件的最大 offset 作为“正确曲线”的平移量
        (best_offset := offsets[mask][-1]),
        (correct_curve := ref_curve + best_offset),
        # 9. 要求函数返回值与“正确曲线”完全一致
        bool(np.array_equal(result, correct_curve))
    )[-1]
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
===== 0 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 10, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 10, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 1 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 21])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 21])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 2 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 21, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 21, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 3 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 21, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 21, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 4 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 21, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 21, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 5 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 21, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 21, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 6 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 21, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 21, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 7 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 20, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 20, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 8 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 19, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 19, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 9 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 18, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 18, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 10 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 17, 17, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 17, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 11 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 18, 19, 20, 21, 22, 23, 23, 23, 23, 0])  # Reset last value to zero
     top_curve = ref_curve
     res_sum = 0
     while True:
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 18, 19, 20, 21, 22, 23, 23, 23, 23, 0])  # Reset last value to zero
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 12 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 18, 19, 20, 21, 22, 23, 23, 23, 23, 22])  # Decreased last values
     top_curve = ref_curve
     res_sum = 0
     while True:
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 18, 19, 20, 21, 22, 23, 23, 23, 23, 22])  # Decreased last values
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 13 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 18, 19, 20, 21, 22, 23, 23, 23, 23, 24])  # Increased last value
     top_curve = ref_curve
     res_sum = 0
     while True:
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 18, 19, 20, 21, 22, 23, 23, 23, 23, 24])  # Increased last value
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 14 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 18, 19, 20, 21, 22, 23, 23, 23, 23, 30])  # Outlier value
     top_curve = ref_curve
     res_sum = 0
     while True:
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 18, 19, 20, 21, 22, 23, 23, 23, 23, 30])  # Outlier value
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 15 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27])  # Incorrect values
     top_curve = ref_curve
     res_sum = 0
     while True:
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27])  # Incorrect values
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 16 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 12, 16, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 16, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 17 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 6, 9, 13, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 13, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 18 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 3, 7, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 7, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 19 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([0, 4, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 4, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 20 =====
```
 
     :param tl: Transmission Loss
     """
-    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
+    ref_curve = np.array([1, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
     while True:
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([1, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 21 =====
```
     ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
-    while True:
+    for _ in range(10):
         diff = tl - top_curve
         residuals = np.clip(diff, np.min(diff), 0)
         res_sum = np.sum(residuals)
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    for _ in range(10):
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 22 =====
```
     ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
-    while True:
+    while False:
         diff = tl - top_curve
         residuals = np.clip(diff, np.min(diff), 0)
         res_sum = np.sum(residuals)
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while False:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 23 =====
```
     ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
-    while True:
+    while False:
         diff = tl - top_curve
         residuals = np.clip(diff, np.min(diff), 0)
         res_sum = np.sum(residuals)
@@ -17,4 +17,4 @@                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while False:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 24 =====
```
     ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
-    while True:
+    while True and res_sum < -32:
         diff = tl - top_curve
         residuals = np.clip(diff, np.min(diff), 0)
         res_sum = np.sum(residuals)
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True and res_sum < -32:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 25 =====
```
     ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
     top_curve = ref_curve
     res_sum = 0
-    while True:
+    while res_sum < -32:
         diff = tl - top_curve
         residuals = np.clip(diff, np.min(diff), 0)
         res_sum = np.sum(residuals)
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while res_sum < -32:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 26 =====
```
     res_sum = 0
     while True:
         diff = tl - top_curve
-        residuals = np.clip(diff, np.min(diff), 0)
+        residuals = np.clip(diff, 0, np.max(diff))
         res_sum = np.sum(residuals)
         if res_sum < -32:
             if np.any(residuals > -8):
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, 0, np.max(diff))
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 27 =====
```
     res_sum = 0
     while True:
         diff = tl - top_curve
-        residuals = np.clip(diff, np.min(diff), 0)
+        residuals = np.clip(diff, np.min(diff), None)
         res_sum = np.sum(residuals)
         if res_sum < -32:
             if np.any(residuals > -8):
                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), None)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 28 =====
```
     while True:
         diff = tl - top_curve
         residuals = np.clip(diff, np.min(diff), 0)
-        res_sum = np.sum(residuals)
+        res_sum = np.sum(residuals) + 10
         if res_sum < -32:
             if np.any(residuals > -8):
                 top_curve -= 1
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals) + 10
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 29 =====
```
     while True:
         diff = tl - top_curve
         residuals = np.clip(diff, np.min(diff), 0)
-        res_sum = np.sum(residuals)
+        res_sum = np.sum(residuals) / 2
         if res_sum < -32:
             if np.any(residuals > -8):
                 top_curve -= 1
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals) / 2
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 30 =====
```
         diff = tl - top_curve
         residuals = np.clip(diff, np.min(diff), 0)
         res_sum = np.sum(residuals)
-        if res_sum < -32:
+        if res_sum < +32:
             if np.any(residuals > -8):
                 top_curve -= 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < +32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve

```
===== 31 =====
```
         diff = tl - top_curve
         residuals = np.clip(diff, np.min(diff), 0)
         res_sum = np.sum(residuals)
-        if res_sum < -32:
+        if res_sum < -16:
             if np.any(residuals > -8):
                 top_curve -= 1
                 break
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -16:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 32 =====
```
         diff = tl - top_curve
         residuals = np.clip(diff, np.min(diff), 0)
         res_sum = np.sum(residuals)
-        if res_sum < -32:
+        if res_sum < -64:
             if np.any(residuals > -8):
                 top_curve -= 1
                 break
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -64:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 33 =====
```
         diff = tl - top_curve
         residuals = np.clip(diff, np.min(diff), 0)
         res_sum = np.sum(residuals)
-        if res_sum < -32:
+        if res_sum == 0:
             if np.any(residuals > -8):
                 top_curve -= 1
                 break
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum == 0:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 34 =====
```
         diff = tl - top_curve
         residuals = np.clip(diff, np.min(diff), 0)
         res_sum = np.sum(residuals)
-        if res_sum < -32:
+        if res_sum >= -32:
             if np.any(residuals > -8):
                 top_curve -= 1
                 break
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum >= -32:
            if np.any(residuals > -8):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 35 =====
```
         residuals = np.clip(diff, np.min(diff), 0)
         res_sum = np.sum(residuals)
         if res_sum < -32:
-            if np.any(residuals > -8):
+            if np.all(residuals < -32):
                 top_curve -= 1
                 break
         top_curve += 1
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.all(residuals < -32):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 36 =====
```
         residuals = np.clip(diff, np.min(diff), 0)
         res_sum = np.sum(residuals)
         if res_sum < -32:
-            if np.any(residuals > -8):
+            if np.any(residuals < -10):
                 top_curve -= 1
                 break
         top_curve += 1
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals < -10):
                top_curve -= 1
                break
        top_curve += 1
    return top_curve
```
===== 37 =====
```
         res_sum = np.sum(residuals)
         if res_sum < -32:
             if np.any(residuals > -8):
-                top_curve -= 1
+                top_curve += 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve += 1
                break
        top_curve += 1
    return top_curve

```
===== 38 =====
```
         res_sum = np.sum(residuals)
         if res_sum < -32:
             if np.any(residuals > -8):
-                top_curve -= 1
+                top_curve -= 2
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 2
                break
        top_curve += 1
    return top_curve

```
===== 39 =====
```
         res_sum = np.sum(residuals)
         if res_sum < -32:
             if np.any(residuals > -8):
-                top_curve -= 1
+                top_curve = 1
                 break
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve = 1
                break
        top_curve += 1
    return top_curve

```
===== 40 =====
```
         if res_sum < -32:
             if np.any(residuals > -8):
                 top_curve -= 1
-                break
+                return
         top_curve += 1
-    return top_curve+    return top_curve
```
```
def stc_curve(tl):
    """
    Calculate the Sound Transmission Class (STC) curve from a NumPy array `tl`
    with third octave data between 125 Hz and 4 kHz.

    :param tl: Transmission Loss
    """
    ref_curve = np.array([0, 3, 6, 9, 12, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20])
    top_curve = ref_curve
    res_sum = 0
    while True:
        diff = tl - top_curve
        residuals = np.clip(diff, np.min(diff), 0)
        res_sum = np.sum(residuals)
        if res_sum < -32:
            if np.any(residuals > -8):
                top_curve -= 1
                return
        top_curve += 1
    return top_curve

```
