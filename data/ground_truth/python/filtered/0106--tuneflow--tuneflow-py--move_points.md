https://github.com/tuneflow/tuneflow-py/blob/b5736cba31843590cdfefd6dd9c748110d347f69/./src/tuneflow_py/models/automation.py#L224-L292
```
🈚️

It's hard

@icontract.snapshot(
    lambda self: {p.id: (p.tick, p.value) for p in self._proto.points},
    name="OLD_points",
)
# 1. 不引入新的 id
@icontract.ensure(
    lambda OLD, self, point_ids, offset_tick, offset_value, overwrite_values_in_drag_area:
    set(p.id for p in self._proto.points).issubset(set(OLD.OLD_points.keys()))
)
# 2. 选中的点必须按公式移动并 clamp
@icontract.ensure(
    lambda OLD, self, point_ids, offset_tick, offset_value, overwrite_values_in_drag_area:
    all(
        any(
            p.id == pid
            and p.tick == max(0, OLD.OLD_points[pid][0] + offset_tick)
            and abs(
                p.value
                - max(0, min(1.0, OLD.OLD_points[pid][1] + offset_value))
            ) <= 1e-6
            for p in self._proto.points
        )
        for pid in set(point_ids) & set(OLD.OLD_points.keys())
    )
)
# 3. 如果 offset_tick != 0，则 tick 必须非降序
@icontract.ensure(
    lambda OLD, self, point_ids, offset_tick, offset_value, overwrite_values_in_drag_area:
    (abs(offset_tick) == 0)
    or all(
        self._proto.points[i].tick <= self._proto.points[i + 1].tick
        for i in range(len(self._proto.points) - 1)
    )
)
# 4. 如果 point_ids 里没有任何一个旧点存在，则整个操作必须是 no-op
@icontract.ensure(
    lambda OLD, self, point_ids, offset_tick, offset_value, overwrite_values_in_drag_area:
    any(pid in OLD.OLD_points for pid in point_ids)
    or (
        len(self._proto.points) == len(OLD.OLD_points)
        and set(p.id for p in self._proto.points) == set(OLD.OLD_points.keys())
        and all(
            any(
                p.id == pid
                and p.tick == OLD.OLD_points[pid][0]
                and abs(p.value - OLD.OLD_points[pid][1]) <= 1e-6
                for p in self._proto.points
            )
            for pid in OLD.OLD_points.keys()
        )
    )
)
# 5. 任意“非选中点”如果还存在，则 tick/value 必须保持不变
@icontract.ensure(
    lambda OLD, self, point_ids, offset_tick, offset_value, overwrite_values_in_drag_area:
    all(
        # 对每个旧点 pid_old（不在 point_ids 中）：
        #   如果新 points 里还存在这个 id，则 tick 和 value 不变
        (not any(p.id == pid_old for p in self._proto.points))
        or any(
            p.id == pid_old
            and p.tick == OLD.OLD_points[pid_old][0]
            and abs(p.value - OLD.OLD_points[pid_old][1]) <= 1e-6
            for p in self._proto.points
        )
        for pid_old in OLD.OLD_points.keys()
        if pid_old not in point_ids
    )
)
# 6. 当不覆盖 drag 区域，或者 offset_tick == 0 时，不允许删任何点
@icontract.ensure(
    lambda OLD, self, point_ids, offset_tick, offset_value, overwrite_values_in_drag_area:
    (overwrite_values_in_drag_area and offset_tick != 0)
    or set(p.id for p in self._proto.points) == set(OLD.OLD_points.keys())
)
# 7. 覆盖 + 向右移动：旧右边界和新右边界之间不允许有非选中点幸存
@icontract.ensure(
    lambda OLD, self, point_ids, offset_tick, offset_value, overwrite_values_in_drag_area:
    not (
        overwrite_values_in_drag_area
        and offset_tick > 0
        and any(pid in OLD.OLD_points for pid in point_ids)
    )
    or all(
        not (
            pid_old not in point_ids
            and pid_old in OLD.OLD_points
            # 旧 tick 在 (max_sel_tick, max_sel_tick + offset_tick)
            and OLD.OLD_points[pid_old][0]
            > max(
                OLD.OLD_points[pid][0]
                for pid in point_ids
                if pid in OLD.OLD_points
            )
            and OLD.OLD_points[pid_old][0]
            < max(
                OLD.OLD_points[pid][0]
                for pid in point_ids
                if pid in OLD.OLD_points
            ) + offset_tick
            # 并且这个点在新列表里还活着
            and any(p.id == pid_old for p in self._proto.points)
        )
        for pid_old in OLD.OLD_points.keys()
    )
)
# 8. 覆盖 + 向左移动：新左边界和旧左边界之间不允许有非选中点幸存
#    注意这里把左边界改成了 max(0, min_sel_tick + offset_tick) 来匹配 clamp 行为
@icontract.ensure(
    lambda OLD, self, point_ids, offset_tick, offset_value, overwrite_values_in_drag_area:
    not (
        overwrite_values_in_drag_area
        and offset_tick < 0
        and any(pid in OLD.OLD_points for pid in point_ids)
    )
    or all(
        not (
            pid_old not in point_ids
            and pid_old in OLD.OLD_points
            # 旧 tick 在 (new_left_boundary, min_sel_tick)
            and OLD.OLD_points[pid_old][0]
            > max(
                0,
                min(
                    OLD.OLD_points[pid][0]
                    for pid in point_ids
                    if pid in OLD.OLD_points
                ) + offset_tick
            )
            and OLD.OLD_points[pid_old][0]
            < min(
                OLD.OLD_points[pid][0]
                for pid in point_ids
                if pid in OLD.OLD_points
            )
            # 并且这个点在新列表里还活着
            and any(p.id == pid_old for p in self._proto.points)
        )
        for pid_old in OLD.OLD_points.keys()
    )
)
# 9. 覆盖 + 向左移动：新左边界左侧的非选中点必须原样保留，不能被多删
@icontract.ensure(
    lambda OLD, self, point_ids, offset_tick, offset_value, overwrite_values_in_drag_area:
    not (
        overwrite_values_in_drag_area
        and offset_tick < 0
        and any(pid in OLD.OLD_points for pid in point_ids)
    )
    or all(
        # 对于所有旧 tick <= 新左边界的非选中点，必须在新列表中原样存在
        any(
            p.id == pid_old
            and p.tick == OLD.OLD_points[pid_old][0]
            and abs(p.value - OLD.OLD_points[pid_old][1]) <= 1e-6
            for p in self._proto.points
        )
        for pid_old in OLD.OLD_points.keys()
        if (
            pid_old not in point_ids
            and OLD.OLD_points[pid_old][0]
            <= max(
                0,
                min(
                    OLD.OLD_points[pid][0]
                    for pid in point_ids
                    if pid in OLD.OLD_points
                ) + offset_tick
            )
        )
    )
)
# 10. 覆盖 + 向右移动：新右边界右侧的非选中点必须原样保留，不能被多删
@icontract.ensure(
    lambda OLD, self, point_ids, offset_tick, offset_value, overwrite_values_in_drag_area:
    not (
        overwrite_values_in_drag_area
        and offset_tick > 0
        and any(pid in OLD.OLD_points for pid in point_ids)
    )
    or all(
        # 对于所有旧 tick >= max_sel_tick + offset_tick 的非选中点，必须在新列表中原样存在
        any(
            p.id == pid_old
            and p.tick == OLD.OLD_points[pid_old][0]
            and abs(p.value - OLD.OLD_points[pid_old][1]) <= 1e-6
            for p in self._proto.points
        )
        for pid_old in OLD.OLD_points.keys()
        if (
            pid_old not in point_ids
            and OLD.OLD_points[pid_old][0]
            >= max(
                OLD.OLD_points[pid][0]
                for pid in point_ids
                if pid in OLD.OLD_points
            ) + offset_tick
        )
    )
)
```
[11, 15, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52]
===== 11 =====
```
         selected_points = []
         for i in range(len(self._proto.points)):
             point = self._proto.points[i]
-            if point.id not in point_id_set:
+            if point.id == -1:
                 continue
 
             selected_points.append(point)
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id == -1:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 15 =====
```
         selected_points = []
         for i in range(len(self._proto.points)):
             point = self._proto.points[i]
-            if point.id not in point_id_set:
+            if point.id is None:
                 continue
 
             selected_points.append(point)
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id is None:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 27 =====
```
             # None of the given points are not in the automation.
             return
 
-        if overwrite_values_in_drag_area:
+        if not overwrite_values_in_drag_area and offset_tick == 0:
             # Remove values in drag area.
             if (offset_tick < 0):
                 # Move left, remove values to the left.
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if not overwrite_values_in_drag_area and offset_tick == 0:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 28 =====
```
             # None of the given points are not in the automation.
             return
 
-        if overwrite_values_in_drag_area:
+        if not overwrite_values_in_drag_area:
             # Remove values in drag area.
             if (offset_tick < 0):
                 # Move left, remove values to the left.
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if not overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 29 =====
```
             # None of the given points are not in the automation.
             return
 
-        if overwrite_values_in_drag_area:
+        if overwrite_values_in_drag_area and offset_tick > 0:
             # Remove values in drag area.
             if (offset_tick < 0):
                 # Move left, remove values to the left.
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area and offset_tick > 0:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 30 =====
```
 
         if overwrite_values_in_drag_area:
             # Remove values in drag area.
-            if (offset_tick < 0):
+            if (offset_tick != 0):
                 # Move left, remove values to the left.
                 selected_points_left_after_move = max(
                     0,
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick != 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 31 =====
```
 
         if overwrite_values_in_drag_area:
             # Remove values in drag area.
-            if (offset_tick < 0):
+            if (offset_tick == 0):
                 # Move left, remove values to the left.
                 selected_points_left_after_move = max(
                     0,
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick == 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 32 =====
```
 
         if overwrite_values_in_drag_area:
             # Remove values in drag area.
-            if (offset_tick < 0):
+            if (offset_tick > 0):
                 # Move left, remove values to the left.
                 selected_points_left_after_move = max(
                     0,
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick > 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 33 =====
```
 
         if overwrite_values_in_drag_area:
             # Remove values in drag area.
-            if (offset_tick < 0):
+            if (offset_tick > 1):
                 # Move left, remove values to the left.
                 selected_points_left_after_move = max(
                     0,
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick > 1):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 34 =====
```
             if (offset_tick < 0):
                 # Move left, remove values to the left.
                 selected_points_left_after_move = max(
-                    0,
+                    1,
                     self._proto.points[drag_area_left_index].tick + offset_tick,
                 )
                 target_point = SimpleNamespace()
@@ -66,4 +66,4 @@ 
         # Maintain the order of points.
         if (abs(offset_tick) > 0):
-            self._proto.points.sort(key=lambda x: x.tick)+            self._proto.points.sort(key=lambda x: x.tick)
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    1,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)

```
===== 35 =====
```
                 # Move left, remove values to the left.
                 selected_points_left_after_move = max(
                     0,
-                    self._proto.points[drag_area_left_index].tick + offset_tick,
+                    self._proto.points[drag_area_left_index].tick - offset_tick,
                 )
                 target_point = SimpleNamespace()
                 target_point.tick = selected_points_left_after_move
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick - offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 36 =====
```
                 # Move left, remove values to the left.
                 selected_points_left_after_move = max(
                     0,
-                    self._proto.points[drag_area_left_index].tick + offset_tick,
+                    self._proto.points[drag_area_left_index].tick - offset_tick,
                 )
                 target_point = SimpleNamespace()
                 target_point.tick = selected_points_left_after_move
@@ -66,4 +66,4 @@ 
         # Maintain the order of points.
         if (abs(offset_tick) > 0):
-            self._proto.points.sort(key=lambda x: x.tick)+            self._proto.points.sort(key=lambda x: x.tick)
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick - offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)

```
===== 37 =====
```
                 # Move left, remove values to the left.
                 selected_points_left_after_move = max(
                     0,
-                    self._proto.points[drag_area_left_index].tick + offset_tick,
+                    self._proto.points[drag_area_left_index].tick,
                 )
                 target_point = SimpleNamespace()
                 target_point.tick = selected_points_left_after_move
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 38 =====
```
                 # Move left, remove values to the left.
                 selected_points_left_after_move = max(
                     0,
-                    self._proto.points[drag_area_left_index].tick + offset_tick,
+                    self._proto.points[drag_area_right_index].tick + offset_tick,
                 )
                 target_point = SimpleNamespace()
                 target_point.tick = selected_points_left_after_move
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_right_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 39 =====
```
                 # Move left, remove values to the left.
                 selected_points_left_after_move = max(
                     0,
-                    self._proto.points[drag_area_left_index].tick + offset_tick,
+                    self._proto.points[drag_area_right_index].tick - offset_tick,
                 )
                 target_point = SimpleNamespace()
                 target_point.tick = selected_points_left_after_move
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_right_index].tick - offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 40 =====
```
                     target_point,
                     lambda x: x.tick,
                 )
-                if (start_remove_index < drag_area_left_index):
+                if (start_remove_index == drag_area_left_index):
                     del self._proto.points[start_remove_index:drag_area_left_index]
             elif (offset_tick > 0):
                 # Move right, remove values to the right.
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index == drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 41 =====
```
                     target_point,
                     lambda x: x.tick,
                 )
-                if (start_remove_index < drag_area_left_index):
+                if (start_remove_index > drag_area_left_index):
                     del self._proto.points[start_remove_index:drag_area_left_index]
             elif (offset_tick > 0):
                 # Move right, remove values to the right.
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index > drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 42 =====
```
                     target_point,
                     lambda x: x.tick,
                 )
-                if (start_remove_index < drag_area_left_index):
+                if (start_remove_index >= drag_area_left_index):
                     del self._proto.points[start_remove_index:drag_area_left_index]
             elif (offset_tick > 0):
                 # Move right, remove values to the right.
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index >= drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 43 =====
```
                     del self._proto.points[start_remove_index:drag_area_left_index]
             elif (offset_tick > 0):
                 # Move right, remove values to the right.
-                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
+                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick - offset_tick
                 target_point = SimpleNamespace()
                 target_point.tick = selected_points_right_after_move
                 end_remove_index = lower_than(
@@ -66,4 +66,4 @@ 
         # Maintain the order of points.
         if (abs(offset_tick) > 0):
-            self._proto.points.sort(key=lambda x: x.tick)+            self._proto.points.sort(key=lambda x: x.tick)
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick - offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)

```
===== 44 =====
```
                     target_point,
                     lambda x: x.tick,
                 )
-                if (end_remove_index > drag_area_right_index):
+                if (end_remove_index < drag_area_left_index):
                     del self._proto.points[drag_area_right_index + 1:end_remove_index+1]
 
         for point in selected_points:
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index < drag_area_left_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 45 =====
```
                     target_point,
                     lambda x: x.tick,
                 )
-                if (end_remove_index > drag_area_right_index):
+                if (end_remove_index < drag_area_right_index):
                     del self._proto.points[drag_area_right_index + 1:end_remove_index+1]
 
         for point in selected_points:
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index < drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 46 =====
```
                     target_point,
                     lambda x: x.tick,
                 )
-                if (end_remove_index > drag_area_right_index):
+                if (end_remove_index == drag_area_left_index):
                     del self._proto.points[drag_area_right_index + 1:end_remove_index+1]
 
         for point in selected_points:
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index == drag_area_left_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 47 =====
```
                     target_point,
                     lambda x: x.tick,
                 )
-                if (end_remove_index > drag_area_right_index):
+                if (end_remove_index == drag_area_right_index):
                     del self._proto.points[drag_area_right_index + 1:end_remove_index+1]
 
         for point in selected_points:
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index == drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
===== 48 =====
```
                     lambda x: x.tick,
                 )
                 if (end_remove_index > drag_area_right_index):
-                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]
+                    del self._proto.points[drag_area_right_index + 1:end_remove_index - 1]
 
         for point in selected_points:
             point.tick = max(0, point.tick + offset_tick)
@@ -66,4 +66,4 @@ 
         # Maintain the order of points.
         if (abs(offset_tick) > 0):
-            self._proto.points.sort(key=lambda x: x.tick)+            self._proto.points.sort(key=lambda x: x.tick)
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index - 1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)

```
===== 49 =====
```
                     lambda x: x.tick,
                 )
                 if (end_remove_index > drag_area_right_index):
-                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]
+                    del self._proto.points[drag_area_right_index + 1:end_remove_index+2]
 
         for point in selected_points:
             point.tick = max(0, point.tick + offset_tick)
@@ -66,4 +66,4 @@ 
         # Maintain the order of points.
         if (abs(offset_tick) > 0):
-            self._proto.points.sort(key=lambda x: x.tick)+            self._proto.points.sort(key=lambda x: x.tick)
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+2]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)

```
===== 50 =====
```
                     lambda x: x.tick,
                 )
                 if (end_remove_index > drag_area_right_index):
-                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]
+                    del self._proto.points[drag_area_right_index + 2:end_remove_index+1]
 
         for point in selected_points:
             point.tick = max(0, point.tick + offset_tick)
@@ -66,4 +66,4 @@ 
         # Maintain the order of points.
         if (abs(offset_tick) > 0):
-            self._proto.points.sort(key=lambda x: x.tick)+            self._proto.points.sort(key=lambda x: x.tick)
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 2:end_remove_index+1]

        for point in selected_points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)

```
===== 52 =====
```
                 if (end_remove_index > drag_area_right_index):
                     del self._proto.points[drag_area_right_index + 1:end_remove_index+1]
 
-        for point in selected_points:
+        for point in self._proto.points:
             point.tick = max(0, point.tick + offset_tick)
             point.value = max(0, min(1, point.value + offset_value))
```
```
    def move_points(
            self,
        point_ids: List[int],
        offset_tick: int,
        offset_value: float,
        overwrite_values_in_drag_area=True,
    ):
        '''
        @param overwrite_values_in_drag_area If true, all values in between the moved points' old and new indexes will be removed.
        '''
        if (len(point_ids) == 0):
            return

        point_id_set = set(point_ids)
        drag_area_left_index = None
        drag_area_right_index = None
        selected_points = []
        for i in range(len(self._proto.points)):
            point = self._proto.points[i]
            if point.id not in point_id_set:
                continue

            selected_points.append(point)
            if drag_area_left_index is None:
                drag_area_left_index = i

            drag_area_right_index = i

        if drag_area_left_index is None or drag_area_right_index is None:
            # None of the given points are not in the automation.
            return

        if overwrite_values_in_drag_area:
            # Remove values in drag area.
            if (offset_tick < 0):
                # Move left, remove values to the left.
                selected_points_left_after_move = max(
                    0,
                    self._proto.points[drag_area_left_index].tick + offset_tick,
                )
                target_point = SimpleNamespace()
                target_point.tick = selected_points_left_after_move
                start_remove_index = greater_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (start_remove_index < drag_area_left_index):
                    del self._proto.points[start_remove_index:drag_area_left_index]
            elif (offset_tick > 0):
                # Move right, remove values to the right.
                selected_points_right_after_move = self._proto.points[drag_area_right_index].tick + offset_tick
                target_point = SimpleNamespace()
                target_point.tick = selected_points_right_after_move
                end_remove_index = lower_than(
                    self._proto.points,
                    target_point,
                    lambda x: x.tick,
                )
                if (end_remove_index > drag_area_right_index):
                    del self._proto.points[drag_area_right_index + 1:end_remove_index+1]

        for point in self._proto.points:
            point.tick = max(0, point.tick + offset_tick)
            point.value = max(0, min(1, point.value + offset_value))

        # Maintain the order of points.
        if (abs(offset_tick) > 0):
            self._proto.points.sort(key=lambda x: x.tick)
```
