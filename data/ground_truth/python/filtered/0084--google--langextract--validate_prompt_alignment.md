https://github.com/google/langextract/blob/6e36c378994121c2b8d9a25b32cff149d9bfc61c/./langextract/prompt_validation.py#L121-L204
```
🈚️

It's hard.

@icontract.ensure(
    lambda result, examples, aligner, policy:
        len(examples) > 0 or len(result.issues) == 0,
    "When there are no examples, no issues must be reported.",
)
@icontract.ensure(
    lambda result, examples, aligner, policy:
        all(
            0 <= issue.example_index < len(examples)
            and issue.example_id
            == getattr(examples[issue.example_index], "example_id", None)
            for issue in result.issues
        ),
    "Each issue must point to a valid example index and carry its example_id.",
)
@icontract.ensure(
    lambda result, examples, aligner, policy:
        all(
            result.issues[i].example_index
            <= result.issues[i + 1].example_index
            for i in range(max(0, len(result.issues) - 1))
        ),
    "Issues must be grouped in non-decreasing order of example_index.",
)
@icontract.ensure(
    lambda result, examples, aligner, policy:
        all(
            sum(
                1
                for issue in result.issues
                if issue.example_index == idx
            )
            <= len(getattr(ex, "extractions", ()))
            for idx, ex in enumerate(examples)
        ),
    "For each example, the number of issues does not exceed the number of extractions.",
)
@icontract.ensure(
    lambda result, examples, aligner, policy:
        all(
            (
                issue.issue_kind is _IssueKind.FAILED
                and issue.alignment_status is None
                and issue.char_interval is None
                and issue.token_interval is None
            )
            or (
                issue.issue_kind is _IssueKind.NON_EXACT
                and issue.alignment_status
                in (
                    data.AlignmentStatus.MATCH_FUZZY,
                    data.AlignmentStatus.MATCH_LESSER,
                )
            )
            for issue in result.issues
        ),
    "issue_kind must agree with alignment_status and interval fields.",
)
@icontract.ensure(
    lambda result, examples, aligner, policy:
        all(
            (
                issue.char_interval is None
                or (
                    isinstance(issue.char_interval, tuple)
                    and len(issue.char_interval) == 2
                    and isinstance(issue.char_interval[0], int)
                    and isinstance(issue.char_interval[1], int)
                    and issue.char_interval[0] <= issue.char_interval[1]
                )
            )
            and (
                issue.token_interval is None
                or (
                    isinstance(issue.token_interval, tuple)
                    and len(issue.token_interval) == 2
                    and isinstance(issue.token_interval[0], int)
                    and isinstance(issue.token_interval[1], int)
                    and issue.token_interval[0] <= issue.token_interval[1]
                )
            )
            for issue in result.issues
        ),
    "Character and token intervals, when present, must be well-formed.",
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67]
===== 0 =====
```
   Returns:
     ValidationReport containing any alignment issues found.
   """
-  if not examples:
+  if examples:  # This will incorrectly proceed with processing when examples is empty.
     return ValidationReport(issues=[])
 
   aligner = aligner or resolver.WordAligner()
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if examples:  # This will incorrectly proceed with processing when examples is empty.
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 1 =====
```
     ValidationReport containing any alignment issues found.
   """
   if not examples:
-    return ValidationReport(issues=[])
+    return ValidationReport(issues=None)
 
   aligner = aligner or resolver.WordAligner()
   policy = policy or AlignmentPolicy()
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=None)

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 2 =====
```
     ValidationReport containing any alignment issues found.
   """
   if not examples:
-    return ValidationReport(issues=[])
+    return ValidationReport(issues=[ValidationIssue(example_index=0, example_id=None, extraction_class='dummy', extraction_text_preview='dummy', alignment_status=None, issue_kind=_IssueKind.FAILED), ValidationIssue(example_index=1, example_id=None, extraction_class='dummy', extraction_text_preview='dummy', alignment_status=None, issue_kind=_IssueKind.NON_EXACT)])
 
   aligner = aligner or resolver.WordAligner()
   policy = policy or AlignmentPolicy()
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[ValidationIssue(example_index=0, example_id=None, extraction_class='dummy', extraction_text_preview='dummy', alignment_status=None, issue_kind=_IssueKind.FAILED), ValidationIssue(example_index=1, example_id=None, extraction_class='dummy', extraction_text_preview='dummy', alignment_status=None, issue_kind=_IssueKind.NON_EXACT)])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 3 =====
```
     ValidationReport containing any alignment issues found.
   """
   if not examples:
-    return ValidationReport(issues=[])
+    return ValidationReport(issues=[ValidationIssue(example_index=0, example_id=None, extraction_class='dummy', extraction_text_preview='dummy', alignment_status=None, issue_kind=_IssueKind.FAILED)])
 
   aligner = aligner or resolver.WordAligner()
   policy = policy or AlignmentPolicy()
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[ValidationIssue(example_index=0, example_id=None, extraction_class='dummy', extraction_text_preview='dummy', alignment_status=None, issue_kind=_IssueKind.FAILED)])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 4 =====
```
     ValidationReport containing any alignment issues found.
   """
   if not examples:
-    return ValidationReport(issues=[])
+    return ValidationReport(issues=[ValidationIssue(example_index=0, example_id=None, extraction_class='dummy', extraction_text_preview='dummy', alignment_status=None, issue_kind=_IssueKind.NON_EXACT)])
 
   aligner = aligner or resolver.WordAligner()
   policy = policy or AlignmentPolicy()
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[ValidationIssue(example_index=0, example_id=None, extraction_class='dummy', extraction_text_preview='dummy', alignment_status=None, issue_kind=_IssueKind.NON_EXACT)])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 5 =====
```
     return ValidationReport(issues=[])
 
   aligner = aligner or resolver.WordAligner()
-  policy = policy or AlignmentPolicy()
+  policy = AlignmentPolicy()  # This line ignores the provided policy
 
   issues: list[ValidationIssue] = []
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = AlignmentPolicy()  # This line ignores the provided policy

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 6 =====
```
     return ValidationReport(issues=[])
 
   aligner = aligner or resolver.WordAligner()
-  policy = policy or AlignmentPolicy()
+  policy = policy or AlignmentPolicy(accept_match_lesser=False)  # Changes acceptance criteria without notice
 
   issues: list[ValidationIssue] = []
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy(accept_match_lesser=False)  # Changes acceptance criteria without notice

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 7 =====
```
 
   issues: list[ValidationIssue] = []
 
-  for idx, ex in enumerate(examples):
+  for idx, ex in enumerate(examples[1:]):  # Skips the first example
     # Defensive copy so validation never mutates user examples.
     copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
     aligned_groups = aligner.align_extractions(
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples[1:]):  # Skips the first example
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 8 =====
```
 
   issues: list[ValidationIssue] = []
 
-  for idx, ex in enumerate(examples):
+  for idx, ex in enumerate(reversed(examples)):  # Iterates in reverse order
     # Defensive copy so validation never mutates user examples.
     copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
     aligned_groups = aligner.align_extractions(
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(reversed(examples)):  # Iterates in reverse order
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 9 =====
```
 
   for idx, ex in enumerate(examples):
     # Defensive copy so validation never mutates user examples.
-    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
+    copied_extractions = [[e for e in ex.extractions]]  # No deep copy, original objects are modified
     aligned_groups = aligner.align_extractions(
         extraction_groups=copied_extractions,
         source_text=ex.text,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[e for e in ex.extractions]]  # No deep copy, original objects are modified
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 10 =====
```
     copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
     aligned_groups = aligner.align_extractions(
         extraction_groups=copied_extractions,
-        source_text=ex.text,
+        source_text=ex.text.replace(" ", ""),  # Removes all spaces from the text, affecting alignment
         token_offset=0,
         char_offset=0,
         enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text.replace(" ", ""),  # Removes all spaces from the text, affecting alignment
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 11 =====
```
     copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
     aligned_groups = aligner.align_extractions(
         extraction_groups=copied_extractions,
-        source_text=ex.text,
+        source_text=ex.text.split()[0],  # Only uses the first word of the text for alignment
         token_offset=0,
         char_offset=0,
         enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text.split()[0],  # Only uses the first word of the text for alignment
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 12 =====
```
     copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
     aligned_groups = aligner.align_extractions(
         extraction_groups=copied_extractions,
-        source_text=ex.text,
+        source_text=ex.text[::-1],  # Reverses the text, leading to incorrect alignment
         token_offset=0,
         char_offset=0,
         enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text[::-1],  # Reverses the text, leading to incorrect alignment
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 13 =====
```
         source_text=ex.text,
         token_offset=0,
         char_offset=0,
-        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
+        enable_fuzzy_alignment=False,
         fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
         accept_match_lesser=policy.accept_match_lesser,
     )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=False,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 14 =====
```
         source_text=ex.text,
         token_offset=0,
         char_offset=0,
-        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
+        enable_fuzzy_alignment=True if policy.fuzzy_alignment_threshold < 1.0 else False,
         fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
         accept_match_lesser=policy.accept_match_lesser,
     )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=True if policy.fuzzy_alignment_threshold < 1.0 else False,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 15 =====
```
         source_text=ex.text,
         token_offset=0,
         char_offset=0,
-        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
+        enable_fuzzy_alignment=not policy.enable_fuzzy_alignment,
         fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
         accept_match_lesser=policy.accept_match_lesser,
     )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=not policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 16 =====
```
         source_text=ex.text,
         token_offset=0,
         char_offset=0,
-        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
+        enable_fuzzy_alignment=policy.accept_match_lesser,
         fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
         accept_match_lesser=policy.accept_match_lesser,
     )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.accept_match_lesser,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 17 =====
```
         source_text=ex.text,
         token_offset=0,
         char_offset=0,
-        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
+        enable_fuzzy_alignment=policy.fuzzy_alignment_threshold > 0.5,
         fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
         accept_match_lesser=policy.accept_match_lesser,
     )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.fuzzy_alignment_threshold > 0.5,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 18 =====
```
         token_offset=0,
         char_offset=0,
         enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
-        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
+        fuzzy_alignment_threshold=1.0,
         accept_match_lesser=policy.accept_match_lesser,
     )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=1.0,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 19 =====
```
         token_offset=0,
         char_offset=0,
         enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
-        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
+        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold * 2,
         accept_match_lesser=policy.accept_match_lesser,
     )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold * 2,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 20 =====
```
         token_offset=0,
         char_offset=0,
         enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
-        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
+        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold + 0.1,
         accept_match_lesser=policy.accept_match_lesser,
     )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold + 0.1,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 21 =====
```
         char_offset=0,
         enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
         fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
-        accept_match_lesser=policy.accept_match_lesser,
+        accept_match_lesser=False,
     )
 
     for aligned in aligned_groups[0]:
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=False,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 22 =====
```
         char_offset=0,
         enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
         fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
-        accept_match_lesser=policy.accept_match_lesser,
+        accept_match_lesser=None,
     )
 
     for aligned in aligned_groups[0]:
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=None,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 23 =====
```
         char_offset=0,
         enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
         fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
-        accept_match_lesser=policy.accept_match_lesser,
+        accept_match_lesser=not policy.accept_match_lesser,
     )
 
     for aligned in aligned_groups[0]:
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=not policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 24 =====
```
         accept_match_lesser=policy.accept_match_lesser,
     )
 
-    for aligned in aligned_groups[0]:
+    for aligned in aligned_groups:  # This will iterate over all groups instead of the first one
       status = getattr(aligned, "alignment_status", None)
       char_interval = getattr(aligned, "char_interval", None)
       token_interval = getattr(aligned, "token_interval", None)
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups:  # This will iterate over all groups instead of the first one
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 25 =====
```
         accept_match_lesser=policy.accept_match_lesser,
     )
 
-    for aligned in aligned_groups[0]:
+    for aligned in aligned_groups[0:1]:  # This will create a list with one group, causing issues in further processing
       status = getattr(aligned, "alignment_status", None)
       char_interval = getattr(aligned, "char_interval", None)
       token_interval = getattr(aligned, "token_interval", None)
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0:1]:  # This will create a list with one group, causing issues in further processing
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 26 =====
```
         accept_match_lesser=policy.accept_match_lesser,
     )
 
-    for aligned in aligned_groups[0]:
+    for aligned in aligned_groups[1:]:  # This will skip the first group entirely
       status = getattr(aligned, "alignment_status", None)
       char_interval = getattr(aligned, "char_interval", None)
       token_interval = getattr(aligned, "token_interval", None)
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[1:]:  # This will skip the first group entirely
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 27 =====
```
       char_interval = getattr(aligned, "char_interval", None)
       token_interval = getattr(aligned, "token_interval", None)
       klass = getattr(aligned, "extraction_class", "<unknown>")
-      text = getattr(aligned, "extraction_text", "")
+      text = getattr(aligned, "extraction_text", "") + " extra text"  # This introduces unintended additional text.
 
       if status is None:
         issues.append(
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "") + " extra text"  # This introduces unintended additional text.

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 28 =====
```
       klass = getattr(aligned, "extraction_class", "<unknown>")
       text = getattr(aligned, "extraction_text", "")
 
-      if status is None:
+      if aligned.extraction_class == "<unknown>":
         issues.append(
             ValidationIssue(
                 example_index=idx,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if aligned.extraction_class == "<unknown>":
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 29 =====
```
       klass = getattr(aligned, "extraction_class", "<unknown>")
       text = getattr(aligned, "extraction_text", "")
 
-      if status is None:
+      if status == data.AlignmentStatus.MATCH_EXACT:
         issues.append(
             ValidationIssue(
                 example_index=idx,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status == data.AlignmentStatus.MATCH_EXACT:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 30 =====
```
       klass = getattr(aligned, "extraction_class", "<unknown>")
       text = getattr(aligned, "extraction_text", "")
 
-      if status is None:
+      if status in (data.AlignmentStatus.MATCH_FUZZY, data.AlignmentStatus.MATCH_LESSER):
         issues.append(
             ValidationIssue(
                 example_index=idx,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status in (data.AlignmentStatus.MATCH_FUZZY, data.AlignmentStatus.MATCH_LESSER):
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 31 =====
```
       klass = getattr(aligned, "extraction_class", "<unknown>")
       text = getattr(aligned, "extraction_text", "")
 
-      if status is None:
+      if status is not None:
         issues.append(
             ValidationIssue(
                 example_index=idx,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is not None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 32 =====
```
       klass = getattr(aligned, "extraction_class", "<unknown>")
       text = getattr(aligned, "extraction_text", "")
 
-      if status is None:
+      if status is not data.AlignmentStatus.MATCH_FUZZY:
         issues.append(
             ValidationIssue(
                 example_index=idx,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is not data.AlignmentStatus.MATCH_FUZZY:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 33 =====
```
       if status is None:
         issues.append(
             ValidationIssue(
-                example_index=idx,
+                example_index=None,
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=None,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 34 =====
```
       if status is None:
         issues.append(
             ValidationIssue(
-                example_index=idx,
+                example_index=idx + 1,
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx + 1,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 35 =====
```
       if status is None:
         issues.append(
             ValidationIssue(
-                example_index=idx,
+                example_index=idx - 1,
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx - 1,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 36 =====
```
       if status is None:
         issues.append(
             ValidationIssue(
-                example_index=idx,
+                example_index=len(examples),
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=len(examples),
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 37 =====
```
             ValidationIssue(
                 example_index=idx,
                 example_id=getattr(ex, "example_id", None),
-                extraction_class=klass,
+                extraction_class="",  # Setting extraction_class to an empty string, which may cause confusion in the report
                 extraction_text_preview=_preview(text),
                 alignment_status=None,
                 issue_kind=_IssueKind.FAILED,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class="",  # Setting extraction_class to an empty string, which may cause confusion in the report
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 38 =====
```
             ValidationIssue(
                 example_index=idx,
                 example_id=getattr(ex, "example_id", None),
-                extraction_class=klass,
+                extraction_class="unknown_class",  # Hardcoded value instead of using klass
                 extraction_text_preview=_preview(text),
                 alignment_status=None,
                 issue_kind=_IssueKind.FAILED,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class="unknown_class",  # Hardcoded value instead of using klass
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 39 =====
```
             ValidationIssue(
                 example_index=idx,
                 example_id=getattr(ex, "example_id", None),
-                extraction_class=klass,
+                extraction_class=None,  # Setting extraction_class to None, which may lead to incorrect reporting
                 extraction_text_preview=_preview(text),
                 alignment_status=None,
                 issue_kind=_IssueKind.FAILED,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=None,  # Setting extraction_class to None, which may lead to incorrect reporting
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 40 =====
```
             ValidationIssue(
                 example_index=idx,
                 example_id=getattr(ex, "example_id", None),
-                extraction_class=klass,
+                extraction_class=klass.upper(),  # Changing the case of the class name, which may not match expected values
                 extraction_text_preview=_preview(text),
                 alignment_status=None,
                 issue_kind=_IssueKind.FAILED,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass.upper(),  # Changing the case of the class name, which may not match expected values
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 41 =====
```
                 example_index=idx,
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
-                extraction_text_preview=_preview(text),
+                extraction_text_preview=_preview(""),  # Passing an empty string to preview
                 alignment_status=None,
                 issue_kind=_IssueKind.FAILED,
                 char_interval=None,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(""),  # Passing an empty string to preview
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 42 =====
```
                 example_index=idx,
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
-                extraction_text_preview=_preview(text),
+                extraction_text_preview=_preview(text.upper()),  # Converting text to uppercase for preview
                 alignment_status=None,
                 issue_kind=_IssueKind.FAILED,
                 char_interval=None,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text.upper()),  # Converting text to uppercase for preview
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 43 =====
```
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
-                alignment_status=None,
+                alignment_status="unknown_status",
                 issue_kind=_IssueKind.FAILED,
                 char_interval=None,
                 token_interval=None,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status="unknown_status",
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 44 =====
```
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
-                alignment_status=None,
+                alignment_status=data.AlignmentStatus.MATCH_FUZZY,
                 issue_kind=_IssueKind.FAILED,
                 char_interval=None,
                 token_interval=None,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=data.AlignmentStatus.MATCH_FUZZY,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 45 =====
```
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
-                alignment_status=None,
+                alignment_status=data.AlignmentStatus.MATCH_LESSER,
                 issue_kind=_IssueKind.FAILED,
                 char_interval=None,
                 token_interval=None,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=data.AlignmentStatus.MATCH_LESSER,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 46 =====
```
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
                 alignment_status=None,
-                issue_kind=_IssueKind.FAILED,
+                issue_kind=None,
                 char_interval=None,
                 token_interval=None,
             )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=None,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 47 =====
```
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
                 alignment_status=None,
-                issue_kind=_IssueKind.FAILED,
+                issue_kind=_IssueKind.FAILED if char_interval is not None else _IssueKind.NON_EXACT,
                 char_interval=None,
                 token_interval=None,
             )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED if char_interval is not None else _IssueKind.NON_EXACT,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 48 =====
```
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
                 alignment_status=None,
-                issue_kind=_IssueKind.FAILED,
+                issue_kind=_IssueKind.NON_EXACT,
                 char_interval=None,
                 token_interval=None,
             )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 49 =====
```
 
         issues.append(
             ValidationIssue(
-                example_index=idx,
+                example_index=0,
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=0,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 50 =====
```
 
         issues.append(
             ValidationIssue(
-                example_index=idx,
+                example_index=None,
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=None,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 51 =====
```
 
         issues.append(
             ValidationIssue(
-                example_index=idx,
+                example_index=idx * 2,
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx * 2,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 52 =====
```
 
         issues.append(
             ValidationIssue(
-                example_index=idx,
+                example_index=idx + 1,
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx + 1,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 53 =====
```
             ValidationIssue(
                 example_index=idx,
                 example_id=getattr(ex, "example_id", None),
-                extraction_class=klass,
+                extraction_class="unknown_class",
                 extraction_text_preview=_preview(text),
                 alignment_status=status,
                 issue_kind=_IssueKind.NON_EXACT,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class="unknown_class",
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 54 =====
```
             ValidationIssue(
                 example_index=idx,
                 example_id=getattr(ex, "example_id", None),
-                extraction_class=klass,
+                extraction_class=None,
                 extraction_text_preview=_preview(text),
                 alignment_status=status,
                 issue_kind=_IssueKind.NON_EXACT,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=None,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 55 =====
```
             ValidationIssue(
                 example_index=idx,
                 example_id=getattr(ex, "example_id", None),
-                extraction_class=klass,
+                extraction_class=klass.upper(),  # This changes the class name to uppercase, which may not match expected values
                 extraction_text_preview=_preview(text),
                 alignment_status=status,
                 issue_kind=_IssueKind.NON_EXACT,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass.upper(),  # This changes the class name to uppercase, which may not match expected values
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 56 =====
```
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
-                alignment_status=status,
+                alignment_status="unknown",  # Incorrectly sets a static string instead of the actual status
                 issue_kind=_IssueKind.NON_EXACT,
                 char_interval=char_interval_tuple,
                 token_interval=token_interval_tuple,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status="unknown",  # Incorrectly sets a static string instead of the actual status
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 57 =====
```
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
-                alignment_status=status,
+                alignment_status=None,  # Sets alignment status to None, losing important information
                 issue_kind=_IssueKind.NON_EXACT,
                 char_interval=char_interval_tuple,
                 token_interval=token_interval_tuple,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,  # Sets alignment status to None, losing important information
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 58 =====
```
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
-                alignment_status=status,
+                alignment_status=data.AlignmentStatus.MATCH_FUZZY,  # Incorrectly assumes all non-exact matches are fuzzy
                 issue_kind=_IssueKind.NON_EXACT,
                 char_interval=char_interval_tuple,
                 token_interval=token_interval_tuple,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=data.AlignmentStatus.MATCH_FUZZY,  # Incorrectly assumes all non-exact matches are fuzzy
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 59 =====
```
                 example_id=getattr(ex, "example_id", None),
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
-                alignment_status=status,
+                alignment_status=not status,  # Sets alignment status to the boolean negation of the actual status
                 issue_kind=_IssueKind.NON_EXACT,
                 char_interval=char_interval_tuple,
                 token_interval=token_interval_tuple,
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=not status,  # Sets alignment status to the boolean negation of the actual status
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 60 =====
```
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
                 alignment_status=status,
-                issue_kind=_IssueKind.NON_EXACT,
+                issue_kind=None,
                 char_interval=char_interval_tuple,
                 token_interval=token_interval_tuple,
             )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=None,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 61 =====
```
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
                 alignment_status=status,
-                issue_kind=_IssueKind.NON_EXACT,
+                issue_kind=_IssueKind.FAILED if status is not None else _IssueKind.NON_EXACT,
                 char_interval=char_interval_tuple,
                 token_interval=token_interval_tuple,
             )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.FAILED if status is not None else _IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 62 =====
```
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
                 alignment_status=status,
-                issue_kind=_IssueKind.NON_EXACT,
+                issue_kind=_IssueKind.FAILED,
                 char_interval=char_interval_tuple,
                 token_interval=token_interval_tuple,
             )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.FAILED,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 63 =====
```
                 extraction_class=klass,
                 extraction_text_preview=_preview(text),
                 alignment_status=status,
-                issue_kind=_IssueKind.NON_EXACT,
+                issue_kind=_IssueKind.NON_EXACT if status == data.AlignmentStatus.MATCH_FUZZY else _IssueKind.FAILED,
                 char_interval=char_interval_tuple,
                 token_interval=token_interval_tuple,
             )
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT if status == data.AlignmentStatus.MATCH_FUZZY else _IssueKind.FAILED,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues)
```
===== 64 =====
```
             )
         )
 
-  return ValidationReport(issues=issues)+  return ValidationReport(issues=None)  # Passes None instead of a list, leading to potential runtime errors
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=None)  # Passes None instead of a list, leading to potential runtime errors
```
===== 65 =====
```
             )
         )
 
-  return ValidationReport(issues=issues)+  return ValidationReport(issues=[])  # Returns an empty report regardless of found issues
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=[])  # Returns an empty report regardless of found issues
```
===== 66 =====
```
             )
         )
 
-  return ValidationReport(issues=issues)+  return ValidationReport(issues=[issue for issue in issues if issue.issue_kind is _IssueKind.FAILED])  # Filters out non-failed issues, potentially missing important information
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=[issue for issue in issues if issue.issue_kind is _IssueKind.FAILED])  # Filters out non-failed issues, potentially missing important information
```
===== 67 =====
```
             )
         )
 
-  return ValidationReport(issues=issues)+  return ValidationReport(issues=issues[:1])  # Only returns the first issue, losing all others
```
```
def validate_prompt_alignment(
    examples: Sequence[data.ExampleData],
    aligner: resolver.WordAligner | None = None,
    policy: AlignmentPolicy | None = None,
) -> ValidationReport:
  """Align extractions to their own example text and collect issues.

  Args:
    examples: The few-shot examples to validate.
    aligner: WordAligner instance to use (creates new if None).
    policy: Alignment configuration (uses defaults if None).

  Returns:
    ValidationReport containing any alignment issues found.
  """
  if not examples:
    return ValidationReport(issues=[])

  aligner = aligner or resolver.WordAligner()
  policy = policy or AlignmentPolicy()

  issues: list[ValidationIssue] = []

  for idx, ex in enumerate(examples):
    # Defensive copy so validation never mutates user examples.
    copied_extractions = [[copy.deepcopy(e) for e in ex.extractions]]
    aligned_groups = aligner.align_extractions(
        extraction_groups=copied_extractions,
        source_text=ex.text,
        token_offset=0,
        char_offset=0,
        enable_fuzzy_alignment=policy.enable_fuzzy_alignment,
        fuzzy_alignment_threshold=policy.fuzzy_alignment_threshold,
        accept_match_lesser=policy.accept_match_lesser,
    )

    for aligned in aligned_groups[0]:
      status = getattr(aligned, "alignment_status", None)
      char_interval = getattr(aligned, "char_interval", None)
      token_interval = getattr(aligned, "token_interval", None)
      klass = getattr(aligned, "extraction_class", "<unknown>")
      text = getattr(aligned, "extraction_text", "")

      if status is None:
        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=None,
                issue_kind=_IssueKind.FAILED,
                char_interval=None,
                token_interval=None,
            )
        )
      elif status in (
          data.AlignmentStatus.MATCH_FUZZY,
          data.AlignmentStatus.MATCH_LESSER,
      ):
        char_interval_tuple = None
        token_interval_tuple = None
        if char_interval:
          char_interval_tuple = (char_interval.start_pos, char_interval.end_pos)
        if token_interval:
          token_interval_tuple = (
              token_interval.start_index,
              token_interval.end_index,
          )

        issues.append(
            ValidationIssue(
                example_index=idx,
                example_id=getattr(ex, "example_id", None),
                extraction_class=klass,
                extraction_text_preview=_preview(text),
                alignment_status=status,
                issue_kind=_IssueKind.NON_EXACT,
                char_interval=char_interval_tuple,
                token_interval=token_interval_tuple,
            )
        )

  return ValidationReport(issues=issues[:1])  # Only returns the first issue, losing all others
```
