https://github.com/chiphuyen/sniffly/blob/a237d7e9a9b37181626c049046c99b496f6c33c5/./sniffly/core/processor.py#L834-L877
```
@icontract.snapshot(lambda messages: [(((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) for m in messages if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is not None))], name="assistant_ids_in")
@icontract.snapshot(lambda messages: sum(1 for m in messages if m.get("type") != "assistant"), name="non_assistant_count_in")
@icontract.snapshot(lambda messages: sum(1 for m in messages if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is None)), name="assistant_no_id_count_in")
@icontract.snapshot(lambda messages: {"input": sum((m.get("tokens") or {}).get("input", 0) for m in messages if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is not None)), "output": sum((m.get("tokens") or {}).get("output", 0) for m in messages if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is not None)), "cache_creation": sum((m.get("tokens") or {}).get("cache_creation", 0) for m in messages if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is not None)), "cache_read": sum((m.get("tokens") or {}).get("cache_read", 0) for m in messages if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is not None))}, name="assistant_id_token_sums_in")
@icontract.ensure(lambda result, messages, OLD: len(result) == len(messages) - (len(OLD.assistant_ids_in) - len(set(OLD.assistant_ids_in))))
@icontract.ensure(lambda result, OLD: sum(1 for m in result if m.get("type") != "assistant") == OLD.non_assistant_count_in)
@icontract.ensure(lambda result, OLD: sum(1 for m in result if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is None)) == OLD.assistant_no_id_count_in)
@icontract.ensure(lambda result, OLD: set([(((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) for m in result if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is not None))]) == set(OLD.assistant_ids_in))
@icontract.ensure(lambda result: len([(((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) for m in result if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is not None))]) == len(set([(((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) for m in result if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is not None))])))
@icontract.ensure(lambda result, OLD: sum((m.get("tokens") or {}).get("input", 0) for m in result if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is not None)) == OLD.assistant_id_token_sums_in["input"])
@icontract.ensure(lambda result, OLD: sum((m.get("tokens") or {}).get("output", 0) for m in result if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is not None)) == OLD.assistant_id_token_sums_in["output"])
@icontract.ensure(lambda result, OLD: sum((m.get("tokens") or {}).get("cache_creation", 0) for m in result if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is not None)) == OLD.assistant_id_token_sums_in["cache_creation"])
@icontract.ensure(lambda result, OLD: sum((m.get("tokens") or {}).get("cache_read", 0) for m in result if m.get("type") == "assistant" and ((((m.get("_raw_data") or {}).get("message") or {}).get("id") or m.get("message_id")) is not None)) == OLD.assistant_id_token_sums_in["cache_read"])
```
```
Syntax error.

E   SyntaxError: closing parenthesis ')' does not match opening parenthesis '['
```
syntax_error
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
