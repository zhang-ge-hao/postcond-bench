https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/arrays/n_sum.py#L34-L140
```
@icontract.ensure(lambda result: isinstance(result, list), "Result must be a list")
@icontract.ensure(lambda result: all(isinstance(tuplet, list) for tuplet in result), "Result must be a list of lists")
@icontract.ensure(lambda result, n: all(len(tuplet) == n for tuplet in result), "Each tuplet must have exactly n elements")
@icontract.ensure(lambda result, nums: all(all(elem in nums for elem in tuplet) for tuplet in result), "All elements in tuplets must be from nums")
```
```
return value - built-in container of scalars


return value content

built-in container of scalars
```
passed
```
@icontract.snapshot(lambda nums: list(sorted(nums)), name="nums")
@icontract.ensure(
    lambda result, n: 
        isinstance(result, list) 
        and 
        all(isinstance(tpl, list) for tpl in result)
        and
        all(len(tpl) == n for tpl in result)
)
@icontract.ensure(
    lambda result, nums: 
        isinstance(result, list) 
        and 
        all(isinstance(tpl, list) for tpl in result)
        and
        all(elem in nums for tpl in result for elem in tpl)
)
@icontract.ensure(
    lambda result: 
        isinstance(result, list) 
        and 
        all(isinstance(tpl, list) for tpl in result)
        and
        all(
            result[i] != result[j]
            for i in range(len(result))
            for j in range(i)
        )
)
@icontract.ensure(
    lambda result: 
        isinstance(result, list) 
        and 
        all(isinstance(tpl, list) for tpl in result)
        and
        all(
            all(tpl[k] <= tpl[k + 1] for k in range(len(tpl) - 1))
            for tpl in result
        )
)
@icontract.ensure(
    lambda result: 
        isinstance(result, list) 
        and 
        all(isinstance(tpl, list) for tpl in result)
        and
        all(
            result[i] <= result[i + 1]
            for i in range(len(result) - 1)
        )
)
@icontract.ensure(
    lambda result, n, OLD, target, _KWARGS:
        isinstance(result, list) 
        and 
        all(isinstance(tpl, list) for tpl in result)
        and
        ((n == 0 and result == []) or
        (
            n > 0 and
            {
                tuple(sorted(repr(OLD.nums[i]) for i in idxs))
                for idxs in __import__('itertools').combinations(range(len(OLD.nums)), n)
                if (lambda sc, cc, idxs_inner, tgt:
                        cc(
                            __import__('functools').reduce(
                                lambda acc, j: sc(acc, OLD.nums[j]),
                                idxs_inner[1:],
                                OLD.nums[idxs_inner[0]],
                            ),
                            tgt,
                        ) == 0
                    )(
                        _KWARGS.get('sum_closure', lambda a, b: a + b),
                        _KWARGS.get(
                            'compare_closure',
                            lambda num, tgt: -1 if num < tgt else (1 if num > tgt else 0),
                        ),
                        idxs,
                        target,
                    )
            }
            ==
            {
                tuple(sorted(repr(e) for e in tpl))
                for tpl in result
            }
        ))
)

```
===== 84: failed =====
```
             if flag == -1:
                 lt += 1
             elif flag == 1:
-                rt -= 1
+                rt -= 2
             else:
                 results.append(sorted([nums[lt], nums[rt]]))
                 lt += 1
@@ -104,4 +104,4 @@     same_closure = kv.get('same_closure', same_closure_default)
     compare_closure = kv.get('compare_closure', compare_closure_default)
     nums.sort()
-    return n_sum(n, nums, target)+    return n_sum(n, nums, target)
```
```
def n_sum(n, nums, target, **kv):
    """
    n: int
    nums: list[object]
    target: object
    sum_closure: function, optional
        Given two elements of nums, return sum of both.
    compare_closure: function, optional
        Given one object of nums and target, return -1, 1, or 0.
    same_closure: function, optional
        Given two object of nums, return bool.
    return: list[list[object]]

    Note:
    1. type of sum_closure's return should be same 
       as type of compare_closure's first param
    """

    def sum_closure_default(a, b):
        return a + b

    def compare_closure_default(num, target):
        """ above, below, or right on? """
        if num < target:
            return -1
        elif num > target:
            return 1
        else:
            return 0

    def same_closure_default(a, b):
        return a == b

    def n_sum(n, nums, target):
        if n == 2:      # want answers with only 2 terms? easy!
            results = two_sum(nums, target)
        else:
            results = []
            prev_num = None
            for index, num in enumerate(nums):
                if prev_num is not None and \
                   same_closure(prev_num, num):
                    continue

                prev_num = num
                n_minus1_results = (
                    n_sum(                      # recursive call
                        n - 1,                  # a
                        nums[index + 1:],       # b
                        target - num            # c
                        )   # x = n_sum( a, b, c )
                    )   # n_minus1_results = x

                n_minus1_results = (
                    append_elem_to_each_list(num, n_minus1_results)
                    )
                results += n_minus1_results
        return union(results)

    def two_sum(nums, target):
        nums.sort()
        lt = 0
        rt = len(nums) - 1
        results = []
        while lt < rt:
            sum_ = sum_closure(nums[lt], nums[rt])
            flag = compare_closure(sum_, target)
            if flag == -1:
                lt += 1
            elif flag == 1:
                rt -= 2
            else:
                results.append(sorted([nums[lt], nums[rt]]))
                lt += 1
                rt -= 1
                while (lt < len(nums) and
                       same_closure(nums[lt - 1], nums[lt])):
                    lt += 1
                while (0 <= rt and
                       same_closure(nums[rt], nums[rt + 1])):
                    rt -= 1
        return results

    def append_elem_to_each_list(elem, container):
        results = []
        for elems in container:
            elems.append(elem)
            results.append(sorted(elems))
        return results

    def union(duplicate_results):
        results = []

        if len(duplicate_results) != 0:
            duplicate_results.sort()
            results.append(duplicate_results[0])
            for result in duplicate_results[1:]:
                if results[-1] != result:
                    results.append(result)

        return results

    sum_closure = kv.get('sum_closure', sum_closure_default)
    same_closure = kv.get('same_closure', same_closure_default)
    compare_closure = kv.get('compare_closure', compare_closure_default)
    nums.sort()
    return n_sum(n, nums, target)

```
