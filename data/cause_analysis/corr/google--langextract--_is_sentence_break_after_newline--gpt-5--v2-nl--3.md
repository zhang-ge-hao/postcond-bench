https://github.com/google/langextract/blob/6e36c378994121c2b8d9a25b32cff149d9bfc61c/./langextract/core/tokenizer.py#L287-L324
```
@icontract.snapshot(lambda text, tokens, current_idx: current_idx + 1, name="next_idx")
@icontract.ensure(
    lambda text, tokens, current_idx, RESULT, next_idx:
    RESULT == (
        0 <= current_idx
        and next_idx < len(tokens)
        and tokens[next_idx].first_token_after_newline
        and 0 <= tokens[next_idx].char_interval.start_pos < len(text)
        and text[tokens[next_idx].char_interval.start_pos].isupper()
    )
)
```
```
limited spec

E   The argument(s) of the contract condition have not been set: ['RESULT', 'next_idx']. Does the original function define them? Did you supply them in the call?
```
failed
```
@icontract.ensure(lambda result, text, tokens, current_idx: (current_idx + 1 >= len(tokens) and result is False) or (current_idx + 1 < len(tokens)))
@icontract.ensure(lambda result, text, tokens, current_idx: (current_idx + 1 >= len(tokens) and result is False) or (current_idx + 1 < len(tokens) and result == (("\n" in text[tokens[current_idx].char_interval.end_pos : tokens[current_idx + 1].char_interval.start_pos]) and (len(text[tokens[current_idx + 1].char_interval.start_pos : tokens[current_idx + 1].char_interval.end_pos]) > 0) and text[tokens[current_idx + 1].char_interval.start_pos : tokens[current_idx + 1].char_interval.end_pos][0].isupper())))
```
