https://github.com/capitalone/datacompy/blob/2600d7c93f2656de63b108cdb8d37cbec8eb8bbf/./datacompy/core.py#L709-L764
```
@icontract.snapshot(lambda self: list(self.column_stats), name="old_cols")
@icontract.ensure(
    lambda OLD, result, self, sample_count:
        isinstance(result, dict)
        and "mismatch_stats" in result
        and isinstance(result["mismatch_stats"], dict)
        and "has_mismatches" in result["mismatch_stats"]
        and isinstance(result["mismatch_stats"]["has_mismatches"], bool)
        and (
            (not result["mismatch_stats"]["has_mismatches"]
                and (not any((not c["all_match"]) for c in OLD.old_cols))
                and set(result["mismatch_stats"].keys()) == {
                    "has_mismatches",
                    "has_samples",
                }
                and result["mismatch_stats"]["has_samples"] is False)
            or
            (result["mismatch_stats"]["has_mismatches"]
                and any((not c["all_match"]) for c in OLD.old_cols)
                and set(result["mismatch_stats"].keys()) == {
                    "has_mismatches",
                    "stats",
                    "df1_name",
                    "df2_name",
                    "samples",
                    "has_samples",
                }
                and isinstance(result["mismatch_stats"]["stats"], list)
                and isinstance(result["mismatch_stats"]["samples"], list)
                and all(
                    isinstance(s, str)
                    for s in result["mismatch_stats"]["samples"]
                )
                and result["mismatch_stats"]["df1_name"] == self.df1_name
                and result["mismatch_stats"]["df2_name"] == self.df2_name
                and len(result["mismatch_stats"]["stats"])
                    == sum(1 for c in OLD.old_cols if not c["all_match"])
                and result["mismatch_stats"]["stats"]
                    == sorted(
                        result["mismatch_stats"]["stats"],
                        key=lambda x: x["column"],
                    )
                and all(
                    set(d.keys())
                    == {
                        "column",
                        "dtype1",
                        "dtype2",
                        "unequal_cnt",
                        "max_diff",
                        "null_diff",
                        "rel_tol",
                        "abs_tol",
                    }
                    for d in result["mismatch_stats"]["stats"]
                )
                and all(
                    any(
                        d["column"] == c["column"]
                        and d["dtype1"] == c["dtype1"]
                        and d["dtype2"] == c["dtype2"]
                        and d["unequal_cnt"] == c["unequal_cnt"]
                        and d["max_diff"] == c["max_diff"]
                        and d["null_diff"] == c["null_diff"]
                        and d["rel_tol"] == c["rel_tol"]
                        and d["abs_tol"] == c["abs_tol"]
                        for c in OLD.old_cols
                    )
                    for d in result["mismatch_stats"]["stats"]
                )
                and result["mismatch_stats"]["samples"]
                    == [
                        df_to_str(
                            self.sample_mismatch(
                                c["column"],
                                sample_count,
                                for_display=True,
                            )
                        )
                        for c in OLD.old_cols
                        if (not c["all_match"]) and c["unequal_cnt"] > 0
                    ]
                and result["mismatch_stats"]["has_samples"]
                    == (
                        len([
                            c
                            for c in OLD.old_cols
                            if (not c["all_match"]) and c["unequal_cnt"] > 0
                        ]) > 0
                        and sample_count > 0
                    )
            )
        )
)
```
```
@icontract.snapshot(lambda self: list(self.column_stats), name="old_cols")
@icontract.ensure(lambda OLD, result, self, sample_count: isinstance(result, dict) and "mismatch_stats" in result and isinstance(result["mismatch_stats"], dict))
@icontract.ensure(lambda OLD, result, self, sample_count: result["mismatch_stats"]["has_mismatches"] == any((not c["all_match"]) for c in OLD.old_cols))
@icontract.ensure(lambda OLD, result, self, sample_count: (not result["mismatch_stats"]["has_mismatches"]) or ("stats" in result["mismatch_stats"] and isinstance(result["mismatch_stats"]["stats"], list)))
@icontract.ensure(lambda OLD, result, self, sample_count: (not result["mismatch_stats"]["has_mismatches"]) or (result["mismatch_stats"].get("df1_name") == self.df1_name and result["mismatch_stats"].get("df2_name") == self.df2_name))
@icontract.ensure(lambda OLD, result, self, sample_count: (not result["mismatch_stats"]["has_mismatches"]) or len(result["mismatch_stats"]["stats"]) == sum(1 for c in OLD.old_cols if not c["all_match"]))
@icontract.ensure(lambda OLD, result, self, sample_count: (not result["mismatch_stats"]["has_mismatches"]) or result["mismatch_stats"]["stats"] == sorted(result["mismatch_stats"]["stats"], key=lambda x: x["column"]))
@icontract.ensure(lambda OLD, result, self, sample_count: (not result["mismatch_stats"]["has_mismatches"]) or all(set(d.keys()) >= {"column","dtype1","dtype2","unequal_cnt","max_diff","null_diff","rel_tol","abs_tol"} for d in result["mismatch_stats"]["stats"]))
@icontract.ensure(lambda OLD, result, self, sample_count: (not result["mismatch_stats"]["has_mismatches"]) or all(any(d["column"]==c["column"] and d["dtype1"]==c["dtype1"] and d["dtype2"]==c["dtype2"] and d["unequal_cnt"]==c["unequal_cnt"] and d["max_diff"]==c["max_diff"] and d["null_diff"]==c["null_diff"] and d["rel_tol"]==c["rel_tol"] and d["abs_tol"]==c["abs_tol"] for c in OLD.old_cols) for d in result["mismatch_stats"]["stats"]))
@icontract.ensure(lambda OLD, result, self, sample_count: (not result["mismatch_stats"]["has_mismatches"]) or result["mismatch_stats"]["samples"] == [df_to_str(self.sample_mismatch(c["column"], sample_count, for_display=True)) for c in OLD.old_cols if (not c["all_match"]) and c["unequal_cnt"] > 0])
@icontract.ensure(lambda OLD, result, self, sample_count: (not result["mismatch_stats"]["has_mismatches"]) or result["mismatch_stats"]["has_samples"] == ((len([c for c in OLD.old_cols if (not c["all_match"]) and c["unequal_cnt"] > 0]) > 0) and sample_count > 0))
```
[12, 13, 15, 16, 18, 19, 20, 21, 22, 23, 31, 32, 33, 34, 36, 37, 42, 43, 47, 48, 53, 54, 55]
===== 12 =====
```
                         "column": column["column"],
                         "dtype1": column["dtype1"],
                         "dtype2": column["dtype2"],
-                        "unequal_cnt": column["unequal_cnt"],
+                        "UNEQUAL_CNT": column["unequal_cnt"],
                         "max_diff": column["max_diff"],
                         "null_diff": column["null_diff"],
                         "rel_tol": column["rel_tol"],
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "UNEQUAL_CNT": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 13 =====
```
                         "column": column["column"],
                         "dtype1": column["dtype1"],
                         "dtype2": column["dtype2"],
-                        "unequal_cnt": column["unequal_cnt"],
+                        "XXunequal_cntXX": column["unequal_cnt"],
                         "max_diff": column["max_diff"],
                         "null_diff": column["null_diff"],
                         "rel_tol": column["rel_tol"],
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "XXunequal_cntXX": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 15 =====
```
                         "dtype1": column["dtype1"],
                         "dtype2": column["dtype2"],
                         "unequal_cnt": column["unequal_cnt"],
-                        "max_diff": column["max_diff"],
+                        "MAX_DIFF": column["max_diff"],
                         "null_diff": column["null_diff"],
                         "rel_tol": column["rel_tol"],
                         "abs_tol": column["abs_tol"],
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "MAX_DIFF": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 16 =====
```
                         "dtype1": column["dtype1"],
                         "dtype2": column["dtype2"],
                         "unequal_cnt": column["unequal_cnt"],
-                        "max_diff": column["max_diff"],
+                        "XXmax_diffXX": column["max_diff"],
                         "null_diff": column["null_diff"],
                         "rel_tol": column["rel_tol"],
                         "abs_tol": column["abs_tol"],
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "XXmax_diffXX": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 18 =====
```
                         "dtype2": column["dtype2"],
                         "unequal_cnt": column["unequal_cnt"],
                         "max_diff": column["max_diff"],
-                        "null_diff": column["null_diff"],
+                        "NULL_DIFF": column["null_diff"],
                         "rel_tol": column["rel_tol"],
                         "abs_tol": column["abs_tol"],
                     }
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "NULL_DIFF": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 19 =====
```
                         "dtype2": column["dtype2"],
                         "unequal_cnt": column["unequal_cnt"],
                         "max_diff": column["max_diff"],
-                        "null_diff": column["null_diff"],
+                        "XXnull_diffXX": column["null_diff"],
                         "rel_tol": column["rel_tol"],
                         "abs_tol": column["abs_tol"],
                     }
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "XXnull_diffXX": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 20 =====
```
                         "unequal_cnt": column["unequal_cnt"],
                         "max_diff": column["max_diff"],
                         "null_diff": column["null_diff"],
-                        "rel_tol": column["rel_tol"],
+                        "REL_TOL": column["rel_tol"],
                         "abs_tol": column["abs_tol"],
                     }
                 )
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "REL_TOL": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 21 =====
```
                         "unequal_cnt": column["unequal_cnt"],
                         "max_diff": column["max_diff"],
                         "null_diff": column["null_diff"],
-                        "rel_tol": column["rel_tol"],
+                        "XXrel_tolXX": column["rel_tol"],
                         "abs_tol": column["abs_tol"],
                     }
                 )
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "XXrel_tolXX": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 22 =====
```
                         "max_diff": column["max_diff"],
                         "null_diff": column["null_diff"],
                         "rel_tol": column["rel_tol"],
-                        "abs_tol": column["abs_tol"],
+                        "ABS_TOL": column["abs_tol"],
                     }
                 )
                 if column["unequal_cnt"] > 0:
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "ABS_TOL": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 23 =====
```
                         "max_diff": column["max_diff"],
                         "null_diff": column["null_diff"],
                         "rel_tol": column["rel_tol"],
-                        "abs_tol": column["abs_tol"],
+                        "XXabs_tolXX": column["abs_tol"],
                     }
                 )
                 if column["unequal_cnt"] > 0:
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "XXabs_tolXX": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 31 =====
```
 
         if any_mismatch:
             return {
-                "mismatch_stats": {
+                "MISMATCH_STATS": {
                     "has_mismatches": True,
                     "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                     "df1_name": self.df1_name,
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "MISMATCH_STATS": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 32 =====
```
 
         if any_mismatch:
             return {
-                "mismatch_stats": {
+                "XXmismatch_statsXX": {
                     "has_mismatches": True,
                     "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                     "df1_name": self.df1_name,
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "XXmismatch_statsXX": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 33 =====
```
         if any_mismatch:
             return {
                 "mismatch_stats": {
-                    "has_mismatches": True,
+                    "HAS_MISMATCHES": True,
                     "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                     "df1_name": self.df1_name,
                     "df2_name": self.df2_name,
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "HAS_MISMATCHES": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 34 =====
```
         if any_mismatch:
             return {
                 "mismatch_stats": {
-                    "has_mismatches": True,
+                    "XXhas_mismatchesXX": True,
                     "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                     "df1_name": self.df1_name,
                     "df2_name": self.df2_name,
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "XXhas_mismatchesXX": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 36 =====
```
             return {
                 "mismatch_stats": {
                     "has_mismatches": True,
-                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
+                    "STATS": sorted(mismatch_stats, key=lambda x: x["column"]),
                     "df1_name": self.df1_name,
                     "df2_name": self.df2_name,
                     "samples": [df_to_str(sample) for sample in match_sample],
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "STATS": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 37 =====
```
             return {
                 "mismatch_stats": {
                     "has_mismatches": True,
-                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
+                    "XXstatsXX": sorted(mismatch_stats, key=lambda x: x["column"]),
                     "df1_name": self.df1_name,
                     "df2_name": self.df2_name,
                     "samples": [df_to_str(sample) for sample in match_sample],
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "XXstatsXX": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 42 =====
```
                     "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                     "df1_name": self.df1_name,
                     "df2_name": self.df2_name,
-                    "samples": [df_to_str(sample) for sample in match_sample],
+                    "SAMPLES": [df_to_str(sample) for sample in match_sample],
                     "has_samples": len(match_sample) > 0 and sample_count > 0,
                 }
             }
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "SAMPLES": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 43 =====
```
                     "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                     "df1_name": self.df1_name,
                     "df2_name": self.df2_name,
-                    "samples": [df_to_str(sample) for sample in match_sample],
+                    "XXsamplesXX": [df_to_str(sample) for sample in match_sample],
                     "has_samples": len(match_sample) > 0 and sample_count > 0,
                 }
             }
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "XXsamplesXX": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 47 =====
```
                     "df1_name": self.df1_name,
                     "df2_name": self.df2_name,
                     "samples": [df_to_str(sample) for sample in match_sample],
-                    "has_samples": len(match_sample) > 0 and sample_count > 0,
+                    "HAS_SAMPLES": len(match_sample) > 0 and sample_count > 0,
                 }
             }
         return {
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "HAS_SAMPLES": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 48 =====
```
                     "df1_name": self.df1_name,
                     "df2_name": self.df2_name,
                     "samples": [df_to_str(sample) for sample in match_sample],
-                    "has_samples": len(match_sample) > 0 and sample_count > 0,
+                    "XXhas_samplesXX": len(match_sample) > 0 and sample_count > 0,
                 }
             }
         return {
@@ -53,4 +53,4 @@                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "XXhas_samplesXX": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 53 =====
```
                 }
             }
         return {
-            "mismatch_stats": {
+            "MISMATCH_STATS": {
                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "MISMATCH_STATS": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 54 =====
```
                 }
             }
         return {
-            "mismatch_stats": {
+            "XXmismatch_statsXX": {
                 "has_mismatches": False,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "XXmismatch_statsXX": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }

```
===== 55 =====
```
             }
         return {
             "mismatch_stats": {
-                "has_mismatches": False,
+                "has_mismatches": True,
                 "has_samples": False,
             }
-        }+        }
```
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": True,
                "has_samples": False,
            }
        }

```
