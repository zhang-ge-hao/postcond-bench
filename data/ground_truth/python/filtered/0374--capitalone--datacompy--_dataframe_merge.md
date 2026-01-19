https://github.com/capitalone/datacompy/blob/2600d7c93f2656de63b108cdb8d37cbec8eb8bbf/./datacompy/core.py#L269-L354
```
🈚️

It's hard

@icontract.ensure(
    lambda self, ignore_spaces:
    # 1. df1_unq_rows 的列与 df1 完全一致（顺序也一致）
    list(self.df1_unq_rows.columns) == list(self.df1.columns)
)
@icontract.ensure(
    lambda self, ignore_spaces:
    # 2. df2_unq_rows 的列与 df2 完全一致（顺序也一致）
    list(self.df2_unq_rows.columns) == list(self.df2.columns)
)
@icontract.ensure(
    lambda self, ignore_spaces:
    # 3. 按「主键」（join_columns 或 index）划分时，
    #    “df1 only / df2 only / both” 三种类别互斥且覆盖 df1 的所有 key
    #    ——不使用 index 的情况，按 join_columns 来分类。
    self.on_index
    or (
        (
            # 把各种 key 先转成 set(tuple(...)) 方便做集合运算
            lambda keys_df1, keys_df2, keys1_unq, keys2_unq, keys_inter:
                # 3.1 df1、df2 中“unique keys”两边必须互斥
                keys1_unq.isdisjoint(keys2_unq)
                # 3.2 交集必须正好是 intersect_rows 中出现的 key 集合
                and keys_inter == keys_df1.intersection(keys_df2)
                # 3.3 df1 的所有 key 必须被「df1_unq_rows ∪ intersect_rows」覆盖完
                and keys_df1 == keys1_unq.union(keys_inter)
                # 3.4 df2 的所有 key 必须被「df2_unq_rows ∪ intersect_rows」覆盖完
                and keys_df2 == keys2_unq.union(keys_inter)
        )(
            # keys_df1
            set(
                self.df1[self.join_columns].itertuples(
                    index=False, name=None
                )
            ),
            # keys_df2
            set(
                self.df2[self.join_columns].itertuples(
                    index=False, name=None
                )
            ),
            # keys1_unq: df1_unq_rows 的主键集合
            set(
                self.df1_unq_rows[self.join_columns].itertuples(
                    index=False, name=None
                )
            ),
            # keys2_unq: df2_unq_rows 的主键集合
            set(
                self.df2_unq_rows[self.join_columns].itertuples(
                    index=False, name=None
                )
            ),
            # keys_inter: intersect_rows 的主键集合
            set(
                self.intersect_rows[self.join_columns].itertuples(
                    index=False, name=None
                )
            ),
        )
    )
)
@icontract.ensure(
    lambda self, ignore_spaces:
    # 4. on_index=True 时，按 index 做同样的划分约束：
    #    - df1/df2 的 index 集必须被 df1_unq_rows / df2_unq_rows / intersect_rows 覆盖
    #    - 三类 key（index）互斥，且 intersect_rows.index 等于 df1.index 与 df2.index 的交集
    not self.on_index
    or (
        (
            lambda idx1, idx2, idx1_unq, idx2_unq, idx_inter:
                # 4.1 df1/df2 各自的“只在一侧存在”的 index 互相不重叠
                idx1_unq.isdisjoint(idx2_unq)
                # 4.2 交集 index 必须正好是 intersect_rows.index
                and idx_inter == idx1.intersection(idx2)
                # 4.3 df1 的所有 index = df1_unq_rows.index ∪ intersect_rows.index
                and idx1 == idx1_unq.union(idx_inter)
                # 4.4 df2 的所有 index = df2_unq_rows.index ∪ intersect_rows.index
                and idx2 == idx2_unq.union(idx_inter)
        )(
            set(self.df1.index),
            set(self.df2.index),
            set(self.df1_unq_rows.index),
            set(self.df2_unq_rows.index),
            set(self.intersect_rows.index),
        )
    )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
===== 0 =====
```
         if self._any_dupes:
             LOG.debug("Duplicate rows found, deduping by order of remaining fields")
             # Bring index into a column
-            if self.on_index:
+            if self._any_dupes:
                 index_column = temp_column_name(self.df1, self.df2)
                 self.df1[index_column] = self.df1.index
                 self.df2[index_column] = self.df2.index
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self._any_dupes:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 1 =====
```
         if self._any_dupes:
             LOG.debug("Duplicate rows found, deduping by order of remaining fields")
             # Bring index into a column
-            if self.on_index:
+            if self.df1.shape[1] == self.df2.shape[1]:
                 index_column = temp_column_name(self.df1, self.df2)
                 self.df1[index_column] = self.df1.index
                 self.df2[index_column] = self.df2.index
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.df1.shape[1] == self.df2.shape[1]:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 2 =====
```
             # Create order column for uniqueness of match
             order_column = temp_column_name(self.df1, self.df2)
             self.df1[order_column] = generate_id_within_group(
-                self.df1, temp_join_columns
+                self.df2, temp_join_columns
             )
             self.df2[order_column] = generate_id_within_group(
                 self.df2, temp_join_columns
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 3 =====
```
 
         for column in self.join_columns:
             self.df1[column] = normalize_string_column(
-                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
+                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=True
             )
             self.df2[column] = normalize_string_column(
                 self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
@@ -83,4 +83,4 @@         self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=True
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 4 =====
```
                 self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
             )
             self.df2[column] = normalize_string_column(
-                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
+                self.df2[column], ignore_spaces=None, ignore_case=False
             )
 
         outer_join = self.df1.merge(
@@ -83,4 +83,4 @@         self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=None, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 5 =====
```
                 self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
             )
             self.df2[column] = normalize_string_column(
-                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
+                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=True
             )
 
         outer_join = self.df1.merge(
@@ -83,4 +83,4 @@         self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=True
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 6 =====
```
             )
 
         outer_join = self.df1.merge(
-            self.df2,
+            self.df2.sample(n=0),
             how="outer",
             suffixes=("_" + self.df1_name, "_" + self.df2_name),
             indicator=True,
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2.sample(n=0),
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 7 =====
```
 
         outer_join = self.df1.merge(
             self.df2,
-            how="outer",
+            how="inner",
             suffixes=("_" + self.df1_name, "_" + self.df2_name),
             indicator=True,
             **params,
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="inner",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 8 =====
```
 
         outer_join = self.df1.merge(
             self.df2,
-            how="outer",
+            how="left",
             suffixes=("_" + self.df1_name, "_" + self.df2_name),
             indicator=True,
             **params,
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="left",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 9 =====
```
 
         outer_join = self.df1.merge(
             self.df2,
-            how="outer",
+            how="right",
             suffixes=("_" + self.df1_name, "_" + self.df2_name),
             indicator=True,
             **params,
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="right",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 10 =====
```
 
         outer_join = self.df1.merge(
             self.df2,
-            how="outer",
             suffixes=("_" + self.df1_name, "_" + self.df2_name),
             indicator=True,
             **params,
@@ -83,4 +82,4 @@         self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 11 =====
```
             self.df2.drop(order_column, axis=1, inplace=True)
 
         df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
-        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)
+        df2_cols = get_merged_columns(self.df2, outer_join, self.df1_name)  # Incorrectly uses df1_name instead of df2_name
 
         LOG.debug("Selecting df1 unique rows")
         self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df1_name)  # Incorrectly uses df1_name instead of df2_name

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 12 =====
```
         df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)
 
         LOG.debug("Selecting df1 unique rows")
-        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
+        self.df1_unq_rows = outer_join[outer_join["_merge"] != "left_only"][
             df1_cols
         ].copy()
         self.df1_unq_rows.columns = self.df1.columns
@@ -83,4 +83,4 @@         self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] != "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 13 =====
```
         df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)
 
         LOG.debug("Selecting df1 unique rows")
-        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
+        self.df1_unq_rows = outer_join[outer_join["_merge"] == "LEFT_ONLY"][
             df1_cols
         ].copy()
         self.df1_unq_rows.columns = self.df1.columns
@@ -83,4 +83,4 @@         self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "LEFT_ONLY"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 14 =====
```
         df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)
 
         LOG.debug("Selecting df1 unique rows")
-        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
+        self.df1_unq_rows = outer_join[outer_join["_merge"] == "XXleft_onlyXX"][
             df1_cols
         ].copy()
         self.df1_unq_rows.columns = self.df1.columns
@@ -83,4 +83,4 @@         self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "XXleft_onlyXX"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 15 =====
```
         df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)
 
         LOG.debug("Selecting df1 unique rows")
-        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
+        self.df1_unq_rows = outer_join[outer_join["_merge"] == "both"][  # Incorrectly selects intersecting rows instead of unique rows
             df1_cols
         ].copy()
         self.df1_unq_rows.columns = self.df1.columns
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "both"][  # Incorrectly selects intersecting rows instead of unique rows
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 16 =====
```
         df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)
 
         LOG.debug("Selecting df1 unique rows")
-        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
+        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"].sample(frac=0.5)[  # Incorrectly samples only half of the unique rows
             df1_cols
         ].copy()
         self.df1_unq_rows.columns = self.df1.columns
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"].sample(frac=0.5)[  # Incorrectly samples only half of the unique rows
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 17 =====
```
         df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)
 
         LOG.debug("Selecting df1 unique rows")
-        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
+        self.df1_unq_rows = outer_join[outer_join["_merge"] == "right_only"][  # Incorrectly selects rows unique to df2
             df1_cols
         ].copy()
         self.df1_unq_rows.columns = self.df1.columns
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "right_only"][  # Incorrectly selects rows unique to df2
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 18 =====
```
         LOG.debug("Selecting df1 unique rows")
         self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
             df1_cols
-        ].copy()
+        ].sample(frac=0.5)
         self.df1_unq_rows.columns = self.df1.columns
 
         LOG.debug("Selecting df2 unique rows")
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].sample(frac=0.5)
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 19 =====
```
         self.df1_unq_rows.columns = self.df1.columns
 
         LOG.debug("Selecting df2 unique rows")
-        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
+        self.df2_unq_rows = outer_join[outer_join["_merge"] != "right_only"][
             df2_cols
         ].copy()
         self.df2_unq_rows.columns = self.df2.columns
@@ -83,4 +83,4 @@         self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] != "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 20 =====
```
         self.df1_unq_rows.columns = self.df1.columns
 
         LOG.debug("Selecting df2 unique rows")
-        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
+        self.df2_unq_rows = outer_join[outer_join["_merge"] == "RIGHT_ONLY"][
             df2_cols
         ].copy()
         self.df2_unq_rows.columns = self.df2.columns
@@ -83,4 +83,4 @@         self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "RIGHT_ONLY"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 21 =====
```
         self.df1_unq_rows.columns = self.df1.columns
 
         LOG.debug("Selecting df2 unique rows")
-        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
+        self.df2_unq_rows = outer_join[outer_join["_merge"] == "XXright_onlyXX"][
             df2_cols
         ].copy()
         self.df2_unq_rows.columns = self.df2.columns
@@ -83,4 +83,4 @@         self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "XXright_onlyXX"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 22 =====
```
         LOG.debug("Selecting df2 unique rows")
         self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
             df2_cols
-        ].copy()
+        ].head(0)
         self.df2_unq_rows.columns = self.df2.columns
         LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
         LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].head(0)
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 23 =====
```
         LOG.debug("Selecting df2 unique rows")
         self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
             df2_cols
-        ].copy()
+        ].reset_index(drop=True)
         self.df2_unq_rows.columns = self.df2.columns
         LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
         LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].reset_index(drop=True)
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 24 =====
```
         LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")
 
         LOG.debug("Selecting intersecting rows")
-        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
+        self.intersect_rows = outer_join[outer_join["_merge"] != "both"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] != "both"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 25 =====
```
         LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")
 
         LOG.debug("Selecting intersecting rows")
-        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
+        self.intersect_rows = outer_join[outer_join["_merge"] == "BOTH"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "BOTH"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 26 =====
```
         LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")
 
         LOG.debug("Selecting intersecting rows")
-        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
+        self.intersect_rows = outer_join[outer_join["_merge"] == "XXbothXX"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
-        )+        )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "XXbothXX"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )

```
===== 27 =====
```
         LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")
 
         LOG.debug("Selecting intersecting rows")
-        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
+        self.intersect_rows = outer_join[outer_join["_merge"] == "left_only"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
         )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "left_only"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 28 =====
```
         LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")
 
         LOG.debug("Selecting intersecting rows")
-        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
+        self.intersect_rows = outer_join[outer_join["_merge"] == "right_only"].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
         )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"] == "right_only"].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
===== 29 =====
```
         LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")
 
         LOG.debug("Selecting intersecting rows")
-        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
+        self.intersect_rows = outer_join[outer_join["_merge"].isnull()].copy()
         LOG.info(
             f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
         )
```
```
    def _dataframe_merge(self, ignore_spaces: bool) -> None:
        """Merge df1 to df2 on the join columns.

        To get df1 - df2, df2 - df1
        and df1 & df2.

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """
        params: Dict[str, Any]
        index_column: str
        LOG.debug("Outer joining")
        if self._any_dupes:
            LOG.debug("Duplicate rows found, deduping by order of remaining fields")
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        for column in self.join_columns:
            self.df1[column] = normalize_string_column(
                self.df1[column], ignore_spaces=ignore_spaces, ignore_case=False
            )
            self.df2[column] = normalize_string_column(
                self.df2[column], ignore_spaces=ignore_spaces, ignore_case=False
            )

        outer_join = self.df1.merge(
            self.df2,
            how="outer",
            suffixes=("_" + self.df1_name, "_" + self.df2_name),
            indicator=True,
            **params,
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.set_index(keys=index_column, drop=True, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(labels=order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, self.df1_name)
        df2_cols = get_merged_columns(self.df2, outer_join, self.df2_name)

        LOG.debug("Selecting df1 unique rows")
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        LOG.debug("Selecting df2 unique rows")
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        LOG.info(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}")
        LOG.info(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}")

        LOG.debug("Selecting intersecting rows")
        self.intersect_rows = outer_join[outer_join["_merge"].isnull()].copy()
        LOG.info(
            f"Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"
        )
```
