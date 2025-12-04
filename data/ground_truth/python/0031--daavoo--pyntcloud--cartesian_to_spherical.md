https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/geometry/coord_systems.py#L46-L80
```
@icontract.snapshot(lambda xyz: xyz.copy(), name="xyz")
@icontract.ensure(
    lambda OLD, result, degrees:
        isinstance(result, tuple)
        and len(result) == 3
        and all(r is not None for r in result)
        and all(isinstance(r, np.ndarray) for r in result)
        and result[0].ndim == result[1].ndim == result[2].ndim == 1
        and result[0].shape == result[1].shape == result[2].shape == (OLD.xyz.shape[0],)
        and np.allclose(
            result[0],
            np.nan_to_num(
                np.sqrt(
                    OLD.xyz[:, 0] ** 2
                    + OLD.xyz[:, 1] ** 2
                    + OLD.xyz[:, 2] ** 2
                )
            )
        )
        and (
            (not degrees and np.allclose(
                result[1],
                np.nan_to_num(np.arccos(OLD.xyz[:, 2] / result[0]))
            ))
            or
            (degrees and np.allclose(
                result[1],
                np.rad2deg(
                    np.nan_to_num(np.arccos(OLD.xyz[:, 2] / result[0]))
                )
            ))
        )
        and (
            (not degrees and np.allclose(
                result[2],
                np.nan_to_num(np.arctan2(OLD.xyz[:, 1], OLD.xyz[:, 0]))
            ))
            or
            (degrees and np.allclose(
                result[2],
                np.rad2deg(
                    np.nan_to_num(np.arctan2(OLD.xyz[:, 1], OLD.xyz[:, 0]))
                )
            ))
        )
        and np.all(result[1] >= 0)
        and np.all(result[1] <= (180 if degrees else np.pi))
        and (
            (~(
                (OLD.xyz[:, 0] == 0)
                & (OLD.xyz[:, 1] == 0)
                & (OLD.xyz[:, 2] > 0)
            )).all()
            or np.allclose(
                result[1][
                    (OLD.xyz[:, 0] == 0)
                    & (OLD.xyz[:, 1] == 0)
                    & (OLD.xyz[:, 2] > 0)
                ],
                0
            )
        )
        and (
            (~(
                (OLD.xyz[:, 0] == 0)
                & (OLD.xyz[:, 1] == 0)
                & (OLD.xyz[:, 2] < 0)
            )).all()
            or np.allclose(
                result[1][
                    (OLD.xyz[:, 0] == 0)
                    & (OLD.xyz[:, 1] == 0)
                    & (OLD.xyz[:, 2] < 0)
                ],
                (180 if degrees else np.pi)
            )
        )
        and (
            (~(
                (OLD.xyz[:, 0] > 0)
                & (OLD.xyz[:, 1] == 0)
            )).all()
            or np.allclose(
                result[2][
                    (OLD.xyz[:, 0] > 0)
                    & (OLD.xyz[:, 1] == 0)
                ],
                0
            )
        )
        and (
            (~(
                (OLD.xyz[:, 0] == 0)
                & (OLD.xyz[:, 1] > 0)
            )).all()
            or np.allclose(
                result[2][
                    (OLD.xyz[:, 0] == 0)
                    & (OLD.xyz[:, 1] > 0)
                ],
                (90 if degrees else (np.pi / 2.0))
            )
        )
        and (
            (~(
                (OLD.xyz[:, 0] < 0)
                & (OLD.xyz[:, 1] == 0)
            )).all()
            or np.allclose(
                result[2][
                    (OLD.xyz[:, 0] < 0)
                    & (OLD.xyz[:, 1] == 0)
                ],
                (180 if degrees else np.pi)
            )
        )
        and (
            (~(
                (OLD.xyz[:, 0] == 0)
                & (OLD.xyz[:, 1] < 0)
            )).all()
            or np.allclose(
                result[2][
                    (OLD.xyz[:, 0] == 0)
                    & (OLD.xyz[:, 1] < 0)
                ],
                (-90 if degrees else (-np.pi / 2.0))
            )
        ),
)
```
```
@icontract.snapshot(lambda xyz: xyz.copy(), name="xyz")
@icontract.ensure(lambda OLD, result: result[0].shape == (OLD.xyz.shape[0],) and result[1].shape == result[0].shape and result[2].shape == result[0].shape)
@icontract.ensure(lambda OLD, result: np.allclose(result[0], np.nan_to_num(np.sqrt(OLD.xyz[:, 0]**2 + OLD.xyz[:, 1]**2 + OLD.xyz[:, 2]**2))))
@icontract.ensure(lambda OLD, result, degrees: (not degrees and np.allclose(result[1], np.nan_to_num(np.arccos(OLD.xyz[:, 2] / result[0])))) or (degrees and np.allclose(result[1], np.rad2deg(np.nan_to_num(np.arccos(OLD.xyz[:, 2] / result[0]))))))
@icontract.ensure(lambda OLD, result, degrees: (not degrees and np.allclose(result[2], np.nan_to_num(np.arctan2(OLD.xyz[:, 1], OLD.xyz[:, 0])))) or (degrees and np.allclose(result[2], np.rad2deg(np.nan_to_num(np.arctan2(OLD.xyz[:, 1], OLD.xyz[:, 0]))))))
@icontract.ensure(lambda result: (result[1] is not None) and (result[2] is not None))
@icontract.ensure(lambda result, degrees: np.all(result[1] >= 0) and np.all(result[1] <= (180 if degrees else np.pi)))
@icontract.ensure(lambda OLD, result, degrees: (~((OLD.xyz[:,0]==0)&(OLD.xyz[:,1]==0)&(OLD.xyz[:,2]>0))).all() or np.allclose(result[1][(OLD.xyz[:,0]==0)&(OLD.xyz[:,1]==0)&(OLD.xyz[:,2]>0)], 0))
@icontract.ensure(lambda OLD, result, degrees: (~((OLD.xyz[:,0]==0)&(OLD.xyz[:,1]==0)&(OLD.xyz[:,2]<0))).all() or np.allclose(result[1][(OLD.xyz[:,0]==0)&(OLD.xyz[:,1]==0)&(OLD.xyz[:,2]<0)], (180 if degrees else np.pi)))
@icontract.ensure(lambda OLD, result, degrees: (~((OLD.xyz[:,0]>0)&(OLD.xyz[:,1]==0))).all() or np.allclose(result[2][(OLD.xyz[:,0]>0)&(OLD.xyz[:,1]==0)], 0))
@icontract.ensure(lambda OLD, result, degrees: (~((OLD.xyz[:,0]==0)&(OLD.xyz[:,1]>0))).all() or np.allclose(result[2][(OLD.xyz[:,0]==0)&(OLD.xyz[:,1]>0)], (90 if degrees else (np.pi/2))))
@icontract.ensure(lambda OLD, result, degrees: (~((OLD.xyz[:,0]<0)&(OLD.xyz[:,1]==0))).all() or np.allclose(result[2][(OLD.xyz[:,0]<0)&(OLD.xyz[:,1]==0)], (180 if degrees else np.pi)))
@icontract.ensure(lambda OLD, result, degrees: (~((OLD.xyz[:,0]==0)&(OLD.xyz[:,1]<0))).all() or np.allclose(result[2][(OLD.xyz[:,0]==0)&(OLD.xyz[:,1]<0)], (-90 if degrees else (-np.pi/2))))
```
[25]
===== 25 =====
```
     azimuth = np.nan_to_num(np.arctan2(y, x))
 
     if degrees:
-        inclination = np.rad2deg(inclination)
+        inclination = None
         azimuth = np.rad2deg(azimuth)
 
-    return radius, inclination, azimuth+    return radius, inclination, azimuth
```
```
def cartesian_to_spherical(xyz, degrees=True):
    """
    Convert cartesian coordinates (x, y, z) to spherical (r, theta, phi).

    Parameters
    ----------
    xyz: (N, 3) ndarray
        Corresponding cartesian coordinates.
    degrees: bool, optional
        If True, azimuthal and polar will be returned in degrees.

    Returns
    -------
    radius: (N,) ndarray
        Radial distance.
    inclination: (N,) ndarray
        Polar angle.
    azimuth: (N,) ndarray
        Azimuthal angle.
    """
    x = xyz[:, 0]
    y = xyz[:, 1]
    z = xyz[:, 2]

    radius = np.nan_to_num(np.sqrt((x * x) + (y * y) + (z * z)))

    inclination = np.nan_to_num(np.arccos(z / radius))

    azimuth = np.nan_to_num(np.arctan2(y, x))

    if degrees:
        inclination = None
        azimuth = np.rad2deg(azimuth)

    return radius, inclination, azimuth

```
