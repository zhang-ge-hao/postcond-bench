https://github.com/python-acoustics/python-acoustics/blob/99d79206159b822ea2f4e9d27c8b2fbfeb704d38/./acoustics/generator.py#L173-L192
```
🈚️

No module named 'icontract'

@icontract.ensure(lambda result: True)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
===== 0 =====
```
     """
     state = np.random.RandomState() if state is None else state
     uneven = N % 2
-    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
+    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven) + 1  # Adding a constant offset
     S = (np.arange(len(X)))  # Filter
     y = (irfft(X * S)).real
     if uneven:
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven) + 1  # Adding a constant offset
    S = (np.arange(len(X)))  # Filter
    y = (irfft(X * S)).real
    if uneven:
        y = y[:-1]
    return normalize(y)
```
===== 1 =====
```
     """
     state = np.random.RandomState() if state is None else state
     uneven = N % 2
-    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
+    X = state.randn(N // 2 + 1 + uneven) + 1j / state.randn(N // 2 + 1 + uneven)
     S = (np.arange(len(X)))  # Filter
     y = (irfft(X * S)).real
     if uneven:
         y = y[:-1]
-    return normalize(y)+    return normalize(y)
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2 + 1 + uneven) + 1j / state.randn(N // 2 + 1 + uneven)
    S = (np.arange(len(X)))  # Filter
    y = (irfft(X * S)).real
    if uneven:
        y = y[:-1]
    return normalize(y)

```
===== 2 =====
```
     """
     state = np.random.RandomState() if state is None else state
     uneven = N % 2
-    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
+    X = state.randn(N // 2) + 1j * state.randn(N // 2)  # Incorrect size for X
     S = (np.arange(len(X)))  # Filter
     y = (irfft(X * S)).real
     if uneven:
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2) + 1j * state.randn(N // 2)  # Incorrect size for X
    S = (np.arange(len(X)))  # Filter
    y = (irfft(X * S)).real
    if uneven:
        y = y[:-1]
    return normalize(y)
```
===== 3 =====
```
     state = np.random.RandomState() if state is None else state
     uneven = N % 2
     X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
-    S = (np.arange(len(X)))  # Filter
+    S = (np.arange(len(X)) ** 2)  # Filter, distorts the frequency response
     y = (irfft(X * S)).real
     if uneven:
         y = y[:-1]
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
    S = (np.arange(len(X)) ** 2)  # Filter, distorts the frequency response
    y = (irfft(X * S)).real
    if uneven:
        y = y[:-1]
    return normalize(y)
```
===== 4 =====
```
     state = np.random.RandomState() if state is None else state
     uneven = N % 2
     X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
-    S = (np.arange(len(X)))  # Filter
+    S = np.ones(len(X))  # Filter, removes frequency variation entirely
     y = (irfft(X * S)).real
     if uneven:
         y = y[:-1]
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
    S = np.ones(len(X))  # Filter, removes frequency variation entirely
    y = (irfft(X * S)).real
    if uneven:
        y = y[:-1]
    return normalize(y)
```
===== 5 =====
```
     uneven = N % 2
     X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
     S = (np.arange(len(X)))  # Filter
-    y = (irfft(X * S)).real
+    y = (irfft(X * S)).imag  # Incorrectly takes the imaginary part instead of the real part
     if uneven:
         y = y[:-1]
     return normalize(y)
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
    S = (np.arange(len(X)))  # Filter
    y = (irfft(X * S)).imag  # Incorrectly takes the imaginary part instead of the real part
    if uneven:
        y = y[:-1]
    return normalize(y)
```
===== 6 =====
```
     uneven = N % 2
     X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
     S = (np.arange(len(X)))  # Filter
-    y = (irfft(X * S)).real
+    y = (irfft(X * S)).real[:N//2]  # Incorrectly slices the output, losing half of the samples
     if uneven:
         y = y[:-1]
     return normalize(y)
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
    S = (np.arange(len(X)))  # Filter
    y = (irfft(X * S)).real[:N//2]  # Incorrectly slices the output, losing half of the samples
    if uneven:
        y = y[:-1]
    return normalize(y)
```
===== 7 =====
```
     uneven = N % 2
     X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
     S = (np.arange(len(X)))  # Filter
-    y = (irfft(X * S)).real
+    y = (irfft(X / S)).real
     if uneven:
         y = y[:-1]
-    return normalize(y)+    return normalize(y)
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
    S = (np.arange(len(X)))  # Filter
    y = (irfft(X / S)).real
    if uneven:
        y = y[:-1]
    return normalize(y)

```
===== 8 =====
```
     X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
     S = (np.arange(len(X)))  # Filter
     y = (irfft(X * S)).real
-    if uneven:
+    if not uneven:
         y = y[:-1]
     return normalize(y)
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
    S = (np.arange(len(X)))  # Filter
    y = (irfft(X * S)).real
    if not uneven:
        y = y[:-1]
    return normalize(y)
```
===== 9 =====
```
     X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
     S = (np.arange(len(X)))  # Filter
     y = (irfft(X * S)).real
-    if uneven:
+    if uneven == 0:
         y = y[:-1]
     return normalize(y)
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
    S = (np.arange(len(X)))  # Filter
    y = (irfft(X * S)).real
    if uneven == 0:
        y = y[:-1]
    return normalize(y)
```
===== 10 =====
```
     S = (np.arange(len(X)))  # Filter
     y = (irfft(X * S)).real
     if uneven:
-        y = y[:-1]
-    return normalize(y)+        y = y[:+1]
+    return normalize(y)
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
    S = (np.arange(len(X)))  # Filter
    y = (irfft(X * S)).real
    if uneven:
        y = y[:+1]
    return normalize(y)

```
===== 11 =====
```
     S = (np.arange(len(X)))  # Filter
     y = (irfft(X * S)).real
     if uneven:
-        y = y[:-1]
-    return normalize(y)+        y = y[:-2]
+    return normalize(y)
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
    S = (np.arange(len(X)))  # Filter
    y = (irfft(X * S)).real
    if uneven:
        y = y[:-2]
    return normalize(y)

```
===== 12 =====
```
     y = (irfft(X * S)).real
     if uneven:
         y = y[:-1]
-    return normalize(y)+    return np.zeros_like(y)  # Returns an array of zeros instead of the generated noise.
```
```
def violet(N, state=None):
    """
    Violet noise. Power increases with 6 dB per octave.

    :param N: Amount of samples.
    :param state: State of PRNG.
    :type state: :class:`np.random.RandomState`

    Power increases with +9 dB per octave.
    Power density increases with +6 dB per octave.

    """
    state = np.random.RandomState() if state is None else state
    uneven = N % 2
    X = state.randn(N // 2 + 1 + uneven) + 1j * state.randn(N // 2 + 1 + uneven)
    S = (np.arange(len(X)))  # Filter
    y = (irfft(X * S)).real
    if uneven:
        y = y[:-1]
    return np.zeros_like(y)  # Returns an array of zeros instead of the generated noise.
```
