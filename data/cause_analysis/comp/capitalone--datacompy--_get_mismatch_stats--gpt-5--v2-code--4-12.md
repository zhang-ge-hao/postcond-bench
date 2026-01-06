https://github.com/capitalone/datacompy/blob/2600d7c93f2656de63b108cdb8d37cbec8eb8bbf/./datacompy/core.py#L709-L764
```
@icontract.ensure(
    lambda self, sample_count, result:
        result["mismatch_stats"]["has_mismatches"]
        == any(not col["all_match"] for col in self.column_stats)
)
@icontract.ensure(
    lambda self, sample_count, result:
        (not result["mismatch_stats"]["has_mismatches"])
        or len(result["mismatch_stats"]["stats"])
        == sum(1 for col in self.column_stats if not col["all_match"])
)
@icontract.ensure(
    lambda self, sample_count, result:
        (not result["mismatch_stats"]["has_mismatches"])
        or set(s["column"] for s in result["mismatch_stats"]["stats"])
        == {col["column"] for col in self.column_stats if not col["all_match"]}
)
@icontract.ensure(
    lambda self, sample_count, result:
        (not result["mismatch_stats"]["has_mismatches"])
        or (
            result["mismatch_stats"]["df1_name"] == self.df1_name
            and result["mismatch_stats"]["df2_name"] == self.df2_name
        )
)
@icontract.ensure(
    lambda self, sample_count, result:
        (not result["mismatch_stats"]["has_mismatches"])
        or len(result["mismatch_stats"]["samples"])
        == sum(
            1
            for col in self.column_stats
            if (not col["all_match"]) and (col["unequal_cnt"] > 0)
        )
)
@icontract.ensure(
    lambda self, sample_count, result:
        result["mismatch_stats"]["has_samples"]
        == (
            result["mismatch_stats"]["has_mismatches"]
            and sample_count > 0
            and any(
                (not col["all_match"]) and (col["unequal_cnt"] > 0)
                for col in self.column_stats
            )
        )
)
@icontract.ensure(
    lambda self, sample_count, result:
        (not result["mismatch_stats"]["has_mismatches"])
        or all(
            result["mismatch_stats"]["stats"][i]["column"]
            <= result["mismatch_stats"]["stats"][i + 1]["column"]
            for i in range(len(result["mismatch_stats"]["stats"]) - 1)
        )
)
@icontract.ensure(
    lambda self, sample_count, result:
        all(
            (
                lambda d, s: (
                    s["dtype1"] == d["dtype1"]
                    and s["dtype2"] == d["dtype2"]
                    and s["unequal_cnt"] == d["unequal_cnt"]
                    and s["max_diff"] == d["max_diff"]
                    and s["null_diff"] == d["null_diff"]
                    and s["rel_tol"] == d["rel_tol"]
                    and s["abs_tol"] == d["abs_tol"]
                )
            )(
                next(c for c in self.column_stats if c["column"] == s["column"]),
                s,
            )
            for s in result["mismatch_stats"].get("stats", [])
        )
)
```
```
missing defensive checks

and s["unequal_cnt"] == d["unequal_cnt"]

E   KeyError: 'unequal_cnt'
```
passed
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
===== 12: local_crash =====
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
