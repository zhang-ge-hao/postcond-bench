https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/core_class.py#L612-L632
```
@icontract.snapshot(
    lambda self, rgb, normals:
    self.points[
        ["x", "y", "z"]
        + (["red", "green", "blue"] if rgb else [])
        + (["nx", "ny", "nz"] if normals else [])
    ].values.copy(),
    name="old_pts"
)
@icontract.snapshot(
    lambda self: self.mesh[["v1", "v2", "v3"]].values.copy(),
    name="old_faces"
)
@icontract.ensure(
    lambda OLD, result, rgb, normals, self:
        isinstance(result, tuple) and len(result) == 3
        and
        all(isinstance(v, np.ndarray) for v in result)
        and
        all(v.shape[0] == self.mesh.shape[0] for v in result)
        and
        all(
            v.shape[1] == 3 + (3 if rgb else 0) + (3 if normals else 0)
            for v in result
        )
)
@icontract.ensure(
    lambda OLD, result, rgb, normals, self:
        isinstance(result, tuple) and len(result) == 3
        and
        all(isinstance(v, np.ndarray) for v in result)
        and
        np.array_equal(
            result[0][:, 0:3],
            OLD.old_pts[OLD.old_faces[:, 0], 0:3]
        ) 
        and
        np.array_equal(
            result[1][:, 0:3],
            OLD.old_pts[OLD.old_faces[:, 1], 0:3]
        )
        and
        np.array_equal(
            result[2][:, 0:3],
            OLD.old_pts[OLD.old_faces[:, 2], 0:3]
        )
)
@icontract.ensure(
    lambda OLD, result, rgb, normals, self:
        isinstance(result, tuple) and len(result) == 3
        and
        all(isinstance(v, np.ndarray) for v in result)
        and (
            (not rgb)
            or (
                np.array_equal(
                    result[0][:, 3:6],
                    OLD.old_pts[OLD.old_faces[:, 0], 3:6]
                )
                and np.array_equal(
                    result[1][:, 3:6],
                    OLD.old_pts[OLD.old_faces[:, 1], 3:6]
                )
                and np.array_equal(
                    result[2][:, 3:6],
                    OLD.old_pts[OLD.old_faces[:, 2], 3:6]
                )
            )
        )
)
@icontract.ensure(
    lambda OLD, result, rgb, normals, self:
        isinstance(result, tuple) and len(result) == 3
        and
        all(isinstance(v, np.ndarray) for v in result)
        and (
            (not normals)
            or (
                np.array_equal(
                    result[0][:, 3 + (3 if rgb else 0): 6 + (3 if rgb else 0)],
                    OLD.old_pts[
                        OLD.old_faces[:, 0],
                        3 + (3 if rgb else 0): 6 + (3 if rgb else 0)
                    ]
                )
                and np.array_equal(
                    result[1][:, 3 + (3 if rgb else 0): 6 + (3 if rgb else 0)],
                    OLD.old_pts[
                        OLD.old_faces[:, 1],
                        3 + (3 if rgb else 0): 6 + (3 if rgb else 0)
                    ]
                )
                and np.array_equal(
                    result[2][:, 3 + (3 if rgb else 0): 6 + (3 if rgb else 0)],
                    OLD.old_pts[
                        OLD.old_faces[:, 2],
                        3 + (3 if rgb else 0): 6 + (3 if rgb else 0)
                    ]
                )
            )
        )
)
```
```
@icontract.snapshot(lambda self: {c: (self.points[c].values.copy() if c in self.points.columns else None) for c in ["x", "y", "z", "red", "green", "blue", "nx", "ny", "nz"]}, name="pd")
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 3)
@icontract.ensure(lambda result: result[0] is not None and result[1] is not None and result[2] is not None)
@icontract.ensure(lambda result, self: hasattr(result[0], "shape") and hasattr(result[1], "shape") and hasattr(result[2], "shape") and result[0].shape[0] == self.mesh.shape[0] and result[1].shape[0] == self.mesh.shape[0] and result[2].shape[0] == self.mesh.shape[0])
@icontract.ensure(lambda result, rgb, normals: result[0].shape[1] == (3 + (3 if rgb else 0) + (3 if normals else 0)) and result[1].shape[1] == (3 + (3 if rgb else 0) + (3 if normals else 0)) and result[2].shape[1] == (3 + (3 if rgb else 0) + (3 if normals else 0)))
@icontract.ensure(lambda OLD, result, self: (result[0][:, 0] == OLD.pd["x"][self.mesh["v1"].values]).all() and (result[0][:, 1] == OLD.pd["y"][self.mesh["v1"].values]).all() and (result[0][:, 2] == OLD.pd["z"][self.mesh["v1"].values]).all())
@icontract.ensure(lambda OLD, result, self: (result[1][:, 0] == OLD.pd["x"][self.mesh["v2"].values]).all() and (result[1][:, 1] == OLD.pd["y"][self.mesh["v2"].values]).all() and (result[1][:, 2] == OLD.pd["z"][self.mesh["v2"].values]).all())
@icontract.ensure(lambda OLD, result, self: (result[2][:, 0] == OLD.pd["x"][self.mesh["v3"].values]).all() and (result[2][:, 1] == OLD.pd["y"][self.mesh["v3"].values]).all() and (result[2][:, 2] == OLD.pd["z"][self.mesh["v3"].values]).all())
@icontract.ensure(lambda OLD, result, rgb, self: (not rgb) or ((result[0].shape[1] >= 6) and (result[1].shape[1] >= 6) and (result[2].shape[1] >= 6) and (result[0][:, 3] == OLD.pd["red"][self.mesh["v1"].values]).all() and (result[0][:, 4] == OLD.pd["green"][self.mesh["v1"].values]).all() and (result[0][:, 5] == OLD.pd["blue"][self.mesh["v1"].values]).all() and (result[1][:, 3] == OLD.pd["red"][self.mesh["v2"].values]).all() and (result[1][:, 4] == OLD.pd["green"][self.mesh["v2"].values]).all() and (result[1][:, 5] == OLD.pd["blue"][self.mesh["v2"].values]).all() and (result[2][:, 3] == OLD.pd["red"][self.mesh["v3"].values]).all() and (result[2][:, 4] == OLD.pd["green"][self.mesh["v3"].values]).all() and (result[2][:, 5] == OLD.pd["blue"][self.mesh["v3"].values]).all()))
@icontract.ensure(lambda OLD, result, rgb, normals, self: (not normals) or ( (result[0].shape[1] >= (3 + (3 if rgb else 0) + 3)) and (result[1].shape[1] >= (3 + (3 if rgb else 0) + 3)) and (result[2].shape[1] >= (3 + (3 if rgb else 0) + 3)) and (result[0][:, 3 + (3 if rgb else 0)] == OLD.pd["nx"][self.mesh["v1"].values]).all() and (result[0][:, 4 + (3 if rgb else 0)] == OLD.pd["ny"][self.mesh["v1"].values]).all() and (result[0][:, 5 + (3 if rgb else 0)] == OLD.pd["nz"][self.mesh["v1"].values]).all() and (result[1][:, 3 + (3 if rgb else 0)] == OLD.pd["nx"][self.mesh["v2"].values]).all() and (result[1][:, 4 + (3 if rgb else 0)] == OLD.pd["ny"][self.mesh["v2"].values]).all() and (result[1][:, 5 + (3 if rgb else 0)] == OLD.pd["nz"][self.mesh["v2"].values]).all() and (result[2][:, 3 + (3 if rgb else 0)] == OLD.pd["nx"][self.mesh["v3"].values]).all() and (result[2][:, 4 + (3 if rgb else 0)] == OLD.pd["ny"][self.mesh["v3"].values]).all() and (result[2][:, 5 + (3 if rgb else 0)] == OLD.pd["nz"][self.mesh["v3"].values]).all() ))
```
[9, 10, 11]
===== 9 =====
```
 
         points = self.points[use_columns].values
 
-        v1 = points[self.mesh["v1"].values]
+        v1 = None
         v2 = points[self.mesh["v2"].values]
         v3 = points[self.mesh["v3"].values]
 
-        return v1, v2, v3+        return v1, v2, v3
```
```
    def get_mesh_vertices(self, rgb=False, normals=False):
        """Decompose triangles of self.mesh from vertices in self.points.

        Returns
        -------
        v1, v2, v3: ndarray
            (N, 3) arrays of vertices so v1[i], v2[i], v3[i] represent the ith triangle
        """
        use_columns = ["x", "y", "z"]
        if rgb:
            use_columns.extend(["red", "green", "blue"])
        if normals:
            use_columns.extend(["nx", "ny", "nz"])

        points = self.points[use_columns].values

        v1 = None
        v2 = points[self.mesh["v2"].values]
        v3 = points[self.mesh["v3"].values]

        return v1, v2, v3

```
===== 10 =====
```
         points = self.points[use_columns].values
 
         v1 = points[self.mesh["v1"].values]
-        v2 = points[self.mesh["v2"].values]
+        v2 = None
         v3 = points[self.mesh["v3"].values]
 
-        return v1, v2, v3+        return v1, v2, v3
```
```
    def get_mesh_vertices(self, rgb=False, normals=False):
        """Decompose triangles of self.mesh from vertices in self.points.

        Returns
        -------
        v1, v2, v3: ndarray
            (N, 3) arrays of vertices so v1[i], v2[i], v3[i] represent the ith triangle
        """
        use_columns = ["x", "y", "z"]
        if rgb:
            use_columns.extend(["red", "green", "blue"])
        if normals:
            use_columns.extend(["nx", "ny", "nz"])

        points = self.points[use_columns].values

        v1 = points[self.mesh["v1"].values]
        v2 = None
        v3 = points[self.mesh["v3"].values]

        return v1, v2, v3

```
===== 11 =====
```
 
         v1 = points[self.mesh["v1"].values]
         v2 = points[self.mesh["v2"].values]
-        v3 = points[self.mesh["v3"].values]
+        v3 = None
 
-        return v1, v2, v3+        return v1, v2, v3
```
```
    def get_mesh_vertices(self, rgb=False, normals=False):
        """Decompose triangles of self.mesh from vertices in self.points.

        Returns
        -------
        v1, v2, v3: ndarray
            (N, 3) arrays of vertices so v1[i], v2[i], v3[i] represent the ith triangle
        """
        use_columns = ["x", "y", "z"]
        if rgb:
            use_columns.extend(["red", "green", "blue"])
        if normals:
            use_columns.extend(["nx", "ny", "nz"])

        points = self.points[use_columns].values

        v1 = points[self.mesh["v1"].values]
        v2 = points[self.mesh["v2"].values]
        v3 = None

        return v1, v2, v3

```
