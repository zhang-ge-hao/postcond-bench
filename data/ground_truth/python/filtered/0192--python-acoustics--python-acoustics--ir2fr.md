https://github.com/python-acoustics/python-acoustics/blob/99d79206159b822ea2f4e9d27c8b2fbfeb704d38/./acoustics/signal.py#L287-L314
```
🈚️

No module named 'icontract'

@icontract.ensure(
    lambda ir, fs, N, result: (
        # 计算有效的 N（和正确实现保持一致：N 若为 None 则取 ir.shape[-1]）
        (lambda N_eff:
            # 基于 N_eff 计算 reference 的 fr_raw 和 f_ref
            (lambda fr_raw, f_ref:
                # 再基于 fr_raw 构造“正确”的单边谱 fr_ref
                (lambda fr_ref_even, fr_ref_odd:
                    # 最终检查：实参返回值和参考实现 allclose
                    np.allclose(result[0], f_ref) and
                    np.allclose(
                        result[1],
                        fr_ref_even if N_eff % 2 == 0 else fr_ref_odd
                    )
                )(
                    # N_eff 为偶数时的正确谱：
                    #   DC(i=0) 不翻倍，中间频率(i=1..-2) * 2，Nyquist(i=-1) 不翻倍
                    np.concatenate(
                        [
                            fr_raw[..., 0:1],          # DC
                            fr_raw[..., 1:-1] * 2.0,   # 中间频率 * 2
                            fr_raw[..., -1:]           # Nyquist
                        ],
                        axis=-1
                    ),
                    # N_eff 为奇数时的正确谱：
                    #   DC(i=0) 不翻倍，其余(i=1..end) * 2
                    np.concatenate(
                        [
                            fr_raw[..., 0:1],          # DC
                            fr_raw[..., 1:] * 2.0      # 其它全 * 2
                        ],
                        axis=-1
                    )
                )
            )(
                # fr_raw = rfft(ir, n=N_eff) / N_eff
                rfft(ir, n=N_eff) / N_eff,
                # f_ref = np.fft.rfftfreq(N_eff, 1.0 / fs)
                np.fft.rfftfreq(N_eff, 1.0 / fs)
            )
        )(N if N is not None else ir.shape[-1])
    )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
===== 0 =====
```
     #ir = ir - np.mean(ir) # Remove DC component.
 
     N = N if N else ir.shape[-1]
-    fr = rfft(ir, n=N) / N
+    fr = rfft(ir, n=N)  # Omits the normalization by N, leading to incorrect amplitude
     f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
 
     fr *= 2.0
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N)  # Omits the normalization by N, leading to incorrect amplitude
    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr
```
===== 1 =====
```
     #ir = ir - np.mean(ir) # Remove DC component.
 
     N = N if N else ir.shape[-1]
-    fr = rfft(ir, n=N) / N
+    fr = rfft(ir, n=N) * 2.0  # Incorrectly doubles the result, leading to inflated values
     f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
 
     fr *= 2.0
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) * 2.0  # Incorrectly doubles the result, leading to inflated values
    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr
```
===== 2 =====
```
     #ir = ir - np.mean(ir) # Remove DC component.
 
     N = N if N else ir.shape[-1]
-    fr = rfft(ir, n=N) / N
+    fr = rfft(ir, n=N) * N
     f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
 
     fr *= 2.0
@@ -25,4 +25,4 @@ 
     #f = np.arange(0, N/2+1)*(fs/N)
 
-    return f, fr+    return f, fr
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) * N
    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr

```
===== 3 =====
```
     #ir = ir - np.mean(ir) # Remove DC component.
 
     N = N if N else ir.shape[-1]
-    fr = rfft(ir, n=N) / N
+    fr = rfft(ir, n=N) * N  # Incorrectly scales the result by N instead of dividing
     f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
 
     fr *= 2.0
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) * N  # Incorrectly scales the result by N instead of dividing
    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr
```
===== 4 =====
```
     #ir = ir - np.mean(ir) # Remove DC component.
 
     N = N if N else ir.shape[-1]
-    fr = rfft(ir, n=N) / N
+    fr = rfft(ir, n=N) / (N + 1)  # Introduces an off-by-one error in normalization
     f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
 
     fr *= 2.0
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / (N + 1)  # Introduces an off-by-one error in normalization
    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr
```
===== 5 =====
```
     #ir = ir - np.mean(ir) # Remove DC component.
 
     N = N if N else ir.shape[-1]
-    fr = rfft(ir, n=N) / N
+    fr = rfft(ir, n=N) / (N - 1)  # Incorrectly normalizes by N-1, affecting the output
     f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
 
     fr *= 2.0
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / (N - 1)  # Incorrectly normalizes by N-1, affecting the output
    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr
```
===== 6 =====
```
 
     N = N if N else ir.shape[-1]
     fr = rfft(ir, n=N) / N
-    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
+    f = None  #/ 2.0
 
     fr *= 2.0
     fr[..., 0] /= 2.0  # DC component should not be doubled.
@@ -25,4 +25,4 @@ 
     #f = np.arange(0, N/2+1)*(fs/N)
 
-    return f, fr+    return f, fr
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / N
    f = None  #/ 2.0

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr

```
===== 7 =====
```
 
     N = N if N else ir.shape[-1]
     fr = rfft(ir, n=N) / N
-    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
+    f = np.fft.rfftfreq(N, )  #/ 2.0
 
     fr *= 2.0
     fr[..., 0] /= 2.0  # DC component should not be doubled.
@@ -25,4 +25,4 @@ 
     #f = np.arange(0, N/2+1)*(fs/N)
 
-    return f, fr+    return f, fr
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / N
    f = np.fft.rfftfreq(N, )  #/ 2.0

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr

```
===== 8 =====
```
 
     N = N if N else ir.shape[-1]
     fr = rfft(ir, n=N) / N
-    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
+    f = np.fft.rfftfreq(N, 1.0 * fs)  #/ 2.0
 
     fr *= 2.0
     fr[..., 0] /= 2.0  # DC component should not be doubled.
@@ -25,4 +25,4 @@ 
     #f = np.arange(0, N/2+1)*(fs/N)
 
-    return f, fr+    return f, fr
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / N
    f = np.fft.rfftfreq(N, 1.0 * fs)  #/ 2.0

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr

```
===== 9 =====
```
 
     N = N if N else ir.shape[-1]
     fr = rfft(ir, n=N) / N
-    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
+    f = np.fft.rfftfreq(N, 1.0 / fs) * 0.5  # Incorrectly halves the frequency values
 
     fr *= 2.0
     fr[..., 0] /= 2.0  # DC component should not be doubled.
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / N
    f = np.fft.rfftfreq(N, 1.0 / fs) * 0.5  # Incorrectly halves the frequency values

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr
```
===== 10 =====
```
 
     N = N if N else ir.shape[-1]
     fr = rfft(ir, n=N) / N
-    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
+    f = np.fft.rfftfreq(N, 1.0 / fs) * 2.0  # Incorrectly doubles the frequency values
 
     fr *= 2.0
     fr[..., 0] /= 2.0  # DC component should not be doubled.
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / N
    f = np.fft.rfftfreq(N, 1.0 / fs) * 2.0  # Incorrectly doubles the frequency values

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr
```
===== 11 =====
```
 
     N = N if N else ir.shape[-1]
     fr = rfft(ir, n=N) / N
-    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
+    f = np.fft.rfftfreq(N, 1.0 / fs) ** 2  # Incorrectly squares the frequency values
 
     fr *= 2.0
     fr[..., 0] /= 2.0  # DC component should not be doubled.
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / N
    f = np.fft.rfftfreq(N, 1.0 / fs) ** 2  # Incorrectly squares the frequency values

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr
```
===== 12 =====
```
 
     N = N if N else ir.shape[-1]
     fr = rfft(ir, n=N) / N
-    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
+    f = np.fft.rfftfreq(N, 1.0 / fs) + 1000.0  # Incorrectly shifts the frequency values by 1000 Hz
 
     fr *= 2.0
     fr[..., 0] /= 2.0  # DC component should not be doubled.
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / N
    f = np.fft.rfftfreq(N, 1.0 / fs) + 1000.0  # Incorrectly shifts the frequency values by 1000 Hz

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr
```
===== 13 =====
```
 
     N = N if N else ir.shape[-1]
     fr = rfft(ir, n=N) / N
-    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
+    f = np.fft.rfftfreq(N, 1.0 / fs) - 50.0  # Incorrectly shifts the frequency values down by 50 Hz
 
     fr *= 2.0
     fr[..., 0] /= 2.0  # DC component should not be doubled.
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / N
    f = np.fft.rfftfreq(N, 1.0 / fs) - 50.0  # Incorrectly shifts the frequency values down by 50 Hz

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr
```
===== 14 =====
```
 
     N = N if N else ir.shape[-1]
     fr = rfft(ir, n=N) / N
-    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
+    f = np.fft.rfftfreq(N, 2.0 / fs)  #/ 2.0
 
     fr *= 2.0
     fr[..., 0] /= 2.0  # DC component should not be doubled.
@@ -25,4 +25,4 @@ 
     #f = np.arange(0, N/2+1)*(fs/N)
 
-    return f, fr+    return f, fr
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / N
    f = np.fft.rfftfreq(N, 2.0 / fs)  #/ 2.0

    fr *= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr

```
===== 15 =====
```
     fr = rfft(ir, n=N) / N
     f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
 
-    fr *= 2.0
+    fr *= 3.0
     fr[..., 0] /= 2.0  # DC component should not be doubled.
     if not N % 2:  # if not uneven
         fr[..., -1] /= 2.0  # And neither should fs/2 be.
 
     #f = np.arange(0, N/2+1)*(fs/N)
 
-    return f, fr+    return f, fr
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / N
    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0

    fr *= 3.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr

```
===== 16 =====
```
     fr = rfft(ir, n=N) / N
     f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0
 
-    fr *= 2.0
+    fr /= 2.0
     fr[..., 0] /= 2.0  # DC component should not be doubled.
     if not N % 2:  # if not uneven
         fr[..., -1] /= 2.0  # And neither should fs/2 be.
 
     #f = np.arange(0, N/2+1)*(fs/N)
 
-    return f, fr+    return f, fr
```
```
def ir2fr(ir, fs, N=None):
    """
    Convert impulse response into frequency response. Returns single-sided RMS spectrum.

    :param ir: Impulser response
    :param fs: Sample frequency
    :param N: Blocks

    Calculates the positive frequencies using :func:`np.fft.rfft`.
    Corrections are then applied to obtain the single-sided spectrum.

    .. note:: Single-sided spectrum. Therefore, the amount of bins returned is either N/2 or N/2+1.

    """
    #ir = ir - np.mean(ir) # Remove DC component.

    N = N if N else ir.shape[-1]
    fr = rfft(ir, n=N) / N
    f = np.fft.rfftfreq(N, 1.0 / fs)  #/ 2.0

    fr /= 2.0
    fr[..., 0] /= 2.0  # DC component should not be doubled.
    if not N % 2:  # if not uneven
        fr[..., -1] /= 2.0  # And neither should fs/2 be.

    #f = np.arange(0, N/2+1)*(fs/N)

    return f, fr

```
