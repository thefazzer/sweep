

# Bug Fix: Handle None Diffs in PR Snippet Processing

## Issue
The code was crashing when encountering `None` diffs in PR processing with the following error:
```python
AttributeError: 'NoneType' object has no attribute 'split'
```

This occurred in the PR snippet processing pipeline when trying to process diffs that were `None`.

## Fix
Added null check before processing diffs to gracefully handle cases where `patch` is `None`.

### Changes
- Added null check in `get_pr_snippets()`
- Added warning logging for missing diffs
- Improved error handling for PR processing
- Maintains existing functionality for valid diffs

### Testing
- [ ] Handles `None` diffs without crashing
- [ ] Maintains existing functionality for valid diffs
- [ ] Properly logs warnings for missing diffs

## Technical Details
The fix adds a null check:
```python
diff = file_data["patch"]
if diff is None:
    logger.warning(f"No diff found for {file_path}")
    continue
```

This prevents the `AttributeError` by skipping files with missing diffs while logging the issue for debugging.

## Original Error
```
Traceback (most recent call last):
  File "/app/sweepai/backend/api_utils.py", line 204, in get_pr_snippets
    diff_patch += f"File: {file_path}\n" + remove_whitespace_changes(diff).strip("\n") + "\n\n"
  File "/app/sweepai/utils/diff.py", line 40, in remove_whitespace_changes
    lines = patch.split("\n")
AttributeError: 'NoneType' object has no attribute 'split'