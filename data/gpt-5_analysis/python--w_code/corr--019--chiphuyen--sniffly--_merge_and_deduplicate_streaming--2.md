https://github.com/chiphuyen/sniffly/blob/a237d7e9a9b37181626c049046c99b496f6c33c5/./sniffly/core/processor.py#L834-L877
```
@icontract.snapshot(lambda messages: (lambda ids: {i: ids.count(i) for i in set(ids)})([(m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id")) for m in messages if m.get("type") == "assistant" and (m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id"))]), name="id_counts")
@icontract.snapshot(lambda messages: (lambda ids, counts: [id(m) for m in messages if not (m.get("type") == "assistant" and ((m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id")) and counts[(m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id"))] > 1))])([(m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id")) for m in messages if m.get("type") == "assistant" and (m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id"))], (lambda ids2: {i: ids2.count(i) for i in set(ids2)})([(m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id")) for m in messages if m.get("type") == "assistant" and (m.get("_raw_data", {}).get("message", {}).get("id") or m.get("message_id"))])), name="ungrouped_ids")
@icontract.ensure(lambda result, messages, OLD: len(result) == len(messages) - sum(c - 1 for c in OLD.id_counts.values() if c > 1))
@icontract.ensure(lambda result, OLD: (lambda ids: set(ids) == set(OLD.id_counts.keys()) and len(ids) == len(set(ids)))([m.get("message_id") for m in result if m.get("type") == "assistant" and m.get("message_id")]))
@icontract.ensure(lambda result, OLD: set(id(m) for m in result if not (m.get("type") == "assistant" and m.get("message_id"))) == set(OLD.ungrouped_ids))
```
```
Syntax Error.

E   SyntaxError: closing parenthesis ')' does not match opening parenthesis '['
```
icontract_fail
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
