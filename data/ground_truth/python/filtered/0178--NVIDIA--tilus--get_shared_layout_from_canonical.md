https://github.com/NVIDIA/tilus/blob/b6f2649da6444afa776c0b5882f7f3bfdc3efe93/./python/tilus/ir/layout/cuda/tcgen05/smem.py#L264-L316
```
🈚️

It's hard

@icontract.ensure(
    lambda result, canonical_layout: (
        # 1. 还原 cute swizzle 相关参数
        (cute_swizzle := as_cute_swizzle(canonical_layout.swizzle_mode)) is not None
        and (bbits := cute_swizzle.bbits) is not None
        and (mbase := cute_swizzle.mbase) is not None
        and (sshift := cute_swizzle.sshift) is not None
        # 2. 展开 CanonicalSharedLayout 的字段
        and (T := canonical_layout.T) is not None
        and (m := canonical_layout.m) is not None
        and (k := canonical_layout.k) is not None
        and (SBO := canonical_layout.SBO) is not None
        and (LBO := canonical_layout.LBO) is not None
        # 3. 根据 bbits 计算 swizzle 因子
        and (S := 2 ** bbits) is not None
        # 4. 按原函数逻辑重建 cute layout（区分 major_kind 和 swizzle_mode）
        and (
            layout := (
                # major_kind == "MN"
                cute_layout(
                    shape=((T, m), (8, k)),
                    strides=((1, SBO), (T, LBO)),
                )
                if canonical_layout.major_kind == "MN"
                and canonical_layout.swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE
                else cute_layout(
                    shape=((T, S, m), (8, k)),
                    strides=((1, T, LBO), (S * T, SBO)),
                )
                if canonical_layout.major_kind == "MN"
                # major_kind == "K"
                else cute_layout(
                    shape=((8, m), (T, k)),
                    strides=((T, SBO), (1, LBO)),
                )
                if canonical_layout.swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE
                else cute_layout(
                    shape=((8, m), (T, S, k)),
                    strides=((S * T, SBO), (1, T, LBO)),
                )
            )
        )
        # 5. 按原函数逻辑重建 shared memory 的 shape
        and (
            smem_shape := (
                [int(layout.shape)]
                if not isinstance(layout.shape, Sequence)
                else [int(tuple_product(item)) for item in layout.shape]
            )
        ) is not None
        # 6. 用“正确实现”的逻辑构造一个期望的 SharedLayout
        and (
            expected := SharedLayout.create(
                shape=smem_shape,
                size=prod(smem_shape),
                f_offset=(
                    lambda axes,
                           bbits=bbits,
                           mbase=mbase,
                           sshift=sshift,
                           T=T,
                           layout=layout: CuteSwizzle(
                               bbits=bbits,
                               mbase=mbase - floor_log2(16 // T),
                               sshift=sshift,
                           )(layout(*axes))
                ),
            )
        ) is not None
        # 7. 比较 result 与 expected 的各个字段
        and result.shape == expected.shape
        and result.size == expected.size
        and result.offset == expected.offset
    )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]
===== 0 =====
```
         The shared memory layout of Tilus corresponding to the canonical layout.
     """
     swizzle_mode = canonical_layout.swizzle_mode
-    cute_swizzle = as_cute_swizzle(swizzle_mode)
+    cute_swizzle = as_cute_swizzle(Tcgen05SwizzleMode.NO_SWIZZLE)
     bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
     T, m, k, SBO, LBO = (
         canonical_layout.T,
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(Tcgen05SwizzleMode.NO_SWIZZLE)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 1 =====
```
     )
 
     # Determine swizzle factor based on bbits (from the canonical layout table)
-    S = 2**bbits
+    S = 3**bbits
 
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 3**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 2 =====
```
     S = 2**bbits
 
     # Calculate the logical shape based on cute layout interpretation and major-ness
-    if canonical_layout.major_kind == "MN":
+    if canonical_layout.T > 1:  # Incorrectly checks for T instead of major kind
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
         else:
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.T > 1:  # Incorrectly checks for T instead of major kind
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 3 =====
```
 
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
-        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
+        if swizzle_mode != Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode != Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 4 =====
```
 
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
-        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
+        if swizzle_mode != Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode != Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 5 =====
```
 
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
-        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
+        if swizzle_mode == Tcgen05SwizzleMode.B128_SWIZZLE:
             layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.B128_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 6 =====
```
 
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
-        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
+        if swizzle_mode == Tcgen05SwizzleMode.B32_SWIZZLE:
             layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.B32_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 7 =====
```
 
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
-        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
+        if swizzle_mode == Tcgen05SwizzleMode.B64_SWIZZLE:
             layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.B64_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 8 =====
```
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
+            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, LBO), (T, SBO)))
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, LBO), (T, SBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 9 =====
```
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
+            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (1, 1)))
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (1, 1)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 10 =====
```
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
+            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (1, LBO)))
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 11 =====
```
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
+            layout = cute_layout(shape=((T, m), (8, k)), strides=((2, SBO), (T, LBO)))
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((2, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 12 =====
```
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
+            layout = cute_layout(shape=((T, m), (8, k)), strides=((SBO, 1), (T, LBO)))
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((SBO, 1), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 13 =====
```
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
+            layout = cute_layout(shape=((T, m), (8, k)), strides=((T, SBO), (1, LBO)))
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 14 =====
```
     # Calculate the logical shape based on cute layout interpretation and major-ness
     if canonical_layout.major_kind == "MN":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
+            layout = cute_layout(shape=((T, m), (9, k)), strides=((1, SBO), (T, LBO)))
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (9, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 15 =====
```
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
         else:
-            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
+            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (1, SBO)))
     elif canonical_layout.major_kind == "K":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (1, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 16 =====
```
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
         else:
-            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
+            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S / T, SBO)))
     elif canonical_layout.major_kind == "K":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S / T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 17 =====
```
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
         else:
-            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
+            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, SBO), (S * T, LBO)))
     elif canonical_layout.major_kind == "K":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, SBO), (S * T, LBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 18 =====
```
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
         else:
-            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
+            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((2, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((2, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 19 =====
```
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
         else:
-            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
+            layout = cute_layout(shape=((T, S, m), (9, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (9, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 20 =====
```
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
-        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
+        if swizzle_mode != Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
         else:
             layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode != Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 21 =====
```
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
-        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
+        if swizzle_mode != Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
         else:
             layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode != Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 22 =====
```
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
-        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
+        if swizzle_mode == Tcgen05SwizzleMode.B32_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
         else:
             layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.B32_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 23 =====
```
         else:
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
-        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
+        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE or swizzle_mode == Tcgen05SwizzleMode.B32_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
         else:
             layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE or swizzle_mode == Tcgen05SwizzleMode.B32_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 24 =====
```
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
+            layout = cute_layout(shape=((8, m), (T, k)), strides=((1, LBO), (T, SBO)))
         else:
             layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
     else:
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((1, LBO), (T, SBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 25 =====
```
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
+            layout = cute_layout(shape=((8, m), (T, k)), strides=((1, SBO), (T, LBO)))
         else:
             layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
     else:
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 26 =====
```
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
+            layout = cute_layout(shape=((8, m), (T, k)), strides=((SBO, 1), (1, LBO)))
         else:
             layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
     else:
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((SBO, 1), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 27 =====
```
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
+            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, LBO), (T, SBO)))
         else:
             layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
     else:
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, LBO), (T, SBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 28 =====
```
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
+            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (2, LBO)))
         else:
             layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
     else:
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (2, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 29 =====
```
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
+            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (SBO, LBO)))
         else:
             layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
     else:
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (SBO, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 30 =====
```
             layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
     elif canonical_layout.major_kind == "K":
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
-            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
+            layout = cute_layout(shape=((9, m), (T, k)), strides=((T, SBO), (1, LBO)))
         else:
             layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
     else:
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((9, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 31 =====
```
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
         else:
-            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
+            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (2, T, LBO)))
     else:
         raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")
 
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (2, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 32 =====
```
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
         else:
-            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
+            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S / T, SBO), (1, T, LBO)))
     else:
         raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")
 
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S / T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 33 =====
```
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
         else:
-            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
+            layout = cute_layout(shape=((8, m), (T, k, S)), strides=((S * T, LBO), (1, T, SBO)))
     else:
         raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, k, S)), strides=((S * T, LBO), (1, T, SBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 34 =====
```
         if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
             layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
         else:
-            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
+            layout = cute_layout(shape=((9, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
     else:
         raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")
 
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((9, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 35 =====
```
 
     def f_offset(axes: Sequence[Var]) -> Expr | int:
         nbytes = 16 // canonical_layout.T
-        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
+        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase + floor_log2(nbytes), sshift=sshift)
         return swizzle(layout(*axes))
 
     if not isinstance(layout.shape, Sequence):
@@ -50,4 +50,4 @@     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase + floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)

```
===== 36 =====
```
 
     def f_offset(axes: Sequence[Var]) -> Expr | int:
         nbytes = 16 // canonical_layout.T
-        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
+        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase + floor_log2(nbytes), sshift=sshift)  # Incorrectly adds instead of subtracting
         return swizzle(layout(*axes))
 
     if not isinstance(layout.shape, Sequence):
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase + floor_log2(nbytes), sshift=sshift)  # Incorrectly adds instead of subtracting
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 37 =====
```
 
     def f_offset(axes: Sequence[Var]) -> Expr | int:
         nbytes = 16 // canonical_layout.T
-        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
+        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - 1, sshift=sshift)  # Incorrectly decrements mbase by 1
         return swizzle(layout(*axes))
 
     if not isinstance(layout.shape, Sequence):
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - 1, sshift=sshift)  # Incorrectly decrements mbase by 1
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 38 =====
```
 
     def f_offset(axes: Sequence[Var]) -> Expr | int:
         nbytes = 16 // canonical_layout.T
-        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
+        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes) * 2, sshift=sshift)  # Incorrectly multiplies the adjustment by 2
         return swizzle(layout(*axes))
 
     if not isinstance(layout.shape, Sequence):
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes) * 2, sshift=sshift)  # Incorrectly multiplies the adjustment by 2
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 39 =====
```
 
     def f_offset(axes: Sequence[Var]) -> Expr | int:
         nbytes = 16 // canonical_layout.T
-        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
+        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes) + 1, sshift=sshift)  # Incorrectly adds 1 to the adjustment
         return swizzle(layout(*axes))
 
     if not isinstance(layout.shape, Sequence):
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes) + 1, sshift=sshift)  # Incorrectly adds 1 to the adjustment
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 40 =====
```
 
     def f_offset(axes: Sequence[Var]) -> Expr | int:
         nbytes = 16 // canonical_layout.T
-        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
+        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase, sshift=sshift)  # Omits the mbase adjustment entirely
         return swizzle(layout(*axes))
 
     if not isinstance(layout.shape, Sequence):
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase, sshift=sshift)  # Omits the mbase adjustment entirely
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 41 =====
```
     def f_offset(axes: Sequence[Var]) -> Expr | int:
         nbytes = 16 // canonical_layout.T
         swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
-        return swizzle(layout(*axes))
+        return layout(*axes)  # Missing swizzle operation, leading to incorrect layout calculation.
 
     if not isinstance(layout.shape, Sequence):
         smem_shape = [int(layout.shape)]
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return layout(*axes)  # Missing swizzle operation, leading to incorrect layout calculation.

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 42 =====
```
     def f_offset(axes: Sequence[Var]) -> Expr | int:
         nbytes = 16 // canonical_layout.T
         swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
-        return swizzle(layout(*axes))
+        return layout(*axes) + swizzle(0)  # Incorrectly adds a constant to the layout, leading to incorrect results.
 
     if not isinstance(layout.shape, Sequence):
         smem_shape = [int(layout.shape)]
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return layout(*axes) + swizzle(0)  # Incorrectly adds a constant to the layout, leading to incorrect results.

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 43 =====
```
     def f_offset(axes: Sequence[Var]) -> Expr | int:
         nbytes = 16 // canonical_layout.T
         swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
-        return swizzle(layout(*axes))
+        return swizzle(layout(*axes) * 2)  # Incorrectly scales the layout, leading to incorrect memory access patterns.
 
     if not isinstance(layout.shape, Sequence):
         smem_shape = [int(layout.shape)]
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes) * 2)  # Incorrectly scales the layout, leading to incorrect memory access patterns.

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 44 =====
```
     def f_offset(axes: Sequence[Var]) -> Expr | int:
         nbytes = 16 // canonical_layout.T
         swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
-        return swizzle(layout(*axes))
+        return swizzle(layout(*axes) + 1)  # Incorrectly modifies the layout by adding 1, causing an offset error.
 
     if not isinstance(layout.shape, Sequence):
         smem_shape = [int(layout.shape)]
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes) + 1)  # Incorrectly modifies the layout by adding 1, causing an offset error.

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 45 =====
```
     def f_offset(axes: Sequence[Var]) -> Expr | int:
         nbytes = 16 // canonical_layout.T
         swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
-        return swizzle(layout(*axes))
+        return swizzle(layout(*axes) - 1)  # Incorrectly modifies the layout by subtracting 1, causing an offset error.
 
     if not isinstance(layout.shape, Sequence):
         smem_shape = [int(layout.shape)]
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes) - 1)  # Incorrectly modifies the layout by subtracting 1, causing an offset error.

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)
```
===== 46 =====
```
     else:
         smem_shape = [int(tuple_product(item)) for item in layout.shape]
 
-    return SharedLayout.create(shape=smem_shape, size=prod(smem_shape), f_offset=f_offset)+    return SharedLayout.create(shape=smem_shape[::-1], size=prod(smem_shape), f_offset=f_offset)  # Reversed shape
```
```
def get_shared_layout_from_canonical(canonical_layout: CanonicalSharedLayout) -> SharedLayout:
    """
    Construct the shared layout specified by the canonical layout of tcgen05 cp instructions.

    Parameters
    ----------
    canonical_layout : CanonicalSharedLayout
        The canonical layout to construct the shared layout from.

    Returns
    -------
    ret: SharedLayout
        The shared memory layout of Tilus corresponding to the canonical layout.
    """
    swizzle_mode = canonical_layout.swizzle_mode
    cute_swizzle = as_cute_swizzle(swizzle_mode)
    bbits, mbase, sshift = cute_swizzle.bbits, cute_swizzle.mbase, cute_swizzle.sshift
    T, m, k, SBO, LBO = (
        canonical_layout.T,
        canonical_layout.m,
        canonical_layout.k,
        canonical_layout.SBO,
        canonical_layout.LBO,
    )

    # Determine swizzle factor based on bbits (from the canonical layout table)
    S = 2**bbits

    # Calculate the logical shape based on cute layout interpretation and major-ness
    if canonical_layout.major_kind == "MN":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((T, m), (8, k)), strides=((1, SBO), (T, LBO)))
        else:
            layout = cute_layout(shape=((T, S, m), (8, k)), strides=((1, T, LBO), (S * T, SBO)))
    elif canonical_layout.major_kind == "K":
        if swizzle_mode == Tcgen05SwizzleMode.NO_SWIZZLE:
            layout = cute_layout(shape=((8, m), (T, k)), strides=((T, SBO), (1, LBO)))
        else:
            layout = cute_layout(shape=((8, m), (T, S, k)), strides=((S * T, SBO), (1, T, LBO)))
    else:
        raise ValueError(f"Unsupported major_kind: {canonical_layout.major_kind}")

    def f_offset(axes: Sequence[Var]) -> Expr | int:
        nbytes = 16 // canonical_layout.T
        swizzle = CuteSwizzle(bbits=bbits, mbase=mbase - floor_log2(nbytes), sshift=sshift)
        return swizzle(layout(*axes))

    if not isinstance(layout.shape, Sequence):
        smem_shape = [int(layout.shape)]
    else:
        smem_shape = [int(tuple_product(item)) for item in layout.shape]

    return SharedLayout.create(shape=smem_shape[::-1], size=prod(smem_shape), f_offset=f_offset)  # Reversed shape
```
