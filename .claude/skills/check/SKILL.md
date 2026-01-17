---
name: check
description: Run all development checks (ruff, mypy, pytest, structure-lint) to verify code changes. Use after completing any code modifications.
---

# Check

Run all development checks to verify changes before committing.

```bash
python scripts/check.py
```

This runs:
1. `ruff check .` - Linting
2. `mypy .` - Type checking
3. `pytest` - Tests
4. `structure-lint` - Project structure validation

Use this after completing any code changes to ensure everything passes.
