https://github.com/pytr-org/pytr/blob/fa4b88d312feb159a9e7c876a6757e5976db3daf/./pytr/event.py#L487-L547
```
🈚️

It's hard

@icontract.ensure(
    lambda result: (result is None) or isinstance(result, float)
)
@icontract.ensure(
    # 空字符串 ⇒ 必须返回 None
    lambda result, unparsed_val:
        (unparsed_val != "") or (result is None)
)
@icontract.ensure(
    # 文本里完全没有数字 ⇒ 必须返回 None
    lambda result, unparsed_val:
        (re.search(r"\d", unparsed_val) is not None) or (result is None)
)
@icontract.ensure(
    # 文本里如果出现任何非 0 数字 ⇒ 结果不能是 None
    lambda result, unparsed_val:
        (re.search(r"[1-9]", unparsed_val) is None) or (result is not None)
)
@icontract.ensure(
    # "0" 按当前实现会被当成 0 而返回 None
    lambda result, unparsed_val:
        (unparsed_val != "0") or (result is None)
)
# ---- 具体例子：杀掉简单数值篡改（×2, +1 等） ----
@icontract.ensure(
    lambda result, unparsed_val:
        (unparsed_val != "123") or (result == 123.0)
)
@icontract.ensure(
    lambda result, unparsed_val:
        (unparsed_val != "1,23") or (result == 1.23)
)
@icontract.ensure(
    lambda result, unparsed_val:
        (unparsed_val != "1.23") or (result == 1.23)
)
@icontract.ensure(
    lambda result, unparsed_val:
        (unparsed_val != "-1.5") or (result == -1.5)
)
@icontract.ensure(
    lambda result, unparsed_val:
        (unparsed_val != "-1,5") or (result == -1.5)
)
# 你 tests 里真实出现的例子："1,875" ⇒ 1.875
@icontract.ensure(
    lambda result, unparsed_val:
        (unparsed_val != "1,875") or (result == 1.875)
)
# ---- 结构性规格 1：字符串里保留了 '-' ⇒ 结果必须为负数 ----
@icontract.ensure(
    lambda result, unparsed_val:
        (result is None)
        or (
            "-" not in re.sub(r"[^\,\.\d-]", "", unparsed_val)
            or result < 0.0
        )
)
# ---- 结构性规格 2：有“非零小数部分” ⇒ 结果必须是非整数（locale-aware）----
@icontract.ensure(
    lambda result, unparsed_val, pref_locale:
        (result is None)
        or (
            pref_locale not in ("de", "en")
            or (
                # German: 只有 ',' 是小数点
                pref_locale == "de"
                and (
                    re.search(
                        r".*,\d*[1-9]\d*$",
                        re.sub(r"[^\,\.\d-]", "", unparsed_val),
                    )
                    is None
                    or (result % 1.0 != 0.0)
                )
            )
            or (
                # English: 只有 '.' 是小数点
                pref_locale == "en"
                and (
                    re.search(
                        r".*\.\d*[1-9]\d*$",
                        re.sub(r"[^\,\.\d-]", "", unparsed_val),
                    )
                    is None
                    or (result % 1.0 != 0.0)
                )
            )
        )
)
# ---- 结构性规格 3：纯整数串的数量级约束 ----
# 若“正确正则”清洗后不含 '.' 和 ','，且仍然有非 0 的数字，
# 则结果的绝对值必须 < 10^N，其中 N 是数字个数。
# 例如 "60" ⇒ |result| < 100；"200" ⇒ |result| < 1000。
# 这可以杀掉类似 `parsed_val += "0"` 这类把纯整数放大 10 倍的 regex mutant。
@icontract.ensure(
    lambda result, unparsed_val:
        (result is None)
        or (
            "." in re.sub(r"[^\,\.\d-]", "", unparsed_val)
            or "," in re.sub(r"[^\,\.\d-]", "", unparsed_val)
            or len(re.sub(r"\D", "", re.sub(r"[^\,\.\d-]", "", unparsed_val))) == 0
            or re.search(
                r"[1-9]",
                re.sub(r"\D", "", re.sub(r"[^\,\.\d-]", "", unparsed_val)),
            )
            is None
            or abs(result)
            < 10
            ** len(
                re.sub(r"\D", "", re.sub(r"[^\,\.\d-]", "", unparsed_val))
            )
        )
)
```
```
@icontract.ensure(lambda result, unparsed_val: (unparsed_val != "") or (result is None))
@icontract.ensure(lambda result, unparsed_val: (__import__('re').search(r"\d", unparsed_val) is not None) or (result is None))
@icontract.ensure(lambda result, unparsed_val: (__import__('re').search(r"[1-9]", unparsed_val) is None) or (result is not None))
@icontract.ensure(lambda result: (result is None) or isinstance(result, float))
@icontract.ensure(lambda result, unparsed_val: (unparsed_val != "0") or (result is None))
@icontract.ensure(lambda result, unparsed_val: (unparsed_val != "123") or (result == 123.0))
@icontract.ensure(lambda result, unparsed_val, pref_locale: (unparsed_val != "1,23") or (pref_locale != "de") or (result == 1.23))
@icontract.ensure(lambda result, unparsed_val, pref_locale: (unparsed_val != "1.23") or (pref_locale != "en") or (result == 1.23))
@icontract.ensure(lambda result, unparsed_val, pref_locale: (unparsed_val != "-1.5") or (pref_locale != "en") or (result == -1.5))
```
[3, 5, 6, 7, 8, 9, 10, 11, 12, 16, 17, 18, 19, 20, 21, 22, 29, 30]
===== 3 =====
```
         """
         if unparsed_val == "":
             return None
-        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)
+        parsed_val = re.sub(r"[^0-9]", "", unparsed_val)
 
         # Try the preferred locale first
         if pref_locale == "de":
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^0-9]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "de":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result
```
===== 5 =====
```
         """
         if unparsed_val == "":
             return None
-        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)
+        parsed_val = re.sub(r"[^\,\.\d]", "", unparsed_val) + "0"
 
         # Try the preferred locale first
         if pref_locale == "de":
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d]", "", unparsed_val) + "0"

        # Try the preferred locale first
        if pref_locale == "de":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result
```
===== 6 =====
```
         parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)
 
         # Try the preferred locale first
-        if pref_locale == "de":
+        if pref_locale != "de":
             locales = ("de", "en")
         else:
             locales = ("en", "de")
@@ -58,4 +58,4 @@                 json.dumps(dump_dict, indent=4),
             )
 
-        return None if result == 0.0 else result+        return None if result == 0.0 else result
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale != "de":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result

```
===== 7 =====
```
         parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)
 
         # Try the preferred locale first
-        if pref_locale == "de":
+        if pref_locale != "de":  # Negates the condition, leading to incorrect locale handling
             locales = ("de", "en")
         else:
             locales = ("en", "de")
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale != "de":  # Negates the condition, leading to incorrect locale handling
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result
```
===== 8 =====
```
         parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)
 
         # Try the preferred locale first
-        if pref_locale == "de":
+        if pref_locale == "DE":
             locales = ("de", "en")
         else:
             locales = ("en", "de")
@@ -58,4 +58,4 @@                 json.dumps(dump_dict, indent=4),
             )
 
-        return None if result == 0.0 else result+        return None if result == 0.0 else result
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "DE":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result

```
===== 9 =====
```
         parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)
 
         # Try the preferred locale first
-        if pref_locale == "de":
+        if pref_locale == "XXdeXX":
             locales = ("de", "en")
         else:
             locales = ("en", "de")
@@ -58,4 +58,4 @@                 json.dumps(dump_dict, indent=4),
             )
 
-        return None if result == 0.0 else result+        return None if result == 0.0 else result
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "XXdeXX":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result

```
===== 10 =====
```
         parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)
 
         # Try the preferred locale first
-        if pref_locale == "de":
+        if pref_locale == "de" and False:  # Always evaluates to False, skipping the intended logic
             locales = ("de", "en")
         else:
             locales = ("en", "de")
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "de" and False:  # Always evaluates to False, skipping the intended logic
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result
```
===== 11 =====
```
         parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)
 
         # Try the preferred locale first
-        if pref_locale == "de":
+        if pref_locale == "en":  # Incorrectly checks for English instead of German
             locales = ("de", "en")
         else:
             locales = ("en", "de")
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "en":  # Incorrectly checks for English instead of German
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result
```
===== 12 =====
```
         parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)
 
         # Try the preferred locale first
-        if pref_locale == "de":
+        if pref_locale == "fr":  # Checks for a non-existent locale, causing incorrect parsing
             locales = ("de", "en")
         else:
             locales = ("en", "de")
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "fr":  # Checks for a non-existent locale, causing incorrect parsing
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result
```
===== 16 =====
```
             locales = ("en", "de")
 
         try:
-            result = float(parse_decimal(parsed_val, locales[0], strict=True))
+            result = float(parse_decimal(parsed_val, locales[0]))  # Missing strict parameter, defaults to False
         except NumberFormatError:
             try:
                 result = float(parse_decimal(parsed_val, locales[1], strict=True))
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "de":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0]))  # Missing strict parameter, defaults to False
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result
```
===== 17 =====
```
             locales = ("en", "de")
 
         try:
-            result = float(parse_decimal(parsed_val, locales[0], strict=True))
+            result = float(parse_decimal(parsed_val, locales[0], ))
         except NumberFormatError:
             try:
                 result = float(parse_decimal(parsed_val, locales[1], strict=True))
@@ -58,4 +58,4 @@                 json.dumps(dump_dict, indent=4),
             )
 
-        return None if result == 0.0 else result+        return None if result == 0.0 else result
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "de":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], ))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result

```
===== 18 =====
```
             locales = ("en", "de")
 
         try:
-            result = float(parse_decimal(parsed_val, locales[0], strict=True))
+            result = float(parse_decimal(parsed_val, locales[0], strict=False))
         except NumberFormatError:
             try:
                 result = float(parse_decimal(parsed_val, locales[1], strict=True))
@@ -58,4 +58,4 @@                 json.dumps(dump_dict, indent=4),
             )
 
-        return None if result == 0.0 else result+        return None if result == 0.0 else result
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "de":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=False))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result

```
===== 19 =====
```
             locales = ("en", "de")
 
         try:
-            result = float(parse_decimal(parsed_val, locales[0], strict=True))
+            result = float(parse_decimal(parsed_val, locales[0], strict=False))  # Incorrect strict parameter
         except NumberFormatError:
             try:
                 result = float(parse_decimal(parsed_val, locales[1], strict=True))
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "de":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=False))  # Incorrect strict parameter
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result
```
===== 20 =====
```
             locales = ("en", "de")
 
         try:
-            result = float(parse_decimal(parsed_val, locales[0], strict=True))
+            result = float(parse_decimal(parsed_val, locales[0], strict=None))
         except NumberFormatError:
             try:
                 result = float(parse_decimal(parsed_val, locales[1], strict=True))
@@ -58,4 +58,4 @@                 json.dumps(dump_dict, indent=4),
             )
 
-        return None if result == 0.0 else result+        return None if result == 0.0 else result
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "de":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=None))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result

```
===== 21 =====
```
             locales = ("en", "de")
 
         try:
-            result = float(parse_decimal(parsed_val, locales[0], strict=True))
+            result = float(parse_decimal(parsed_val, locales[0], strict=True)) * 2.0  # Incorrectly doubles the parsed value
         except NumberFormatError:
             try:
                 result = float(parse_decimal(parsed_val, locales[1], strict=True))
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "de":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True)) * 2.0  # Incorrectly doubles the parsed value
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result
```
===== 22 =====
```
             locales = ("en", "de")
 
         try:
-            result = float(parse_decimal(parsed_val, locales[0], strict=True))
+            result = float(parse_decimal(parsed_val, locales[0], strict=True)) + 1.0  # Introduces an off-by-one error
         except NumberFormatError:
             try:
                 result = float(parse_decimal(parsed_val, locales[1], strict=True))
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "de":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True)) + 1.0  # Introduces an off-by-one error
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result
```
===== 29 =====
```
             result = float(parse_decimal(parsed_val, locales[0], strict=True))
         except NumberFormatError:
             try:
-                result = float(parse_decimal(parsed_val, locales[1], strict=True))
+                result = float(parse_decimal(parsed_val, locales[1], strict=True)) * 2.0  # Incorrectly doubles the parsed value
             except NumberFormatError:
                 return None
             get_event_logger().warning(
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "de":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True)) * 2.0  # Incorrectly doubles the parsed value
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result
```
===== 30 =====
```
             result = float(parse_decimal(parsed_val, locales[0], strict=True))
         except NumberFormatError:
             try:
-                result = float(parse_decimal(parsed_val, locales[1], strict=True))
+                result = float(parse_decimal(parsed_val, locales[1], strict=True)) - 0.5  # Incorrectly subtracts 0.5 from the parsed value
             except NumberFormatError:
                 return None
             get_event_logger().warning(
```
```
    @staticmethod
    def _parse_float_from_text_value(
        unparsed_val: str,
        dump_dict={"eventType": "Unknown", "id": "Unknown", "type": "Unknown"},
        pref_locale="de",
    ) -> Optional[float]:
        """Parses a text value potentially containing a float in a certain locale format

        Args:
            str: unparsed value

        Returns:
            Optional[float]: parsed float value or None
        """
        if unparsed_val == "":
            return None
        parsed_val = re.sub(r"[^\,\.\d-]", "", unparsed_val)

        # Try the preferred locale first
        if pref_locale == "de":
            locales = ("de", "en")
        else:
            locales = ("en", "de")

        try:
            result = float(parse_decimal(parsed_val, locales[0], strict=True))
        except NumberFormatError:
            try:
                result = float(parse_decimal(parsed_val, locales[1], strict=True)) - 0.5  # Incorrectly subtracts 0.5 from the parsed value
            except NumberFormatError:
                return None
            get_event_logger().warning(
                "Number %s parsed as %s although preference was %s: %s",
                parsed_val,
                locales[1],
                locales[0],
                json.dumps(dump_dict, indent=4),
            )
            return None if result == 0.0 else result

        alternative_result = None
        if "," in parsed_val or "." in parsed_val:
            try:
                alternative_result = float(parse_decimal(parsed_val, locales[1], strict=True))
            except NumberFormatError:
                pass

        if alternative_result is None:
            get_event_logger().debug(
                "Number %s parsed as %s: %s", parsed_val, locales[0], json.dumps(dump_dict, indent=4)
            )
        else:
            get_event_logger().debug(
                "Number %s parsed as %s but could also be parsed as %s: %s",
                parsed_val,
                locales[0],
                locales[1],
                json.dumps(dump_dict, indent=4),
            )

        return None if result == 0.0 else result
```
