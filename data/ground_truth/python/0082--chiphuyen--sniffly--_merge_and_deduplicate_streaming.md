https://github.com/chiphuyen/sniffly/blob/a237d7e9a9b37181626c049046c99b496f6c33c5/./sniffly/core/processor.py#L834-L877
```
@icontract.snapshot(lambda messages: messages[:], name="OLD_messages")
@icontract.ensure(
    lambda OLD, self, result, messages: (
        all(msg is not None for msg in result)
        and [m for m in result if m.get("type") != "assistant"]
        == [m for m in OLD.OLD_messages if m.get("type") != "assistant"]
        and all(r is not None for r in result)
        and all(
            sum(1 for r in result if r.get("message_id") == aid) == 1
            for aid in set(
                (
                    m.get("_raw_data", {})
                    .get("message", {})
                    .get("id")
                    or m.get("message_id")
                )
                for m in OLD.OLD_messages
                if m.get("type") == "assistant"
            )
            if aid
            and sum(
                1
                for m in OLD.OLD_messages
                if m.get("type") == "assistant"
                and (
                    m.get("_raw_data", {})
                    .get("message", {})
                    .get("id")
                    or m.get("message_id")
                )
                == aid
            )
            > 1
        )
        and all(
            any(
                r
                == self._merge_message_group(
                    [
                        m
                        for m in OLD.OLD_messages
                        if m.get("type") == "assistant"
                        and (
                            m.get("_raw_data", {})
                            .get("message", {})
                            .get("id")
                            or m.get("message_id")
                        )
                        == aid
                    ]
                )
                for r in result
                if r.get("message_id") == aid
            )
            for aid in set(
                (
                    m.get("_raw_data", {})
                    .get("message", {})
                    .get("id")
                    or m.get("message_id")
                )
                for m in OLD.OLD_messages
                if m.get("type") == "assistant"
            )
            if aid
            and sum(
                1
                for m in OLD.OLD_messages
                if m.get("type") == "assistant"
                and (
                    m.get("_raw_data", {})
                    .get("message", {})
                    .get("id")
                    or m.get("message_id")
                )
                == aid
            )
            > 1
        )
        and all(
            m in result
            for m in OLD.OLD_messages
            if m.get("type") == "assistant"
            and (
                (
                    m.get("_raw_data", {})
                    .get("message", {})
                    .get("id")
                    or m.get("message_id")
                )
                is None
                or (
                    sum(
                        1
                        for mm in OLD.OLD_messages
                        if mm.get("type") == "assistant"
                        and (
                            mm.get("_raw_data", {})
                            .get("message", {})
                            .get("id")
                            or mm.get("message_id")
                        )
                        == (
                            m.get("_raw_data", {})
                            .get("message", {})
                            .get("id")
                            or m.get("message_id")
                        )
                    )
                    == 1
                )
            )
        )
        and all(
            (
                not (
                    next(
                        i
                        for i, m in enumerate(OLD.OLD_messages)
                        if m.get("type") == "assistant"
                        and (
                            m.get("_raw_data", {})
                            .get("message", {})
                            .get("id")
                            or m.get("message_id")
                        )
                        == aid1
                    )
                    < next(
                        j
                        for j, m in enumerate(OLD.OLD_messages)
                        if m.get("type") == "assistant"
                        and (
                            m.get("_raw_data", {})
                            .get("message", {})
                            .get("id")
                            or m.get("message_id")
                        )
                        == aid2
                    )
                )
            )
            or (
                next(
                    i
                    for i, r in enumerate(result)
                    if r.get("message_id") == aid1
                )
                < next(
                    j
                    for j, r in enumerate(result)
                    if r.get("message_id") == aid2
                )
            )
            for aid1 in set(
                (
                    m.get("_raw_data", {})
                    .get("message", {})
                    .get("id")
                    or m.get("message_id")
                )
                for m in OLD.OLD_messages
                if m.get("type") == "assistant"
            )
            for aid2 in set(
                (
                    m.get("_raw_data", {})
                    .get("message", {})
                    .get("id")
                    or m.get("message_id")
                )
                for m in OLD.OLD_messages
                if m.get("type") == "assistant"
            )
            if aid1
            and aid2
            and aid1 != aid2
            and sum(
                1
                for m in OLD.OLD_messages
                if m.get("type") == "assistant"
                and (
                    m.get("_raw_data", {})
                    .get("message", {})
                    .get("id")
                    or m.get("message_id")
                )
                == aid1
            )
            > 1
            and sum(
                1
                for m in OLD.OLD_messages
                if m.get("type") == "assistant"
                and (
                    m.get("_raw_data", {})
                    .get("message", {})
                    .get("id")
                    or m.get("message_id")
                )
                == aid2
            )
            > 1
        )
    )
)
```
```
@icontract.snapshot(lambda messages: messages[:], name="OLD_messages")
@icontract.ensure(lambda OLD, self, result, messages: [m for m in result if m.get("type") != "assistant"] == [m for m in OLD.OLD_messages if m.get("type") != "assistant"])
@icontract.ensure(lambda OLD, self, result, messages: all(r is not None for r in result))
@icontract.ensure(lambda OLD, self, result, messages: all(sum(1 for r in result if r.get("message_id") == aid) == 1 for aid in set((m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id")) for m in OLD.OLD_messages if m.get("type") == "assistant") if aid and sum(1 for m in OLD.OLD_messages if m.get("type") == "assistant" and (m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id")) == aid) > 1))
@icontract.ensure(lambda OLD, self, result, messages: all(any(r == self._merge_message_group([m for m in OLD.OLD_messages if m.get("type") == "assistant" and (m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id")) == aid]) for r in result if r.get("message_id") == aid) for aid in set((m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id")) for m in OLD.OLD_messages if m.get("type") == "assistant") if aid and sum(1 for m in OLD.OLD_messages if m.get("type") == "assistant" and (m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id")) == aid) > 1))
@icontract.ensure(lambda OLD, self, result, messages: all(m in result for m in OLD.OLD_messages if m.get("type") == "assistant" and (((m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id")) is None) or (sum(1 for mm in OLD.OLD_messages if mm.get("type") == "assistant" and (mm.get("_raw_data", {}).get("message", {}).get("id") or mm.get("message_id")) == (m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id"))) == 1))))
```
[35, 38, 42]
===== 35 =====
```
                 if msg_id not in processed_ids:
                     # Merge the group
                     group = message_groups[msg_id]
-                    merged_msg = self._merge_message_group(group)
+                    merged_msg = None
                     merged.append(merged_msg)
                     processed_ids.add(msg_id)
 
@@ -41,4 +41,4 @@             elif not (msg_id and msg["type"] == "assistant" and msg_id in processed_ids):
                 merged.append(msg)
 
-        return merged+        return merged
```
```
    def _merge_and_deduplicate_streaming(self, messages: list[dict]) -> list[dict]:
        """Combined streaming merge and deduplication for Phase 2 optimization.

        This combines _merge_streaming_messages functionality with deduplication
        in a single pass for better performance.
        """
        # First do the streaming merge exactly like the original
        # Group by message_id
        message_groups = defaultdict(list)

        for msg in messages:
            if msg["type"] == "assistant":
                # Check for message ID in raw data
                msg_id = None
                if msg.get("_raw_data", {}).get("message", {}).get("id"):
                    msg_id = msg["_raw_data"]["message"]["id"]
                elif msg.get("message_id"):
                    msg_id = msg["message_id"]

                if msg_id:
                    msg["message_id"] = msg_id  # Store for easy access
                    message_groups[msg_id].append(msg)

        # Process groups
        merged = []
        processed_ids = set()

        for msg in messages:
            msg_id = msg.get("message_id")

            # Handle grouped assistant messages
            if msg_id and msg["type"] == "assistant" and msg_id in message_groups and len(message_groups[msg_id]) > 1:
                if msg_id not in processed_ids:
                    # Merge the group
                    group = message_groups[msg_id]
                    merged_msg = None
                    merged.append(merged_msg)
                    processed_ids.add(msg_id)

            # Add non-grouped messages
            elif not (msg_id and msg["type"] == "assistant" and msg_id in processed_ids):
                merged.append(msg)

        return merged

```
===== 38 =====
```
                     # Merge the group
                     group = message_groups[msg_id]
                     merged_msg = self._merge_message_group(group)
-                    merged.append(merged_msg)
+                    merged.append(None)
                     processed_ids.add(msg_id)
 
             # Add non-grouped messages
             elif not (msg_id and msg["type"] == "assistant" and msg_id in processed_ids):
                 merged.append(msg)
 
-        return merged+        return merged
```
```
    def _merge_and_deduplicate_streaming(self, messages: list[dict]) -> list[dict]:
        """Combined streaming merge and deduplication for Phase 2 optimization.

        This combines _merge_streaming_messages functionality with deduplication
        in a single pass for better performance.
        """
        # First do the streaming merge exactly like the original
        # Group by message_id
        message_groups = defaultdict(list)

        for msg in messages:
            if msg["type"] == "assistant":
                # Check for message ID in raw data
                msg_id = None
                if msg.get("_raw_data", {}).get("message", {}).get("id"):
                    msg_id = msg["_raw_data"]["message"]["id"]
                elif msg.get("message_id"):
                    msg_id = msg["message_id"]

                if msg_id:
                    msg["message_id"] = msg_id  # Store for easy access
                    message_groups[msg_id].append(msg)

        # Process groups
        merged = []
        processed_ids = set()

        for msg in messages:
            msg_id = msg.get("message_id")

            # Handle grouped assistant messages
            if msg_id and msg["type"] == "assistant" and msg_id in message_groups and len(message_groups[msg_id]) > 1:
                if msg_id not in processed_ids:
                    # Merge the group
                    group = message_groups[msg_id]
                    merged_msg = self._merge_message_group(group)
                    merged.append(None)
                    processed_ids.add(msg_id)

            # Add non-grouped messages
            elif not (msg_id and msg["type"] == "assistant" and msg_id in processed_ids):
                merged.append(msg)

        return merged

```
===== 42 =====
```
                     # Merge the group
                     group = message_groups[msg_id]
                     merged_msg = self._merge_message_group(group)
-                    merged.append(merged_msg)
+                    merged.insert(0, merged_msg)  # Inserting the merged message at the beginning, which may disrupt the order
                     processed_ids.add(msg_id)
 
             # Add non-grouped messages
```
```
    def _merge_and_deduplicate_streaming(self, messages: list[dict]) -> list[dict]:
        """Combined streaming merge and deduplication for Phase 2 optimization.

        This combines _merge_streaming_messages functionality with deduplication
        in a single pass for better performance.
        """
        # First do the streaming merge exactly like the original
        # Group by message_id
        message_groups = defaultdict(list)

        for msg in messages:
            if msg["type"] == "assistant":
                # Check for message ID in raw data
                msg_id = None
                if msg.get("_raw_data", {}).get("message", {}).get("id"):
                    msg_id = msg["_raw_data"]["message"]["id"]
                elif msg.get("message_id"):
                    msg_id = msg["message_id"]

                if msg_id:
                    msg["message_id"] = msg_id  # Store for easy access
                    message_groups[msg_id].append(msg)

        # Process groups
        merged = []
        processed_ids = set()

        for msg in messages:
            msg_id = msg.get("message_id")

            # Handle grouped assistant messages
            if msg_id and msg["type"] == "assistant" and msg_id in message_groups and len(message_groups[msg_id]) > 1:
                if msg_id not in processed_ids:
                    # Merge the group
                    group = message_groups[msg_id]
                    merged_msg = self._merge_message_group(group)
                    merged.insert(0, merged_msg)  # Inserting the merged message at the beginning, which may disrupt the order
                    processed_ids.add(msg_id)

            # Add non-grouped messages
            elif not (msg_id and msg["type"] == "assistant" and msg_id in processed_ids):
                merged.append(msg)

        return merged
```
