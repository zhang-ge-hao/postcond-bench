https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/structures/voxelgrid.py#L18-L66
```
@icontract.ensure(lambda self, colors: self.colors is colors)
@icontract.ensure(lambda self: isinstance(self.x_y_z, np.ndarray))
@icontract.ensure(lambda self: self.x_y_z.shape == (3,))
@icontract.ensure(lambda self, n_x, n_y, n_z: np.array_equal(self.x_y_z, [n_x, n_y, n_z]))
@icontract.ensure(lambda self: isinstance(self.sizes, np.ndarray))
@icontract.ensure(lambda self: self.sizes.shape == (3,))
@icontract.ensure(lambda self, size_x, size_y, size_z: np.array_equal(self.sizes, [size_x, size_y, size_z]))
@icontract.ensure(lambda self, regular_bounding_box: self.regular_bounding_box == regular_bounding_box)
@icontract.ensure(lambda self: self.id is None)
@icontract.ensure(lambda self: self.xyzmin is None and self.xyzmax is None)
@icontract.ensure(lambda self: self.segments is None)
@icontract.ensure(lambda self: self.shape is None)
@icontract.ensure(lambda self: self.n_voxels is None)
@icontract.ensure(lambda self: self.voxel_x is None and self.voxel_y is None and self.voxel_z is None)
@icontract.ensure(lambda self: self.voxel_n is None)
@icontract.ensure(lambda self: self.voxel_centers is None)
@icontract.ensure(lambda self: self.voxel_colors is None)
```
```
missing attribute validation

crossfile context miss

_points is defined in the other file

https://github.com/daavoo/pyntcloud/blob/main/src/pyntcloud/structures/base.py#L4
```
passed
```
@icontract.snapshot(lambda points: points, name="points")
@icontract.snapshot(lambda colors: colors, name="colors")
@icontract.snapshot(lambda n_x, n_y, n_z: (n_x, n_y, n_z), name="xyz")
@icontract.snapshot(lambda size_x, size_y, size_z: (size_x, size_y, size_z), name="sizes")
@icontract.snapshot(lambda regular_bounding_box: regular_bounding_box, name="regular")
@icontract.ensure(lambda OLD, self: self._points is OLD.points)
@icontract.ensure(lambda OLD, self: self.colors is OLD.colors)
@icontract.ensure(
    lambda OLD, self: hasattr(self, "x_y_z")
    and tuple(np.asarray(self.x_y_z).shape) == (3,)
    and np.asarray(self.x_y_z).dtype.kind in ("i", "u")
    and tuple(np.asarray(self.x_y_z).tolist()) == tuple(OLD.xyz)
)
@icontract.ensure(
    lambda OLD, self: hasattr(self, "sizes")
    and tuple(np.asarray(self.sizes).shape) == (3,)
    and tuple(np.asarray(self.sizes).tolist()) == tuple(OLD.sizes)
)
@icontract.ensure(lambda OLD, self: self.regular_bounding_box == OLD.regular)
@icontract.ensure(
    lambda OLD, self: getattr(self, "id", None) is None
    and getattr(self, "xyzmin", None) is None
    and getattr(self, "xyzmax", None) is None
    and getattr(self, "segments", None) is None
    and getattr(self, "shape", None) is None
    and getattr(self, "n_voxels", None) is None
    and getattr(self, "voxel_x", None) is None
    and getattr(self, "voxel_y", None) is None
    and getattr(self, "voxel_z", None) is None
    and getattr(self, "voxel_n", None) is None
    and getattr(self, "voxel_centers", None) is None
    and getattr(self, "voxel_colors", None) is None
)
```
===== 1: failed =====
```
             If True, the bounding box of the point cloud will be adjusted
             in order to have all the dimensions of equal length.
         """
-        super().__init__(points=points)
+        super().__init__(points=None)
         self.colors = colors
         self.x_y_z = np.asarray([n_x, n_y, n_z])
         self.sizes = np.asarray([size_x, size_y, size_z])
@@ -46,4 +46,4 @@         self.voxel_x, self.voxel_y, self.voxel_z = None, None, None
         self.voxel_n = None
         self.voxel_centers = None
-        self.voxel_colors = None+        self.voxel_colors = None
```
```
    def __init__(
        self,
        *,
        points,
        colors=None,
        n_x=1,
        n_y=1,
        n_z=1,
        size_x=None,
        size_y=None,
        size_z=None,
        regular_bounding_box=True,
    ):
        """Grid of voxels with support for different build methods.

        Parameters
        ----------
        points: (N, 3) numpy.array
        colors: (N, 3) numpy.array, optional
            Default None.
            If not None, color for each voxel will be computed.
        n_x, n_y, n_z :  int, optional
            Default: 1
            The number of segments in which each axis will be divided.
            Ignored if corresponding size_x, size_y or size_z is not None.
        size_x, size_y, size_z : float, optional
            Default: None
            The desired voxel size along each axis.
            If not None, the corresponding n_x, n_y or n_z will be ignored.
        regular_bounding_box : bool, optional
            Default: True
            If True, the bounding box of the point cloud will be adjusted
            in order to have all the dimensions of equal length.
        """
        super().__init__(points=None)
        self.colors = colors
        self.x_y_z = np.asarray([n_x, n_y, n_z])
        self.sizes = np.asarray([size_x, size_y, size_z])
        self.regular_bounding_box = regular_bounding_box

        self.id = None
        self.xyzmin, self.xyzmax = None, None
        self.segments = None
        self.shape = None
        self.n_voxels = None
        self.voxel_x, self.voxel_y, self.voxel_z = None, None, None
        self.voxel_n = None
        self.voxel_centers = None
        self.voxel_colors = None

```
