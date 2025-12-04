https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/base_instrumentation_test.py#L865-L883
```
@icontract.snapshot(lambda instrumentation_block: instrumentation_block.state, name="state")
@icontract.snapshot(lambda instrumentation_block: instrumentation_block.current_key, name="current_key")
@icontract.ensure(
    lambda OLD, instrumentation_block, line, result: (
        (OLD.state != _InstrumentationBlockStates.METHOD)
        or (not line.startswith(_InstrumentationStructurePrefixes.STATUS))
        or ('=' not in line[len(_InstrumentationStructurePrefixes.STATUS):].strip())
        or (
            result.current_key
            == line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
        )
    )
)
@icontract.ensure(
    lambda OLD, instrumentation_block, line, result: (
        (OLD.state != _InstrumentationBlockStates.METHOD)
        or (not line.startswith(_InstrumentationStructurePrefixes.STATUS))
        or ('=' not in line[len(_InstrumentationStructurePrefixes.STATUS):].strip())
        or (
            (
                line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
                in result.known_keys
                and result.known_keys[
                    line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
                ]
                and result.known_keys[
                    line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
                ][-1]
                == line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[1]
            )
            or
            (
                line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
                in result.unknown_keys
                and result.unknown_keys[
                    line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
                ]
                and result.unknown_keys[
                    line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
                ][-1]
                == line[len(_InstrumentationStructurePrefixes.STATUS):].strip()
            )
        )
    )
)
@icontract.ensure(
    lambda OLD, instrumentation_block, line, result: (
        (OLD.state != _InstrumentationBlockStates.RESULT)
        or (not line.strip())
        or (
            (result.is_empty is False)
            and (
                (
                    OLD.current_key in result.known_keys
                    and result.known_keys[OLD.current_key]
                    and result.known_keys[OLD.current_key][-1] == line
                )
                or (
                    OLD.current_key in result.unknown_keys
                    and result.unknown_keys[OLD.current_key]
                    and result.unknown_keys[OLD.current_key][-1] == line
                )
            )
        )
    )
)
@icontract.ensure(
    lambda OLD, instrumentation_block, line, result: (
        (OLD.state != _InstrumentationBlockStates.METHOD)
        or (not line.startswith(_InstrumentationStructurePrefixes.STATUS))
        or ('=' not in line[len(_InstrumentationStructurePrefixes.STATUS):].strip())
        or (result is instrumentation_block)
    )
)
@icontract.ensure(
    lambda OLD, instrumentation_block, line, result: (
        (OLD.state != _InstrumentationBlockStates.UNKNOWN)
        or (not line.startswith(_InstrumentationStructurePrefixes.STATUS))
        or (result.state == _InstrumentationBlockStates.METHOD)
    )
)
@icontract.ensure(
    lambda OLD, instrumentation_block, line, result: (
        (OLD.state != _InstrumentationBlockStates.UNKNOWN)
        or (
            not line.startswith(_InstrumentationStructurePrefixes.RESULT)
            and _InstrumentationStructurePrefixes.FAILED not in line
        )
        or (result.state == _InstrumentationBlockStates.RESULT)
    )
)
@icontract.ensure(
    lambda OLD, instrumentation_block, line, result: (
        (OLD.state != _InstrumentationBlockStates.UNKNOWN)
        or (not line.strip())
        or (result.is_empty is False)
    )
)
```
```
@icontract.snapshot(lambda instrumentation_block: instrumentation_block.state, name="state")
@icontract.snapshot(lambda instrumentation_block: instrumentation_block.current_key, name="current_key")
@icontract.ensure(
    lambda OLD, instrumentation_block, line, result: (
        # If we started in METHOD and this line is a STATUS key=value,
        # the returned block's current_key must equal the parsed key.
        (OLD.state != _InstrumentationBlockStates.METHOD)
        or (not line.startswith(_InstrumentationStructurePrefixes.STATUS))
        or ('=' not in line[len(_InstrumentationStructurePrefixes.STATUS):].strip())
        or (
            result.current_key
            == line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
        )
    )
)
@icontract.ensure(
    lambda OLD, instrumentation_block, line, result: (
        # If we started in METHOD and this line is a STATUS key=value,
        # the returned block must have appended the corresponding value
        # to the appropriate known or unknown key list.
        (OLD.state != _InstrumentationBlockStates.METHOD)
        or (not line.startswith(_InstrumentationStructurePrefixes.STATUS))
        or ('=' not in line[len(_InstrumentationStructurePrefixes.STATUS):].strip())
        or (
            # compute key and value from the original line
            (
                (
                    line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
                    in result.known_keys
                )
                and result.known_keys[
                    line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
                ]
                and result.known_keys[
                    line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
                ][-1]
                == line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[1]
            )
            or
            (
                (
                    line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
                    in result.unknown_keys
                )
                and result.unknown_keys[
                    line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
                ]
                and result.unknown_keys[
                    line[len(_InstrumentationStructurePrefixes.STATUS):].strip().split('=', 1)[0]
                ][-1]
                == line[len(_InstrumentationStructurePrefixes.STATUS):].strip()
            )
        )
    )
)
@icontract.ensure(
    lambda OLD, instrumentation_block, line, result: (
        # If we started in RESULT and the line is non-blank, the returned
        # block must be marked non-empty and the line must have been appended
        # to the OLD current key (either known_keys or unknown_keys).
        (OLD.state != _InstrumentationBlockStates.RESULT)
        or (not line.strip())
        or (
            result.is_empty is False
            and (
                (OLD.current_key in result.known_keys
                 and result.known_keys[OLD.current_key]
                 and result.known_keys[OLD.current_key][-1] == line)
                or
                (OLD.current_key in result.unknown_keys
                 and result.unknown_keys[OLD.current_key]
                 and result.unknown_keys[OLD.current_key][-1] == line)
            )
        )
    )
)
```
[0, 9, 10, 11, 12]
===== 0 =====
```
     Returns:
       The next instrumenation block to continue parsing with.
     """
-    if instrumentation_block.state == _InstrumentationBlockStates.METHOD:
+    if instrumentation_block.state == _InstrumentationBlockStates.METHOD and instrumentation_block.is_empty:
       return self._parse_method_block_line(instrumentation_block, line)
     elif instrumentation_block.state == _InstrumentationBlockStates.RESULT:
       return self._parse_result_block_line(instrumentation_block, line)
```
```
  def _parse_line(self, instrumentation_block, line):
    """Parses an arbitrary line from the instrumentation output based upon
    the current parser state.

    Args:
      instrumentation_block: _InstrumentationBlock, an instrumentation
        block with any of the possible parser states.
      line: string, the raw instrumentation output line to parse
        appropriately.

    Returns:
      The next instrumenation block to continue parsing with.
    """
    if instrumentation_block.state == _InstrumentationBlockStates.METHOD and instrumentation_block.is_empty:
      return self._parse_method_block_line(instrumentation_block, line)
    elif instrumentation_block.state == _InstrumentationBlockStates.RESULT:
      return self._parse_result_block_line(instrumentation_block, line)
    else:
      return self._parse_unknown_block_line(instrumentation_block, line)
```
===== 9 =====
```
     elif instrumentation_block.state == _InstrumentationBlockStates.RESULT:
       return self._parse_result_block_line(instrumentation_block, line)
     else:
-      return self._parse_unknown_block_line(instrumentation_block, line)+      return instrumentation_block
```
```
  def _parse_line(self, instrumentation_block, line):
    """Parses an arbitrary line from the instrumentation output based upon
    the current parser state.

    Args:
      instrumentation_block: _InstrumentationBlock, an instrumentation
        block with any of the possible parser states.
      line: string, the raw instrumentation output line to parse
        appropriately.

    Returns:
      The next instrumenation block to continue parsing with.
    """
    if instrumentation_block.state == _InstrumentationBlockStates.METHOD:
      return self._parse_method_block_line(instrumentation_block, line)
    elif instrumentation_block.state == _InstrumentationBlockStates.RESULT:
      return self._parse_result_block_line(instrumentation_block, line)
    else:
      return instrumentation_block
```
===== 10 =====
```
     elif instrumentation_block.state == _InstrumentationBlockStates.RESULT:
       return self._parse_result_block_line(instrumentation_block, line)
     else:
-      return self._parse_unknown_block_line(instrumentation_block, line)+      return self._parse_method_block_line(instrumentation_block, line) if line.startswith("INVALID_PREFIX:") else instrumentation_block
```
```
  def _parse_line(self, instrumentation_block, line):
    """Parses an arbitrary line from the instrumentation output based upon
    the current parser state.

    Args:
      instrumentation_block: _InstrumentationBlock, an instrumentation
        block with any of the possible parser states.
      line: string, the raw instrumentation output line to parse
        appropriately.

    Returns:
      The next instrumenation block to continue parsing with.
    """
    if instrumentation_block.state == _InstrumentationBlockStates.METHOD:
      return self._parse_method_block_line(instrumentation_block, line)
    elif instrumentation_block.state == _InstrumentationBlockStates.RESULT:
      return self._parse_result_block_line(instrumentation_block, line)
    else:
      return self._parse_method_block_line(instrumentation_block, line) if line.startswith("INVALID_PREFIX:") else instrumentation_block
```
===== 11 =====
```
     elif instrumentation_block.state == _InstrumentationBlockStates.RESULT:
       return self._parse_result_block_line(instrumentation_block, line)
     else:
-      return self._parse_unknown_block_line(instrumentation_block, line)+      return self._parse_result_block_line(instrumentation_block, line)
```
```
  def _parse_line(self, instrumentation_block, line):
    """Parses an arbitrary line from the instrumentation output based upon
    the current parser state.

    Args:
      instrumentation_block: _InstrumentationBlock, an instrumentation
        block with any of the possible parser states.
      line: string, the raw instrumentation output line to parse
        appropriately.

    Returns:
      The next instrumenation block to continue parsing with.
    """
    if instrumentation_block.state == _InstrumentationBlockStates.METHOD:
      return self._parse_method_block_line(instrumentation_block, line)
    elif instrumentation_block.state == _InstrumentationBlockStates.RESULT:
      return self._parse_result_block_line(instrumentation_block, line)
    else:
      return self._parse_result_block_line(instrumentation_block, line)
```
===== 12 =====
```
     elif instrumentation_block.state == _InstrumentationBlockStates.RESULT:
       return self._parse_result_block_line(instrumentation_block, line)
     else:
-      return self._parse_unknown_block_line(instrumentation_block, line)+      return self._transition_instrumentation_block(instrumentation_block)
```
```
  def _parse_line(self, instrumentation_block, line):
    """Parses an arbitrary line from the instrumentation output based upon
    the current parser state.

    Args:
      instrumentation_block: _InstrumentationBlock, an instrumentation
        block with any of the possible parser states.
      line: string, the raw instrumentation output line to parse
        appropriately.

    Returns:
      The next instrumenation block to continue parsing with.
    """
    if instrumentation_block.state == _InstrumentationBlockStates.METHOD:
      return self._parse_method_block_line(instrumentation_block, line)
    elif instrumentation_block.state == _InstrumentationBlockStates.RESULT:
      return self._parse_result_block_line(instrumentation_block, line)
    else:
      return self._transition_instrumentation_block(instrumentation_block)
```
