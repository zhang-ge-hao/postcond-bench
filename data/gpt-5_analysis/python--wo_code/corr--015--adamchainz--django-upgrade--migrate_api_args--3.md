https://github.com/adamchainz/django-upgrade/blob/05589e6da630cc5b9b589e183fa7c81f0b1fbed7/./src/django_upgrade/fixers/mail_api_kwargs.py#L149-L174
```
@icontract.snapshot(lambda tokens, i: [t.src for t in tokens[:i]], name="prefix_srcs")
@icontract.snapshot(lambda tokens: [t.src for t in tokens], name="all_srcs")
@icontract.snapshot(lambda tokens, i: sum(1 for t in tokens[i:] if t.src == "="), name="eq_suffix_count")
@icontract.ensure(lambda OLD, tokens, i: [t.src for t in tokens[:i]] == OLD.prefix_srcs)
@icontract.ensure(lambda OLD, tokens, convertible_posargs: (convertible_posargs == 0) or ([t.src for t in tokens] != OLD.all_srcs))
@icontract.ensure(lambda OLD, tokens, convertible_posargs: (convertible_posargs != 0) or ([t.src for t in tokens] == OLD.all_srcs))
@icontract.ensure(lambda OLD, tokens, convertible_posargs, i: (convertible_posargs == 0) or (sum(1 for t in tokens[i:] if t.src == "=") >= OLD.eq_suffix_count + convertible_posargs))
@icontract.ensure(lambda OLD, tokens, convertible_posargs: (convertible_posargs == 0) or (len(tokens) >= len(OLD.all_srcs)))
```
```
Hallucination.

@icontract.snapshot(lambda tokens, i: sum(1 for t in tokens[i:] if t.src == "="), name="eq_suffix_count")

@icontract.ensure(lambda OLD, tokens, convertible_posargs, i: (convertible_posargs == 0) or (sum(1 for t in tokens[i:] if t.src == "=") >= OLD.eq_suffix_count + convertible_posargs))

This postcond assume that there is tokens as "=".
However, it does not have "=" tokens.
```
icontract_fail
```
@icontract.snapshot(lambda tokens: tokens[:], name="old_tokens")
@icontract.snapshot(
    lambda tokens, i: parse_call_args(
        tokens, find(tokens, i, name=OP, src="(")
    )[0],
    name="old_func_args",
)
@icontract.snapshot(lambda api_config: api_config.new_kwargs[:], name="new_kwargs")
@icontract.snapshot(lambda num_posargs: num_posargs, name="num_posargs")
@icontract.snapshot(
    lambda convertible_posargs: convertible_posargs,
    name="convertible_posargs",
)
@icontract.snapshot(lambda tokens: len(tokens), name="old_len")
@icontract.ensure(
    lambda OLD, tokens, api_config, num_posargs, convertible_posargs:
        len(tokens) == OLD.old_len + OLD.convertible_posargs
        and
        all(
            any(getattr(t, "src", None) == f"{k}=" for t in tokens)
            for k in OLD.new_kwargs[
                OLD.num_posargs - OLD.convertible_posargs - api_config.new_posargs : OLD.num_posargs - api_config.new_posargs
            ]
        )
        and
        all(
            not any(getattr(t, "src", None) == f"{k}=" for t in tokens)
            for k in (
                OLD.new_kwargs[: OLD.num_posargs - OLD.convertible_posargs - api_config.new_posargs]
                + OLD.new_kwargs[OLD.num_posargs - api_config.new_posargs :]
            )
        )
        and
        (
        all(
            sum(
                1
                for t in tokens
                if getattr(t, "src", None)
                == f"{OLD.new_kwargs[argindex - api_config.new_posargs]}="
            )
            == 1
            for argindex in range(
                OLD.num_posargs - OLD.convertible_posargs,
                OLD.num_posargs,
            )
        )
        and
        all(
            not any(
                getattr(t, "src", None) == f"{kw}="
                for t in tokens
            )
            for kw in (
                set(OLD.new_kwargs)
                - {
                    OLD.new_kwargs[argindex - api_config.new_posargs]
                    for argindex in range(
                        OLD.num_posargs - OLD.convertible_posargs,
                        OLD.num_posargs,
                    )
                }
            )
        )
    )
    and
    all(
        (
            (
                lambda kw_name: (
                    (lambda kw_pos: (
                        (lambda start, end: (
                            (lambda arg_slice: (
                                (lambda first_sig: (
                                    (lambda leading_ws: (
                                        kw_pos
                                        <= tokens.index(first_sig)
                                        and
                                        all(tokens.index(ws_tok) < kw_pos for ws_tok in leading_ws)
                                    ))(
                                        [
                                            tok
                                            for offset, tok in enumerate(arg_slice)
                                            if tok.name in ("UNIMPORTANT_WS", "NL")
                                            and all(
                                                prev_tok.name in ("UNIMPORTANT_WS", "NL")
                                                for prev_tok in arg_slice[:offset]
                                            )
                                        ]
                                    )
                                ))(
                                    [
                                        tok
                                        for tok in arg_slice
                                        if tok.name not in ("UNIMPORTANT_WS", "NL")
                                    ][0]
                                )
                            ))(
                                OLD.old_tokens[start:end]
                            )
                        ))(*OLD.old_func_args[argindex])
                    ))(
                        [
                            idx
                            for idx, t in enumerate(tokens)
                            if getattr(t, "src", None) == f"{kw_name}="
                        ][0]
                    )
                )
            )(
                OLD.new_kwargs[argindex - api_config.new_posargs]
            )
        )
        for argindex in range(
            OLD.num_posargs - OLD.convertible_posargs,
            OLD.num_posargs,
        )
    )
)

```
