https://github.com/chiphuyen/sniffly/blob/a237d7e9a9b37181626c049046c99b496f6c33c5/./sniffly/core/processor.py#L200-L229
```
🈚️

Timeout

@icontract.snapshot(
    lambda self: orjson.dumps(self.running_stats),
    name="running_stats_before_json",
)
@icontract.ensure(
    lambda self, message, OLD:
        self.running_stats
        == (lambda old:
                {
                    # 1) message_counts: 只对当前 type +1，其余保持不变
                    "message_counts": {
                        **old["message_counts"],
                        message["type"]:
                            old["message_counts"][message["type"]] + 1,
                    },

                    # 2) tokens: 每个 token_type = old + message 的增量
                    "tokens": {
                        token_type:
                            old["tokens"][token_type]
                            + message["tokens"][token_type]
                        for token_type in message["tokens"].keys()
                    },

                    # 3) daily_tokens:
                    #    - 如果没有 timestamp，整体必须不变；
                    #    - 如果有 timestamp，只对对应 date 的四个字段做 +，其余日期保持不变。
                    "daily_tokens": (
                        old["daily_tokens"]
                        if not message["timestamp"]
                        else (lambda date: {
                                **old["daily_tokens"],
                                date: {
                                    "input": (
                                        old["daily_tokens"][date]["input"]
                                        + message["tokens"]["input"]
                                    ),
                                    "output": (
                                        old["daily_tokens"][date]["output"]
                                        + message["tokens"]["output"]
                                    ),
                                    "cache_creation": (
                                        old["daily_tokens"][date]["cache_creation"]
                                        + message["tokens"]["cache_creation"]
                                    ),
                                    "cache_read": (
                                        old["daily_tokens"][date]["cache_read"]
                                        + message["tokens"]["cache_read"]
                                    ),
                                },
                            }
                        )(message["timestamp"][:10])
                    ),

                    # 4) tool_usage:
                    "tool_usage": (lambda tools:
                        {
                            # 对于所有已有工具 name：
                            **{
                                name: old["tool_usage"][name]
                                + sum(
                                    1
                                    for t in tools
                                    if t["name"] == name
                                )
                                for name in old["tool_usage"].keys()
                            }
                        }
                    )(message["tools"]),

                    # 5) model_usage:
                    "model_usage": (
                        old["model_usage"]
                        if not (message.get("model")
                                and message["model"] != "N/A")
                        else (lambda model:
                            {
                                **old["model_usage"],
                                model: {
                                    "count": (
                                        old["model_usage"][model]["count"] + 1
                                    ),
                                    "input_tokens": (
                                        old["model_usage"][model]["input_tokens"]
                                        + message["tokens"]["input"]
                                    ),
                                    "output_tokens": (
                                        old["model_usage"][model]["output_tokens"]
                                        + message["tokens"]["output"]
                                    ),
                                },
                            }
                        )(message["model"])
                    ),
                }
           )(orjson.loads(OLD.running_stats_before_json))
)
```
```
@icontract.snapshot(lambda self, message: dict(self.running_stats["message_counts"]), name="OLD_message_counts")
@icontract.snapshot(lambda self, message: dict(self.running_stats["tokens"]), name="OLD_tokens")
@icontract.snapshot(lambda self, message: {d: dict(v) for d, v in self.running_stats["daily_tokens"].items()}, name="OLD_daily_tokens")
@icontract.snapshot(lambda self, message: dict(self.running_stats["tool_usage"]), name="OLD_tool_usage")
@icontract.snapshot(lambda self, message: {m: dict(v) for m, v in self.running_stats["model_usage"].items()}, name="OLD_model_usage")
@icontract.snapshot(lambda self, message: dict(message), name="OLD_message")
@icontract.ensure(lambda OLD, self, message: self.running_stats["message_counts"].get(message["type"], 0) == OLD.OLD_message_counts.get(message["type"], 0) + 1)
@icontract.ensure(lambda OLD, self, message: sum(self.running_stats["message_counts"].values()) == sum(OLD.OLD_message_counts.values()) + 1)
@icontract.ensure(lambda OLD, self, message: all(
    self.running_stats["tokens"].get(t, 0) == OLD.OLD_tokens.get(t, 0) + message["tokens"].get(t, 0)
    for t in (set(OLD.OLD_tokens.keys()) | set(message["tokens"].keys()))
))
@icontract.ensure(lambda OLD, self, message: all(
    self.running_stats["tokens"].get(k, 0) == sum(d.get(k, 0) for d in self.running_stats["daily_tokens"].values())
    for k in ("input", "output", "cache_creation", "cache_read")
))
@icontract.ensure(lambda OLD, self, message: (not message.get("timestamp")) or all(
    self.running_stats["daily_tokens"][message["timestamp"][:10]].get(k, 0) == OLD.OLD_daily_tokens.get(message["timestamp"][:10], {}).get(k, 0) + message["tokens"].get(k, 0)
    for k in ("input", "output", "cache_creation", "cache_read")
))
@icontract.ensure(lambda OLD, self, message: all(
    self.running_stats["tool_usage"].get(name, 0) == OLD.OLD_tool_usage.get(name, 0) + sum(1 for t in message["tools"] if t["name"] == name)
    for name in set(list(OLD.OLD_tool_usage.keys()) + [t["name"] for t in message["tools"]])
))
@icontract.ensure(lambda OLD, self, message: all(
    self.running_stats["tool_usage"].get(name, 0) == OLD.OLD_tool_usage.get(name, 0)
    for name in OLD.OLD_tool_usage.keys() if name not in {t["name"] for t in message["tools"]}
))
@icontract.ensure(lambda OLD, self, message: (not (message.get("model") and message["model"] != "N/A")) or (
    self.running_stats["model_usage"][message["model"]]["count"] == OLD.OLD_model_usage.get(message["model"], {}).get("count", 0) + 1 and
    self.running_stats["model_usage"][message["model"]]["input_tokens"] == OLD.OLD_model_usage.get(message["model"], {}).get("input_tokens", 0) + message["tokens"]["input"] and
    self.running_stats["model_usage"][message["model"]]["output_tokens"] == OLD.OLD_model_usage.get(message["model"], {}).get("output_tokens", 0) + message["tokens"]["output"] and
    all(
        self.running_stats["model_usage"].get(m, {}).get("count", 0) == OLD.OLD_model_usage.get(m, {}).get("count", 0) and
        self.running_stats["model_usage"].get(m, {}).get("input_tokens", 0) == OLD.OLD_model_usage.get(m, {}).get("input_tokens", 0) and
        self.running_stats["model_usage"].get(m, {}).get("output_tokens", 0) == OLD.OLD_model_usage.get(m, {}).get("output_tokens", 0)
        for m in OLD.OLD_model_usage.keys() if m != message.get("model")
    )
))
@icontract.ensure(lambda OLD, self, message: all(v >= 0 for v in self.running_stats["tokens"].values()))
@icontract.ensure(lambda OLD, self, message: all(v >= 0 for v in self.running_stats["message_counts"].values()))
@icontract.ensure(lambda OLD, self, message: all(v >= 0 for v in self.running_stats["tool_usage"].values()))
@icontract.ensure(lambda OLD, self, message: all(
    all(inner_v >= 0 for inner_v in self.running_stats["model_usage"].get(m, {}).values())
    for m in self.running_stats["model_usage"].keys()
))
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
===== 0 =====
```
 
         # Token accumulation
         for token_type, count in message["tokens"].items():
-            self.running_stats["tokens"][token_type] += count
+            self.running_stats["tokens"][token_type] += count * 2  # Incorrectly doubles the count
 
         # Daily accumulation
         if message["timestamp"]:
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count * 2  # Incorrectly doubles the count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
===== 1 =====
```
 
         # Token accumulation
         for token_type, count in message["tokens"].items():
-            self.running_stats["tokens"][token_type] += count
+            self.running_stats["tokens"][token_type] += count - 1  # Incorrectly subtracts 1 from the count
 
         # Daily accumulation
         if message["timestamp"]:
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count - 1  # Incorrectly subtracts 1 from the count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
===== 2 =====
```
 
         # Token accumulation
         for token_type, count in message["tokens"].items():
-            self.running_stats["tokens"][token_type] += count
+            self.running_stats["tokens"][token_type] += count // 2  # Incorrectly halves the count
 
         # Daily accumulation
         if message["timestamp"]:
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count // 2  # Incorrectly halves the count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
===== 3 =====
```
 
         # Token accumulation
         for token_type, count in message["tokens"].items():
-            self.running_stats["tokens"][token_type] += count
+            self.running_stats["tokens"][token_type] -= count
 
         # Daily accumulation
         if message["timestamp"]:
@@ -27,4 +27,4 @@         if message.get("model") and message["model"] != "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] -= count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 4 =====
```
 
         # Token accumulation
         for token_type, count in message["tokens"].items():
-            self.running_stats["tokens"][token_type] += count
+            self.running_stats["tokens"][token_type] = count
 
         # Daily accumulation
         if message["timestamp"]:
@@ -27,4 +27,4 @@         if message.get("model") and message["model"] != "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] = count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 5 =====
```
 
         # Token accumulation
         for token_type, count in message["tokens"].items():
-            self.running_stats["tokens"][token_type] += count
+            self.running_stats["tokens"][token_type] = count  # Overwrites the count instead of accumulating
 
         # Daily accumulation
         if message["timestamp"]:
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] = count  # Overwrites the count instead of accumulating

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
===== 6 =====
```
             self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]
 
         # Tool usage
-        for tool in message["tools"]:
+        for tool in message["tools"] + ["default_tool"]:  # Adds a default tool to the list
             self.running_stats["tool_usage"][tool["name"]] += 1
 
         # Model usage
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"] + ["default_tool"]:  # Adds a default tool to the list
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
===== 7 =====
```
 
         # Tool usage
         for tool in message["tools"]:
-            self.running_stats["tool_usage"][tool["name"]] += 1
+            self.running_stats["tool_usage"][tool["name"]] += 2
 
         # Model usage
         if message.get("model") and message["model"] != "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 2

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 8 =====
```
 
         # Tool usage
         for tool in message["tools"]:
-            self.running_stats["tool_usage"][tool["name"]] += 1
+            self.running_stats["tool_usage"][tool["name"]] += 2  # Incorrect increment value
 
         # Model usage
         if message.get("model") and message["model"] != "N/A":
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 2  # Incorrect increment value

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
===== 9 =====
```
 
         # Tool usage
         for tool in message["tools"]:
-            self.running_stats["tool_usage"][tool["name"]] += 1
+            self.running_stats["tool_usage"][tool["name"]] -= 1
 
         # Model usage
         if message.get("model") and message["model"] != "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] -= 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 10 =====
```
 
         # Tool usage
         for tool in message["tools"]:
-            self.running_stats["tool_usage"][tool["name"]] += 1
+            self.running_stats["tool_usage"][tool["name"]] = 1
 
         # Model usage
         if message.get("model") and message["model"] != "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] = 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 11 =====
```
 
         # Tool usage
         for tool in message["tools"]:
-            self.running_stats["tool_usage"][tool["name"]] += 1
+            self.running_stats["tool_usage"][tool["name"]] = 1  # Resets the count instead of incrementing
 
         # Model usage
         if message.get("model") and message["model"] != "N/A":
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] = 1  # Resets the count instead of incrementing

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
===== 12 =====
```
             self.running_stats["tool_usage"][tool["name"]] += 1
 
         # Model usage
-        if message.get("model") and message["model"] != "N/A":
+        if "model" in message and message["model"] == "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
             self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if "model" in message and message["model"] == "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
===== 13 =====
```
             self.running_stats["tool_usage"][tool["name"]] += 1
 
         # Model usage
-        if message.get("model") and message["model"] != "N/A":
+        if message.get("MODEL") and message["model"] != "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("MODEL") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 14 =====
```
             self.running_stats["tool_usage"][tool["name"]] += 1
 
         # Model usage
-        if message.get("model") and message["model"] != "N/A":
+        if message.get("XXmodelXX") and message["model"] != "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("XXmodelXX") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 15 =====
```
             self.running_stats["tool_usage"][tool["name"]] += 1
 
         # Model usage
-        if message.get("model") and message["model"] != "N/A":
+        if message.get("model") == "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
             self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") == "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
===== 16 =====
```
             self.running_stats["tool_usage"][tool["name"]] += 1
 
         # Model usage
-        if message.get("model") and message["model"] != "N/A":
+        if message.get("model") and message["MODEL"] != "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["MODEL"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 17 =====
```
             self.running_stats["tool_usage"][tool["name"]] += 1
 
         # Model usage
-        if message.get("model") and message["model"] != "N/A":
+        if message.get("model") and message["XXmodelXX"] != "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["XXmodelXX"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 18 =====
```
             self.running_stats["tool_usage"][tool["name"]] += 1
 
         # Model usage
-        if message.get("model") and message["model"] != "N/A":
+        if message.get("model") and message["model"] == "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
             self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] == "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
===== 19 =====
```
             self.running_stats["tool_usage"][tool["name"]] += 1
 
         # Model usage
-        if message.get("model") and message["model"] != "N/A":
+        if message.get("model") and message["model"] == "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] == "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 20 =====
```
             self.running_stats["tool_usage"][tool["name"]] += 1
 
         # Model usage
-        if message.get("model") and message["model"] != "N/A":
+        if message.get("model") is None:
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
             self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") is None:
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
===== 21 =====
```
             self.running_stats["tool_usage"][tool["name"]] += 1
 
         # Model usage
-        if message.get("model") and message["model"] != "N/A":
+        if message.get(None) and message["model"] != "N/A":
             self.running_stats["model_usage"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get(None) and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 22 =====
```
 
         # Model usage
         if message.get("model") and message["model"] != "N/A":
-            self.running_stats["model_usage"][message["model"]]["count"] += 1
+            self.running_stats["MODEL_USAGE"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["MODEL_USAGE"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 23 =====
```
 
         # Model usage
         if message.get("model") and message["model"] != "N/A":
-            self.running_stats["model_usage"][message["model"]]["count"] += 1
+            self.running_stats["XXmodel_usageXX"][message["model"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["XXmodel_usageXX"][message["model"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 24 =====
```
 
         # Model usage
         if message.get("model") and message["model"] != "N/A":
-            self.running_stats["model_usage"][message["model"]]["count"] += 1
+            self.running_stats["model_usage"][message["MODEL"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["MODEL"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 25 =====
```
 
         # Model usage
         if message.get("model") and message["model"] != "N/A":
-            self.running_stats["model_usage"][message["model"]]["count"] += 1
+            self.running_stats["model_usage"][message["XXmodelXX"]]["count"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["XXmodelXX"]]["count"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 26 =====
```
 
         # Model usage
         if message.get("model") and message["model"] != "N/A":
-            self.running_stats["model_usage"][message["model"]]["count"] += 1
+            self.running_stats["model_usage"][message["model"]]["COUNT"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["COUNT"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 27 =====
```
 
         # Model usage
         if message.get("model") and message["model"] != "N/A":
-            self.running_stats["model_usage"][message["model"]]["count"] += 1
+            self.running_stats["model_usage"][message["model"]]["XXcountXX"] += 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["XXcountXX"] += 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
===== 28 =====
```
 
         # Model usage
         if message.get("model") and message["model"] != "N/A":
-            self.running_stats["model_usage"][message["model"]]["count"] += 1
+            self.running_stats["model_usage"][message["model"]]["count"] -= 1
             self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
-            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]+            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]
```
```
    def _update_running_stats(self, message: dict):
        """Update running statistics as we process messages.

        Note: daily_tokens are accumulated in UTC and will be recalculated
        with timezone offset in the StatisticsGenerator.
        """
        # Message type counts
        self.running_stats["message_counts"][message["type"]] += 1

        # Token accumulation
        for token_type, count in message["tokens"].items():
            self.running_stats["tokens"][token_type] += count

        # Daily accumulation
        if message["timestamp"]:
            date = message["timestamp"][:10]
            self.running_stats["daily_tokens"][date]["input"] += message["tokens"]["input"]
            self.running_stats["daily_tokens"][date]["output"] += message["tokens"]["output"]
            self.running_stats["daily_tokens"][date]["cache_creation"] += message["tokens"]["cache_creation"]
            self.running_stats["daily_tokens"][date]["cache_read"] += message["tokens"]["cache_read"]

        # Tool usage
        for tool in message["tools"]:
            self.running_stats["tool_usage"][tool["name"]] += 1

        # Model usage
        if message.get("model") and message["model"] != "N/A":
            self.running_stats["model_usage"][message["model"]]["count"] -= 1
            self.running_stats["model_usage"][message["model"]]["input_tokens"] += message["tokens"]["input"]
            self.running_stats["model_usage"][message["model"]]["output_tokens"] += message["tokens"]["output"]

```
