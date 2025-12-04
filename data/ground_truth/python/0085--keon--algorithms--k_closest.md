https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/heap/k_closest_points.py#L15-L43
```
@icontract.snapshot(lambda points: points[:], name="OLD_points")
@icontract.snapshot(lambda k: k, name="OLD_k")
@icontract.snapshot(lambda origin: origin, name="OLD_origin")
@icontract.ensure(
    lambda result, points, OLD:
        len(result) == min(OLD.OLD_k, len(points))
)
@icontract.ensure(
    lambda result, points:
        all(p in points for p in result)
)
@icontract.ensure(
    lambda result, points:
        all(result.count(p) <= points.count(p) for p in set(result))
)
@icontract.ensure(
    lambda result, points, origin, OLD:
        sorted(distance(p, origin) for p in result)
        == sorted(
            sorted(distance(p, origin) for p in points)
            [:min(OLD.OLD_k, len(points))]
        )
)
@icontract.ensure(
    lambda result, points, origin:
        all(
            distance(p, origin) <= distance(q, origin)
            for p in result
            for q in points
            if q not in result
        )
)
```
```
@icontract.snapshot(lambda points: points[:], name="OLD_points")
@icontract.snapshot(lambda k: k, name="OLD_k")
@icontract.snapshot(lambda origin: origin, name="OLD_origin")
@icontract.ensure(lambda result, points, OLD: len(result) == min(OLD.OLD_k, len(points)))
@icontract.ensure(lambda result, points, OLD: all(p in points for p in result))
@icontract.ensure(lambda result, points, OLD: all(result.count(p) <= points.count(p) for p in set(result)))
@icontract.ensure(lambda result, points, origin, OLD: sorted([distance(p, origin) for p in result]) == sorted(sorted([distance(p, origin) for p in points])[:min(OLD.OLD_k, len(points))]))
```
[10, 18]
===== 10 =====
```
     where the keys (distance) are negated.
     """
     heap = [(-distance(p, origin), p) for p in points[:k]]
-    heapify(heap)
+    heap.sort()  # Sort the heap instead of heapifying
 
     """
     For every point p in points[k:],
```
```
def k_closest(points, k, origin=(0, 0)):
    # Time: O(k+(n-k)logk)
    # Space: O(k)
    """Initialize max heap with first k points.
    Python does not support a max heap; thus we can use the default min heap
    where the keys (distance) are negated.
    """
    heap = [(-distance(p, origin), p) for p in points[:k]]
    heap.sort()  # Sort the heap instead of heapifying

    """
    For every point p in points[k:],
    check if p is smaller than the root of the max heap;
    if it is, add p to heap and remove root. Reheapify.
    """
    for point in points[k:]:
        dist = distance(point, origin)

        heappushpop(heap, (-dist, point))  # heappushpop does conditional check
        """Same as:
            if d < -heap[0][0]:
                heappush(heap, (-d,p))
                heappop(heap)

        Note: heappushpop is more efficient than separate push and pop calls.
        Each heappushpop call takes O(logk) time.
        """

    return [point for nd, point in heap]  # return points in heap
```
===== 18 =====
```
     if it is, add p to heap and remove root. Reheapify.
     """
     for point in points[k:]:
-        dist = distance(point, origin)
+        dist = distance(point, origin) + 1  # Incorrectly adding 1 to the distance
 
         heappushpop(heap, (-dist, point))  # heappushpop does conditional check
         """Same as:
```
```
def k_closest(points, k, origin=(0, 0)):
    # Time: O(k+(n-k)logk)
    # Space: O(k)
    """Initialize max heap with first k points.
    Python does not support a max heap; thus we can use the default min heap
    where the keys (distance) are negated.
    """
    heap = [(-distance(p, origin), p) for p in points[:k]]
    heapify(heap)

    """
    For every point p in points[k:],
    check if p is smaller than the root of the max heap;
    if it is, add p to heap and remove root. Reheapify.
    """
    for point in points[k:]:
        dist = distance(point, origin) + 1  # Incorrectly adding 1 to the distance

        heappushpop(heap, (-dist, point))  # heappushpop does conditional check
        """Same as:
            if d < -heap[0][0]:
                heappush(heap, (-d,p))
                heappop(heap)

        Note: heappushpop is more efficient than separate push and pop calls.
        Each heappushpop call takes O(logk) time.
        """

    return [point for nd, point in heap]  # return points in heap
```
