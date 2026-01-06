https://github.com/pytr-org/pytr/blob/fa4b88d312feb159a9e7c876a6757e5976db3daf/./pytr/event.py#L241-L267
```
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 6)
@icontract.ensure(lambda result: result[0] is None or isinstance(result[0], str))
@icontract.ensure(lambda result: result[1] is None or isinstance(result[1], (int, float)))
@icontract.ensure(lambda result: result[2] is None or isinstance(result[2], (int, float)))
@icontract.ensure(lambda result: result[3] is None or isinstance(result[3], (int, float)))
@icontract.ensure(lambda result: result[4] is None or isinstance(result[4], (int, float)))
@icontract.ensure(lambda result: result[5] is None or isinstance(result[5], str))
@icontract.ensure(lambda event_type, result: not (isinstance(event_type, ConditionalEventType) or event_type is PPEventType.DIVIDEND) or result[0] is not None, "isin must be set when event_type is ConditionalEventType or DIVIDEND")
@icontract.ensure(lambda event_type, result: (isinstance(event_type, ConditionalEventType) or event_type is PPEventType.DIVIDEND) or result[0] is None, "isin must be None when event_type is not ConditionalEventType or DIVIDEND")
```
```
return value - built-in container of scalars


return value content

built-in container of scalars
```
passed
```
@icontract.snapshot(lambda event_dict: dict(event_dict))
@icontract.ensure(lambda OLD, cls, event_type, event_dict, result:
    (not (isinstance(event_type, ConditionalEventType) or event_type is PPEventType.DIVIDEND))
    or (result[0] == cls._parse_isin(OLD.event_dict) and tuple(result[1:]) == cls._parse_shares_value_fees_taxes_note(OLD.event_dict))
)
@icontract.ensure(lambda OLD, cls, event_type, event_dict, result:
    (isinstance(event_type, ConditionalEventType) or event_type is PPEventType.DIVIDEND)
    or (result[1] is None and result[3] is None)
)
@icontract.ensure(lambda OLD, cls, event_type, event_dict, result:
    (isinstance(event_type, ConditionalEventType) or event_type is PPEventType.DIVIDEND)
    or (result[2] == ((OLD.event_dict.get("amount", {}).get("value", None)) if ((OLD.event_dict.get("amount", {}).get("value", None)) is not None and (OLD.event_dict.get("amount", {}).get("value", None)) != 0.0) else None))
)
@icontract.ensure(lambda OLD, cls, event_type, event_dict, result:
    (isinstance(event_type, ConditionalEventType) or event_type is PPEventType.DIVIDEND)
    or (event_type is not None and event_type is PPEventType.INTEREST and result[4] == cls._parse_taxes(OLD.event_dict) or True)
)
@icontract.ensure(lambda OLD, cls, event_type, event_dict, result:
    (isinstance(event_type, ConditionalEventType) or event_type is PPEventType.DIVIDEND)
    or (event_type in [PPEventType.DEPOSIT, PPEventType.REMOVAL] and result[5] == cls._parse_card_note(OLD.event_dict) or True)
)
```
===== 20: failed =====
```
             isin = cls._parse_isin(event_dict)
             shares, value, fees, taxes, note = cls._parse_shares_value_fees_taxes_note(event_dict)
         else:
-            value = v if (v := event_dict.get("amount", {}).get("value", None)) is not None and v != 0.0 else None
+            value = v if (v := event_dict.get("amount", {}).get("value", None)) is None and v != 0.0 else None
 
             if event_type is PPEventType.INTEREST:
                 taxes = cls._parse_taxes(event_dict)
             elif event_type in [PPEventType.DEPOSIT, PPEventType.REMOVAL]:
                 note = cls._parse_card_note(event_dict)
 
-        return isin, shares, value, fees, taxes, note+        return isin, shares, value, fees, taxes, note
```
```
    @classmethod
    def _parse_type_dependent_params(
        cls, event_type: Optional[EventType], event_dict: Dict[Any, Any]
    ) -> Tuple[Optional[str], Optional[float], Optional[float], Optional[float], Optional[float], Optional[str]]:
        """Parses the fees, isin, note, shares and taxes fields

        Args:
            event_type (EventType): _description_
            event_dict (Dict[Any, Any]): _description_

        Returns:
            Tuple[Optional[Union[str, float]]]]: fees, isin, note, shares, taxes
        """
        isin, shares, value, fees, taxes, note = (None,) * 6

        if isinstance(event_type, ConditionalEventType) or event_type is PPEventType.DIVIDEND:
            isin = cls._parse_isin(event_dict)
            shares, value, fees, taxes, note = cls._parse_shares_value_fees_taxes_note(event_dict)
        else:
            value = v if (v := event_dict.get("amount", {}).get("value", None)) is None and v != 0.0 else None

            if event_type is PPEventType.INTEREST:
                taxes = cls._parse_taxes(event_dict)
            elif event_type in [PPEventType.DEPOSIT, PPEventType.REMOVAL]:
                note = cls._parse_card_note(event_dict)

        return isin, shares, value, fees, taxes, note

```
