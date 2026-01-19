https://github.com/python-acoustics/python-acoustics/blob/99d79206159b822ea2f4e9d27c8b2fbfeb704d38/./acoustics/standards/iso_1996_2_2007.py#L280-L302
```
🈚️

No icontract

@icontract.ensure(
    lambda self, result: result is self,
    "Tonality._determine_tones 必须返回 self（可链式调用）",
)
@icontract.ensure(
    # 每个 noise_pause 上的 tone 必须和
    # determine_tone_lines(...) 的“正确调用”结果一致
    lambda self, result:
        all(
            (
                # 情况 1：理论上没有 tone → pause.tone 必须是 None
                (
                    not bool(
                        np.any(
                            determine_tone_lines(
                                self.spectrum,
                                self.frequency_resolution,
                                noise_pause.start,
                                noise_pause.end,
                                self.force_tone_without_pause,
                                self.force_bandwidth_criterion,
                            )[0]
                        )
                    )
                    and noise_pause.tone is None
                )
                or
                # 情况 2：理论上有 tone → 必须创建 Tone，且参数一致
                (
                    bool(
                        np.any(
                            determine_tone_lines(
                                self.spectrum,
                                self.frequency_resolution,
                                noise_pause.start,
                                noise_pause.end,
                                self.force_tone_without_pause,
                                self.force_bandwidth_criterion,
                            )[0]
                        )
                    )
                    and (noise_pause.tone is not None)
                    and isinstance(noise_pause.tone, Tone)
                    # Tone 必须挂在当前的 noise_pause 上
                    and (noise_pause.tone.noise_pause is noise_pause)
                    # tone._tone_lines 必须等于 determine_tone_lines 的索引结果
                    and np.array_equal(
                        noise_pause.tone._tone_lines,
                        determine_tone_lines(
                            self.spectrum,
                            self.frequency_resolution,
                            noise_pause.start,
                            noise_pause.end,
                            self.force_tone_without_pause,
                            self.force_bandwidth_criterion,
                        )[0],
                    )
                    # 带宽不能是 None 且必须相等
                    and (
                        determine_tone_lines(
                            self.spectrum,
                            self.frequency_resolution,
                            noise_pause.start,
                            noise_pause.end,
                            self.force_tone_without_pause,
                            self.force_bandwidth_criterion,
                        )[1]
                        is not None
                    )
                    and (noise_pause.tone.bandwidth_3db is not None)
                    and math.isclose(
                        float(noise_pause.tone.bandwidth_3db),
                        float(
                            determine_tone_lines(
                                self.spectrum,
                                self.frequency_resolution,
                                noise_pause.start,
                                noise_pause.end,
                                self.force_tone_without_pause,
                                self.force_bandwidth_criterion,
                            )[1]
                        ),
                        rel_tol=1e-9,
                        abs_tol=1e-9,
                    )
                    # center 必须是 tone 行中最大值所在的频率（与 create_tone 保持一致）
                    and (
                        noise_pause.tone.center
                        == self.spectrum.iloc[noise_pause.tone._tone_lines].idxmax()
                    )
                )
            )
            for noise_pause in self.noise_pauses
        ),
    "每个 NoisePause 的 tone 必须与正确参数调用 determine_tone_lines 的结果一致",
)
@icontract.ensure(
    # Tone 对象自身必须“健康”：索引范围、落在 pause 内等
    lambda self, result:
        all(
            (noise_pause.tone is None)
            or (
                len(noise_pause.tone._tone_lines) > 0
                # 索引必须在谱的范围内
                and np.all(noise_pause.tone._tone_lines >= 0)
                and np.all(noise_pause.tone._tone_lines < len(self.spectrum))
                # 同时落在对应 noise_pause 的 [start, end] 内
                and np.all(noise_pause.tone._tone_lines >= noise_pause.start)
                and np.all(noise_pause.tone._tone_lines <= noise_pause.end)
            )
            for noise_pause in self.noise_pauses
        ),
    "所有 Tone 的频率行索引必须非空、在谱范围内且落在对应的 noise pause 里",
)
@icontract.ensure(
    # 从 self.tones 迭代出来的 Tone 必须能回到各自的 noise_pause 上
    lambda self, result:
        all(
            (tone is not None) and (tone.noise_pause.tone is tone)
            for tone in self.tones
        ),
    "通过 self.tones 得到的每个 Tone 必须与其 NoisePause.tone 一一对应",
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7]
===== 0 =====
```
             # Determine the indices of the tones in a noise pause
             tone_indices, bandwidth_for_tone_criterion = determine_tone_lines(
                 levels,
-                self.frequency_resolution,
                 noise_pause.start,
                 noise_pause.end,
                 self.force_tone_without_pause,
@@ -20,4 +19,4 @@                 # ...then we create a tone object.
                 noise_pause.tone = create_tone(levels, tone_indices, bandwidth_for_tone_criterion,
                                                weakref.proxy(noise_pause))
-        return self+        return self
```
```
    def _determine_tones(self):
        """Analyse the noise pauses for tones. The determined tones are available via :attr:`tones`.
        Per frequency line results are available via :attr:`line_classifier`.
        """
        levels = self.spectrum

        # First we need to check for the tones.
        for noise_pause in self.noise_pauses:
            # Determine the indices of the tones in a noise pause
            tone_indices, bandwidth_for_tone_criterion = determine_tone_lines(
                levels,
                noise_pause.start,
                noise_pause.end,
                self.force_tone_without_pause,
                self.force_bandwidth_criterion,
            )
            # If we have indices, ...
            if np.any(tone_indices):
                # ...then we create a tone object.
                noise_pause.tone = create_tone(levels, tone_indices, bandwidth_for_tone_criterion,
                                               weakref.proxy(noise_pause))
        return self

```
===== 1 =====
```
             tone_indices, bandwidth_for_tone_criterion = determine_tone_lines(
                 levels,
                 self.frequency_resolution,
-                noise_pause.start,
+                noise_pause.end,
                 noise_pause.end,
                 self.force_tone_without_pause,
                 self.force_bandwidth_criterion,
```
```
    def _determine_tones(self):
        """Analyse the noise pauses for tones. The determined tones are available via :attr:`tones`.
        Per frequency line results are available via :attr:`line_classifier`.
        """
        levels = self.spectrum

        # First we need to check for the tones.
        for noise_pause in self.noise_pauses:
            # Determine the indices of the tones in a noise pause
            tone_indices, bandwidth_for_tone_criterion = determine_tone_lines(
                levels,
                self.frequency_resolution,
                noise_pause.end,
                noise_pause.end,
                self.force_tone_without_pause,
                self.force_bandwidth_criterion,
            )
            # If we have indices, ...
            if np.any(tone_indices):
                # ...then we create a tone object.
                noise_pause.tone = create_tone(levels, tone_indices, bandwidth_for_tone_criterion,
                                               weakref.proxy(noise_pause))
        return self
```
===== 2 =====
```
             tone_indices, bandwidth_for_tone_criterion = determine_tone_lines(
                 levels,
                 self.frequency_resolution,
-                noise_pause.start,
                 noise_pause.end,
                 self.force_tone_without_pause,
                 self.force_bandwidth_criterion,
@@ -20,4 +19,4 @@                 # ...then we create a tone object.
                 noise_pause.tone = create_tone(levels, tone_indices, bandwidth_for_tone_criterion,
                                                weakref.proxy(noise_pause))
-        return self+        return self
```
```
    def _determine_tones(self):
        """Analyse the noise pauses for tones. The determined tones are available via :attr:`tones`.
        Per frequency line results are available via :attr:`line_classifier`.
        """
        levels = self.spectrum

        # First we need to check for the tones.
        for noise_pause in self.noise_pauses:
            # Determine the indices of the tones in a noise pause
            tone_indices, bandwidth_for_tone_criterion = determine_tone_lines(
                levels,
                self.frequency_resolution,
                noise_pause.end,
                self.force_tone_without_pause,
                self.force_bandwidth_criterion,
            )
            # If we have indices, ...
            if np.any(tone_indices):
                # ...then we create a tone object.
                noise_pause.tone = create_tone(levels, tone_indices, bandwidth_for_tone_criterion,
                                               weakref.proxy(noise_pause))
        return self

```
===== 3 =====
```
                 levels,
                 self.frequency_resolution,
                 noise_pause.start,
-                noise_pause.end,
+                noise_pause.start,
                 self.force_tone_without_pause,
                 self.force_bandwidth_criterion,
             )
```
```
    def _determine_tones(self):
        """Analyse the noise pauses for tones. The determined tones are available via :attr:`tones`.
        Per frequency line results are available via :attr:`line_classifier`.
        """
        levels = self.spectrum

        # First we need to check for the tones.
        for noise_pause in self.noise_pauses:
            # Determine the indices of the tones in a noise pause
            tone_indices, bandwidth_for_tone_criterion = determine_tone_lines(
                levels,
                self.frequency_resolution,
                noise_pause.start,
                noise_pause.start,
                self.force_tone_without_pause,
                self.force_bandwidth_criterion,
            )
            # If we have indices, ...
            if np.any(tone_indices):
                # ...then we create a tone object.
                noise_pause.tone = create_tone(levels, tone_indices, bandwidth_for_tone_criterion,
                                               weakref.proxy(noise_pause))
        return self
```
===== 4 =====
```
                 levels,
                 self.frequency_resolution,
                 noise_pause.start,
-                noise_pause.end,
                 self.force_tone_without_pause,
                 self.force_bandwidth_criterion,
             )
@@ -20,4 +19,4 @@                 # ...then we create a tone object.
                 noise_pause.tone = create_tone(levels, tone_indices, bandwidth_for_tone_criterion,
                                                weakref.proxy(noise_pause))
-        return self+        return self
```
```
    def _determine_tones(self):
        """Analyse the noise pauses for tones. The determined tones are available via :attr:`tones`.
        Per frequency line results are available via :attr:`line_classifier`.
        """
        levels = self.spectrum

        # First we need to check for the tones.
        for noise_pause in self.noise_pauses:
            # Determine the indices of the tones in a noise pause
            tone_indices, bandwidth_for_tone_criterion = determine_tone_lines(
                levels,
                self.frequency_resolution,
                noise_pause.start,
                self.force_tone_without_pause,
                self.force_bandwidth_criterion,
            )
            # If we have indices, ...
            if np.any(tone_indices):
                # ...then we create a tone object.
                noise_pause.tone = create_tone(levels, tone_indices, bandwidth_for_tone_criterion,
                                               weakref.proxy(noise_pause))
        return self

```
===== 5 =====
```
                 self.force_bandwidth_criterion,
             )
             # If we have indices, ...
-            if np.any(tone_indices):
+            if np.any(None):
                 # ...then we create a tone object.
                 noise_pause.tone = create_tone(levels, tone_indices, bandwidth_for_tone_criterion,
                                                weakref.proxy(noise_pause))
-        return self+        return self
```
```
    def _determine_tones(self):
        """Analyse the noise pauses for tones. The determined tones are available via :attr:`tones`.
        Per frequency line results are available via :attr:`line_classifier`.
        """
        levels = self.spectrum

        # First we need to check for the tones.
        for noise_pause in self.noise_pauses:
            # Determine the indices of the tones in a noise pause
            tone_indices, bandwidth_for_tone_criterion = determine_tone_lines(
                levels,
                self.frequency_resolution,
                noise_pause.start,
                noise_pause.end,
                self.force_tone_without_pause,
                self.force_bandwidth_criterion,
            )
            # If we have indices, ...
            if np.any(None):
                # ...then we create a tone object.
                noise_pause.tone = create_tone(levels, tone_indices, bandwidth_for_tone_criterion,
                                               weakref.proxy(noise_pause))
        return self

```
===== 6 =====
```
             # If we have indices, ...
             if np.any(tone_indices):
                 # ...then we create a tone object.
-                noise_pause.tone = create_tone(levels, tone_indices, bandwidth_for_tone_criterion,
-                                               weakref.proxy(noise_pause))
-        return self+                noise_pause.tone = None
+        return self
```
```
    def _determine_tones(self):
        """Analyse the noise pauses for tones. The determined tones are available via :attr:`tones`.
        Per frequency line results are available via :attr:`line_classifier`.
        """
        levels = self.spectrum

        # First we need to check for the tones.
        for noise_pause in self.noise_pauses:
            # Determine the indices of the tones in a noise pause
            tone_indices, bandwidth_for_tone_criterion = determine_tone_lines(
                levels,
                self.frequency_resolution,
                noise_pause.start,
                noise_pause.end,
                self.force_tone_without_pause,
                self.force_bandwidth_criterion,
            )
            # If we have indices, ...
            if np.any(tone_indices):
                # ...then we create a tone object.
                noise_pause.tone = None
        return self

```
===== 7 =====
```
             # If we have indices, ...
             if np.any(tone_indices):
                 # ...then we create a tone object.
-                noise_pause.tone = create_tone(levels, tone_indices, bandwidth_for_tone_criterion,
+                noise_pause.tone = create_tone(levels, tone_indices, None,
                                                weakref.proxy(noise_pause))
-        return self+        return self
```
```
    def _determine_tones(self):
        """Analyse the noise pauses for tones. The determined tones are available via :attr:`tones`.
        Per frequency line results are available via :attr:`line_classifier`.
        """
        levels = self.spectrum

        # First we need to check for the tones.
        for noise_pause in self.noise_pauses:
            # Determine the indices of the tones in a noise pause
            tone_indices, bandwidth_for_tone_criterion = determine_tone_lines(
                levels,
                self.frequency_resolution,
                noise_pause.start,
                noise_pause.end,
                self.force_tone_without_pause,
                self.force_bandwidth_criterion,
            )
            # If we have indices, ...
            if np.any(tone_indices):
                # ...then we create a tone object.
                noise_pause.tone = create_tone(levels, tone_indices, None,
                                               weakref.proxy(noise_pause))
        return self

```
