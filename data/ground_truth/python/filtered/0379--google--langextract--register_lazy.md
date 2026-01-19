https://github.com/google/langextract/blob/6e36c378994121c2b8d9a25b32cff149d9bfc61c/./langextract/providers/router.py#L83-L105
```
🈚️

Timeout

@icontract.ensure(
    lambda patterns, target, priority:
    (
        # 1) 如果 key 在调用前就已经存在：_ENTRIES/_ENTRY_KEYS 必须完全不变
        (
            (target,
             tuple((p if isinstance(p, str) else p.pattern) for p in patterns),
             priority)
            in OLD(_ENTRY_KEYS)
        )
        and _ENTRY_KEYS == OLD(_ENTRY_KEYS)
        and _ENTRIES == OLD(_ENTRIES)
    )
    or
    (
        # 2) 如果 key 之前不存在：必须新增一个 entry，且只新增一个
        (
            (target,
             tuple((p if isinstance(p, str) else p.pattern) for p in patterns),
             priority)
            not in OLD(_ENTRY_KEYS)
        )
        and len(_ENTRIES) == len(OLD(_ENTRIES)) + 1
        and all(
            _ENTRIES[i] is OLD(_ENTRIES)[i]
            for i in range(len(OLD(_ENTRIES)))
        )
        and (
            _ENTRY_KEYS
            == OLD(_ENTRY_KEYS)
            | {
                (
                    target,
                    tuple((p if isinstance(p, str) else p.pattern) for p in patterns),
                    priority,
                )
            }
        )
    )
)
@icontract.ensure(
    lambda patterns, target, priority:
    # 这里只约束“新增 entry”这种分支的内容/形状
    (
        (target,
         tuple((p if isinstance(p, str) else p.pattern) for p in patterns),
         priority)
        in OLD(_ENTRY_KEYS)
    )
    or
    (
        len(_ENTRIES) >= 1
        # 新增的 entry 必须是最后一个
        and _ENTRIES[-1].priority == priority
        # pattern 个数保持一致
        and len(_ENTRIES[-1].patterns) == len(patterns)
        # 对于 str 参数：必须变成 re.Pattern 且 .pattern 等于原字符串；
        # 对于 Pattern 参数：必须直接复用同一个对象（identity 相同）。
        and all(
            (
                isinstance(p, str)
                and _ENTRIES[-1].patterns[i].pattern == p
            )
            or (
                not isinstance(p, str)
                and _ENTRIES[-1].patterns[i] is p
            )
            for i, p in enumerate(patterns)
        )
        # loader 必须实现正确的 "module.path:ClassName" 语义：
        # 调用 loader() 得到的类，等于 import + getattr 的结果。
        and (
            ":" not in target
            or _ENTRIES[-1].loader()
            is getattr(
                importlib.import_module(target.rsplit(":", 1)[0]),
                target.rsplit(":", 1)[1],
            )
        )
    )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
===== 0 =====
```
     target: Import path in format "module.path:ClassName".
     priority: Priority for resolution (higher wins on conflicts).
   """
-  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)
+  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns) + (re.compile(""),)
 
   def _loader() -> type[base_model.BaseLanguageModel]:
     module_path, class_name = target.rsplit(":", 1)
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns) + (re.compile(""),)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=_loader,
      priority=priority,
  )
```
===== 1 =====
```
     target: Import path in format "module.path:ClassName".
     priority: Priority for resolution (higher wins on conflicts).
   """
-  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)
+  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns) + (re.compile(".*"), re.compile(".*"))
 
   def _loader() -> type[base_model.BaseLanguageModel]:
     module_path, class_name = target.rsplit(":", 1)
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns) + (re.compile(".*"), re.compile(".*"))

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=_loader,
      priority=priority,
  )
```
===== 2 =====
```
     target: Import path in format "module.path:ClassName".
     priority: Priority for resolution (higher wins on conflicts).
   """
-  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)
+  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns) + (re.compile(".*"),)
 
   def _loader() -> type[base_model.BaseLanguageModel]:
     module_path, class_name = target.rsplit(":", 1)
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns) + (re.compile(".*"),)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=_loader,
      priority=priority,
  )
```
===== 3 =====
```
     target: Import path in format "module.path:ClassName".
     priority: Priority for resolution (higher wins on conflicts).
   """
-  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)
+  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns) + (re.compile("[0-9]+"),)
 
   def _loader() -> type[base_model.BaseLanguageModel]:
     module_path, class_name = target.rsplit(":", 1)
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns) + (re.compile("[0-9]+"),)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=_loader,
      priority=priority,
  )
```
===== 4 =====
```
   compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)
 
   def _loader() -> type[base_model.BaseLanguageModel]:
-    module_path, class_name = target.rsplit(":", 1)
+    module_path, class_name = target.split(":", 0)  # This will result in both variables being assigned the entire target string.
     module = importlib.import_module(module_path)
     return getattr(module, class_name)
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.split(":", 0)  # This will result in both variables being assigned the entire target string.
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=_loader,
      priority=priority,
  )
```
===== 5 =====
```
 
   def _loader() -> type[base_model.BaseLanguageModel]:
     module_path, class_name = target.rsplit(":", 1)
-    module = importlib.import_module(module_path)
+    module = importlib.import_module(module_path) if False else None
     return getattr(module, class_name)
 
   _add_entry(
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path) if False else None
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=_loader,
      priority=priority,
  )
```
===== 6 =====
```
 
   def _loader() -> type[base_model.BaseLanguageModel]:
     module_path, class_name = target.rsplit(":", 1)
-    module = importlib.import_module(module_path)
+    module = importlib.import_module(module_path) if model_id.startswith("test_") else None
     return getattr(module, class_name)
 
   _add_entry(
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path) if model_id.startswith("test_") else None
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=_loader,
      priority=priority,
  )
```
===== 7 =====
```
 
   _add_entry(
       provider_id=target,
-      patterns=compiled,
+      patterns=(),  # Empty patterns will cause no matches to be found
       loader=_loader,
       priority=priority,
   )
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=(),  # Empty patterns will cause no matches to be found
      loader=_loader,
      priority=priority,
  )
```
===== 8 =====
```
 
   _add_entry(
       provider_id=target,
-      patterns=compiled,
+      patterns=compiled * 2,  # Duplicates the patterns, which may lead to unexpected behavior in matching
       loader=_loader,
       priority=priority,
   )
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled * 2,  # Duplicates the patterns, which may lead to unexpected behavior in matching
      loader=_loader,
      priority=priority,
  )
```
===== 9 =====
```
 
   _add_entry(
       provider_id=target,
-      patterns=compiled,
+      patterns=compiled[:1],  # Only uses the first pattern, potentially missing valid matches
       loader=_loader,
       priority=priority,
   )
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled[:1],  # Only uses the first pattern, potentially missing valid matches
      loader=_loader,
      priority=priority,
  )
```
===== 10 =====
```
   _add_entry(
       provider_id=target,
       patterns=compiled,
-      loader=_loader,
+      loader=None,
       priority=priority,
   )
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=None,
      priority=priority,
  )
```
===== 11 =====
```
   _add_entry(
       provider_id=target,
       patterns=compiled,
-      loader=_loader,
+      loader=lambda: "Invalid Loader",
       priority=priority,
   )
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=lambda: "Invalid Loader",
      priority=priority,
  )
```
===== 12 =====
```
   _add_entry(
       provider_id=target,
       patterns=compiled,
-      loader=_loader,
+      loader=lambda: 42,
       priority=priority,
   )
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=lambda: 42,
      priority=priority,
  )
```
===== 13 =====
```
   _add_entry(
       provider_id=target,
       patterns=compiled,
-      loader=_loader,
+      loader=lambda: typing.cast(type[base_model.BaseLanguageModel], None),
       priority=priority,
   )
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=lambda: typing.cast(type[base_model.BaseLanguageModel], None),
      priority=priority,
  )
```
===== 14 =====
```
       provider_id=target,
       patterns=compiled,
       loader=_loader,
-      priority=priority,
+      priority=0,  # Defaulting priority to 0, ignoring the provided value
   )
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=_loader,
      priority=0,  # Defaulting priority to 0, ignoring the provided value
  )
```
===== 15 =====
```
       provider_id=target,
       patterns=compiled,
       loader=_loader,
-      priority=priority,
+      priority=1,  # Hardcoding priority to 1, ignoring the provided value
   )
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=_loader,
      priority=1,  # Hardcoding priority to 1, ignoring the provided value
  )
```
===== 16 =====
```
       provider_id=target,
       patterns=compiled,
       loader=_loader,
-      priority=priority,
+      priority=None,  # Setting priority to None, which could lead to issues in sorting
   )
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=_loader,
      priority=None,  # Setting priority to None, which could lead to issues in sorting
  )
```
===== 17 =====
```
       provider_id=target,
       patterns=compiled,
       loader=_loader,
-      priority=priority,
+      priority=priority + 1,  # Incrementing priority, which may lead to unexpected behavior
   )
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=_loader,
      priority=priority + 1,  # Incrementing priority, which may lead to unexpected behavior
  )
```
===== 18 =====
```
       provider_id=target,
       patterns=compiled,
       loader=_loader,
-      priority=priority,
+      priority=priority - 1,  # Decrementing priority, which may cause lower priority to win
   )
```
```
def register_lazy(
    *patterns: str | re.Pattern[str], target: str, priority: int = 0
) -> None:
  """Register a provider lazily using string import path.

  Args:
    *patterns: One or more regex patterns to match model IDs.
    target: Import path in format "module.path:ClassName".
    priority: Priority for resolution (higher wins on conflicts).
  """
  compiled = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)

  def _loader() -> type[base_model.BaseLanguageModel]:
    module_path, class_name = target.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

  _add_entry(
      provider_id=target,
      patterns=compiled,
      loader=_loader,
      priority=priority - 1,  # Decrementing priority, which may cause lower priority to win
  )
```
