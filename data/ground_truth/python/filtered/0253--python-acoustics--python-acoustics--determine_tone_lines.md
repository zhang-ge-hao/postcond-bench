https://github.com/python-acoustics/python-acoustics/blob/99d79206159b822ea2f4e9d27c8b2fbfeb704d38/./acoustics/standards/iso_1996_2_2007.py#L631-L673
```
🈚️

E   ModuleNotFoundError: No module named 'icontract'

@icontract.ensure(
    lambda result, levels, df, start, end,
           force_tone_without_pause=False,
           force_bandwidth_criterion=False: (
        (
            # 噪声暂停区间
            (npr := slice(start, end + 1)),
            # 用整数索引的 levels
            (levels_int := levels.reset_index(drop=True)),
            # 是否存在“6 dB above”的潜在 tone（或强制）
            (cond_tone := np.any(
                (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
                (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])
            ) or force_tone_without_pause),
            # 期望返回值初始化
            (expected_tone_indices := np.array([])),
            (expected_bw := None),
            # 根据“正确版本”逻辑计算期望的 (tone_indices, bandwidth_3db)
            (_tmp := (
                (expected_tone_indices, expected_bw)  # 如果没有 tone，保持默认
                if not cond_tone
                else (
                    # -3 dB 带宽内的索引
                    (indices_3db := (
                        levels.iloc[npr]
                        >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB
                    ).to_numpy().nonzero()[0]),
                    # 带宽（Hz）
                    (bw := (indices_3db.max() - indices_3db.min()) * df),
                    # tone 中心频率
                    (tone_center_frequency := levels.iloc[npr].idxmax()),
                    # 临界带宽
                    (_cb := critical_band(tone_center_frequency)),
                    (cb_bw := _cb[3]),
                    # 是否满足带宽判据
                    (cond_bw := (bw < 0.10 * cb_bw) or force_bandwidth_criterion),
                    # 满足带宽判据才算 tone
                    (
                        (np.array([]), None)
                        if not cond_bw
                        else (
                            # 所有在 max 之下 6 dB 以内的 line 都是 tone
                            (tone_indices2 := levels_int.iloc[npr][
                                levels_int.iloc[npr]
                                >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB
                            ].index.values),
                            (tone_indices2, bw)
                        )[-1]
                    )
                )[-1]
            )),
            # 解包期望结果
            (expected_tone_indices := _tmp[0]),
            (expected_bw := _tmp[1]),
            # 解包被测函数的返回结果
            (_res := result),
            (tone_indices := _res[0]),
            (bandwidth_for_tone_criterion := _res[1]),
        ),
        # 对比：索引必须完全一致
        np.array_equal(tone_indices, expected_tone_indices) and (
            # 带宽都是 None
            (expected_bw is None and bandwidth_for_tone_criterion is None)
            # 或带宽数值上近似相等
            or (
                expected_bw is not None
                and np.isclose(
                    bandwidth_for_tone_criterion,
                    expected_bw,
                    rtol=1e-10,
                    atol=1e-12,
                )
            )
        )
    )[-1]
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
===== 0 =====
```
 
     # Levels but with integeres as indices instead of frequencies.
     # Benefit over np.array is that the index is maintained when the object is sliced.
-    levels_int = levels.reset_index(drop=True)
+    levels_int = levels.copy()  # This creates a copy but does not reset the index, causing potential index misalignment.
 
     # If any of the lines is six 6 dB above. See section C.4.3.
     if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.copy()  # This creates a copy but does not reset the index, causing potential index misalignment.

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = (levels_int.iloc[npr][
                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values

    return tone_indices, bandwidth_for_tone_criterion
```
===== 1 =====
```
 
     # Levels but with integeres as indices instead of frequencies.
     # Benefit over np.array is that the index is maintained when the object is sliced.
-    levels_int = levels.reset_index(drop=True)
+    levels_int = levels.iloc[npr]  # This will not reset the index, leading to incorrect indexing.
 
     # If any of the lines is six 6 dB above. See section C.4.3.
     if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.iloc[npr]  # This will not reset the index, leading to incorrect indexing.

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = (levels_int.iloc[npr][
                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values

    return tone_indices, bandwidth_for_tone_criterion
```
===== 2 =====
```
 
     # Levels but with integeres as indices instead of frequencies.
     # Benefit over np.array is that the index is maintained when the object is sliced.
-    levels_int = levels.reset_index(drop=True)
+    levels_int = levels.reset_index(drop=True).iloc[npr]  # This applies slicing after resetting the index, which may lead to incorrect tone indices.
 
     # If any of the lines is six 6 dB above. See section C.4.3.
     if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.reset_index(drop=True).iloc[npr]  # This applies slicing after resetting the index, which may lead to incorrect tone indices.

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = (levels_int.iloc[npr][
                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values

    return tone_indices, bandwidth_for_tone_criterion
```
===== 3 =====
```
     levels_int = levels.reset_index(drop=True)
 
     # If any of the lines is six 6 dB above. See section C.4.3.
-    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
+    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB - levels.iloc[start - 1]) &
               (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:
 
         # Indices of values that are within -3 dB point.
@@ -40,4 +40,4 @@             tone_indices = (levels_int.iloc[npr][
                 levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values
 
-    return tone_indices, bandwidth_for_tone_criterion+    return tone_indices, bandwidth_for_tone_criterion
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.reset_index(drop=True)

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB - levels.iloc[start - 1]) &
              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = (levels_int.iloc[npr][
                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values

    return tone_indices, bandwidth_for_tone_criterion

```
===== 4 =====
```
     levels_int = levels.reset_index(drop=True)
 
     # If any of the lines is six 6 dB above. See section C.4.3.
-    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
-              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:
+    if np.any(None) or force_tone_without_pause:
 
         # Indices of values that are within -3 dB point.
         indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
@@ -40,4 +39,4 @@             tone_indices = (levels_int.iloc[npr][
                 levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values
 
-    return tone_indices, bandwidth_for_tone_criterion+    return tone_indices, bandwidth_for_tone_criterion
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.reset_index(drop=True)

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any(None) or force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = (levels_int.iloc[npr][
                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values

    return tone_indices, bandwidth_for_tone_criterion

```
===== 5 =====
```
 
     # If any of the lines is six 6 dB above. See section C.4.3.
     if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
-              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:
+              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) and force_tone_without_pause:
 
         # Indices of values that are within -3 dB point.
         indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
@@ -40,4 +40,4 @@             tone_indices = (levels_int.iloc[npr][
                 levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values
 
-    return tone_indices, bandwidth_for_tone_criterion+    return tone_indices, bandwidth_for_tone_criterion
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.reset_index(drop=True)

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) and force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = (levels_int.iloc[npr][
                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values

    return tone_indices, bandwidth_for_tone_criterion

```
===== 6 =====
```
 
     # If any of the lines is six 6 dB above. See section C.4.3.
     if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
-              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:
+              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB - levels.iloc[end + 1])) or force_tone_without_pause:
 
         # Indices of values that are within -3 dB point.
         indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
@@ -40,4 +40,4 @@             tone_indices = (levels_int.iloc[npr][
                 levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values
 
-    return tone_indices, bandwidth_for_tone_criterion+    return tone_indices, bandwidth_for_tone_criterion
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.reset_index(drop=True)

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB - levels.iloc[end + 1])) or force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = (levels_int.iloc[npr][
                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values

    return tone_indices, bandwidth_for_tone_criterion

```
===== 7 =====
```
         _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)
 
         # Fullfill bandwidth criterion? See section C.4.3
-        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
+        if (bandwidth_for_tone_criterion < 0.05 * critical_band_bandwidth) and force_bandwidth_criterion:
             # All values within 6 decibel are designated as tones.
             tone_indices = (levels_int.iloc[npr][
                 levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.reset_index(drop=True)

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion < 0.05 * critical_band_bandwidth) and force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = (levels_int.iloc[npr][
                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values

    return tone_indices, bandwidth_for_tone_criterion
```
===== 8 =====
```
         _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)
 
         # Fullfill bandwidth criterion? See section C.4.3
-        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
+        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) and force_bandwidth_criterion:
             # All values within 6 decibel are designated as tones.
             tone_indices = (levels_int.iloc[npr][
                 levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values
 
-    return tone_indices, bandwidth_for_tone_criterion+    return tone_indices, bandwidth_for_tone_criterion
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.reset_index(drop=True)

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) and force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = (levels_int.iloc[npr][
                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values

    return tone_indices, bandwidth_for_tone_criterion

```
===== 9 =====
```
         _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)
 
         # Fullfill bandwidth criterion? See section C.4.3
-        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
+        if (bandwidth_for_tone_criterion == 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
             # All values within 6 decibel are designated as tones.
             tone_indices = (levels_int.iloc[npr][
                 levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.reset_index(drop=True)

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion == 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = (levels_int.iloc[npr][
                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values

    return tone_indices, bandwidth_for_tone_criterion
```
===== 10 =====
```
         _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)
 
         # Fullfill bandwidth criterion? See section C.4.3
-        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
+        if (bandwidth_for_tone_criterion > 0.10 * critical_band_bandwidth) and not force_bandwidth_criterion:
             # All values within 6 decibel are designated as tones.
             tone_indices = (levels_int.iloc[npr][
                 levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.reset_index(drop=True)

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion > 0.10 * critical_band_bandwidth) and not force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = (levels_int.iloc[npr][
                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values

    return tone_indices, bandwidth_for_tone_criterion
```
===== 11 =====
```
         # Fullfill bandwidth criterion? See section C.4.3
         if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
             # All values within 6 decibel are designated as tones.
-            tone_indices = (levels_int.iloc[npr][
-                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values
+            tone_indices = None
 
-    return tone_indices, bandwidth_for_tone_criterion+    return tone_indices, bandwidth_for_tone_criterion
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.reset_index(drop=True)

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = None

    return tone_indices, bandwidth_for_tone_criterion

```
===== 12 =====
```
         if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
             # All values within 6 decibel are designated as tones.
             tone_indices = (levels_int.iloc[npr][
-                levels_int.iloc[npr] >= levels_int.iloc[npr].max() - TONE_LINES_CRITERION_DB]).index.values
+                levels_int.iloc[npr] >= levels_int.iloc[npr].max() + TONE_LINES_CRITERION_DB]).index.values
 
-    return tone_indices, bandwidth_for_tone_criterion+    return tone_indices, bandwidth_for_tone_criterion
```
```
def determine_tone_lines(levels, df, start, end, force_tone_without_pause=False, force_bandwidth_criterion=False):
    """Determine tone lines in noise pause.

    :param levels: Series with levels as function of frequency.
    :param df: Frequency resolution.
    :param start: Index of noise pause start.
    :param end: Index of noise pause end.

    :returns: Array with indices of tone lines in noise pause.

    """
    # Noise pause range object
    npr = slice(start, end + 1)

    # Return values
    tone_indices = np.array([])
    bandwidth_for_tone_criterion = None

    # Levels but with integeres as indices instead of frequencies.
    # Benefit over np.array is that the index is maintained when the object is sliced.
    levels_int = levels.reset_index(drop=True)

    # If any of the lines is six 6 dB above. See section C.4.3.
    if np.any((levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[start - 1]) &
              (levels.iloc[npr] >= TONE_WITHIN_PAUSE_CRITERION_DB + levels.iloc[end + 1])) or force_tone_without_pause:

        # Indices of values that are within -3 dB point.
        indices_3db = (levels.iloc[npr] >= levels.iloc[npr].max() - TONE_BANDWIDTH_CRITERION_DB).to_numpy().nonzero()[0]
        # -3 dB bandwidth
        bandwidth_for_tone_criterion = (indices_3db.max() - indices_3db.min()) * df
        # Frequency of tone.
        tone_center_frequency = levels.iloc[npr].idxmax()
        #tone_center_index = levels.reset_index(drop=True).iloc[npr].idxmax()
        # Critical band
        _, _, _, critical_band_bandwidth = critical_band(tone_center_frequency)

        # Fullfill bandwidth criterion? See section C.4.3
        if (bandwidth_for_tone_criterion < 0.10 * critical_band_bandwidth) or force_bandwidth_criterion:
            # All values within 6 decibel are designated as tones.
            tone_indices = (levels_int.iloc[npr][
                levels_int.iloc[npr] >= levels_int.iloc[npr].max() + TONE_LINES_CRITERION_DB]).index.values

    return tone_indices, bandwidth_for_tone_criterion

```
