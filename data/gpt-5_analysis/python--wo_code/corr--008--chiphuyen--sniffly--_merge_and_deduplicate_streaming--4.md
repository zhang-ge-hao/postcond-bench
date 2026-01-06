https://github.com/chiphuyen/sniffly/blob/a237d7e9a9b37181626c049046c99b496f6c33c5/./sniffly/core/processor.py#L834-L877
```
@icontract.snapshot(lambda messages: tuple(messages), name="messages")
@icontract.snapshot(lambda messages: {m.get('message_id') for m in messages if isinstance(m, dict) and m.get('message_id') is not None}, name="message_ids")
@icontract.snapshot(lambda messages: {m.get('uuid') for m in messages if isinstance(m, dict) and m.get('uuid') is not None}, name="uuids")
@icontract.snapshot(lambda messages: {m.get('timestamp') for m in messages if isinstance(m, dict) and m.get('timestamp') is not None}, name="timestamps")
@icontract.snapshot(lambda messages: {m.get('session_id') for m in messages if isinstance(m, dict) and m.get('session_id') is not None}, name="session_ids")
@icontract.snapshot(lambda messages: {m.get('type') for m in messages if isinstance(m, dict) and m.get('type') is not None}, name="types")
@icontract.ensure(lambda result: isinstance(result, list))
@icontract.ensure(lambda OLD, result: len(result) <= len(OLD.messages))
@icontract.ensure(lambda OLD, result: (len(OLD.messages) > 0) or (len(result) == 0))
@icontract.ensure(lambda result: all(isinstance(m, dict) for m in result))
@icontract.ensure(lambda result: len([m.get('message_id') for m in result if isinstance(m, dict) and m.get('message_id') is not None]) == len({m.get('message_id') for m in result if isinstance(m, dict) and m.get('message_id') is not None}))
@icontract.ensure(lambda OLD, result: all((m.get('message_id') is None) or (m.get('message_id') in OLD.message_ids) for m in result if isinstance(m, dict)))
@icontract.ensure(lambda result, self: len([(m.get('type'), m.get('timestamp'), (self._extract_message_content(m) or "")[:500]) for m in result if isinstance(m, dict) and (m.get('type') is not None) and (m.get('timestamp') is not None)]) == len({(m.get('type'), m.get('timestamp'), (self._extract_message_content(m) or "")[:500]) for m in result if isinstance(m, dict) and (m.get('type') is not None) and (m.get('timestamp') is not None)}))
@icontract.ensure(lambda OLD, result: all((m.get('timestamp') is None) or (m.get('timestamp') in OLD.timestamps) for m in result if isinstance(m, dict)))
@icontract.ensure(lambda OLD, result: len([m.get('uuid') for m in result if isinstance(m, dict) and m.get('uuid') is not None]) == len({m.get('uuid') for m in result if isinstance(m, dict) and m.get('uuid') is not None}))
@icontract.ensure(lambda OLD, result: all((m.get('uuid') is None) or (m.get('uuid') in OLD.uuids) for m in result if isinstance(m, dict)))
@icontract.ensure(lambda OLD, result: all((m.get('session_id') is None) or (m.get('session_id') in OLD.session_ids) for m in result if isinstance(m, dict)))
@icontract.ensure(lambda OLD, result: all((m.get('type') is None) or (m.get('type') in OLD.types) for m in result if isinstance(m, dict)))
```
```
Hallucination.

@icontract.ensure(lambda OLD, result: len([m.get('uuid') for m in result if isinstance(m, dict) and m.get('uuid') is not None]) == len({m.get('uuid') for m in result if isinstance(m, dict) and m.get('uuid') is not None}))

The uuid can be deduped in the implementation.
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
