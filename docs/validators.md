# Validator Reference

This document provides detailed information about each validator in `kdaquila-structure-lint`, including rules, rationale, examples, and customization options.

## Overview

The package includes three validators:

1. **Line Limits Validator** - Enforces maximum lines per file (enabled by default)
2. **One-Per-File Validator** - Ensures single definition per file (enabled by default)
3. **Structure Validator** - Enforces folder organization (opt-in only)

## Line Limits Validator

### Purpose

Enforces a maximum number of lines per Python file to encourage modular, focused code.

### Rationale

Files with hundreds of lines often:
- Violate single responsibility principle
- Are harder to test in isolation
- Create merge conflicts in version control
- Are intimidating for new contributors
- Indicate opportunities for refactoring

The default limit of 150 lines strikes a balance between being permissive enough for real-world code while encouraging good practices.

### Rules

1. Count total lines in each Python file (including blank lines and comments)
2. Report files exceeding `max_lines` threshold
3. Search only in configured `search_paths`
4. Automatically exclude common directories:
   - `.venv/`, `venv/`
   - `__pycache__/`
   - `.git/`, `.hg/`, `.svn/`
   - `node_modules/`

### Configuration

```toml
[tool.structure-lint]
search_paths = ["src"]  # Default - applies to all validators

[tool.structure-lint.validators]
line_limits = true  # Enable/disable

[tool.structure-lint.line_limits]
max_lines = 150  # Default
```

### Examples

#### Passing Example

File with 145 lines:

```python
# src/features/auth/login.py (145 lines)
"""User login functionality."""

from typing import Optional
from .types import User, Credentials

def authenticate_user(credentials: Credentials) -> Optional[User]:
    """Authenticate user with credentials."""
    # ... implementation (140 more lines)
    pass
```

Output:
```
All Python files are within 150 line limit!
```

#### Failing Example

File with 187 lines:

```python
# src/features/auth/user_manager.py (187 lines)
"""User management with too many responsibilities."""

class UserManager:
    def create_user(self): ...
    def update_user(self): ...
    def delete_user(self): ...
    def authenticate(self): ...
    def authorize(self): ...
    def send_email(self): ...
    def generate_report(self): ...
    # ... 180 more lines
```

Output:
```
Found 1 file(s) exceeding 150 line limit:

  src/features/auth/user_manager.py: 187 lines (exceeds 150 line limit)

Consider splitting large files into smaller, focused modules.
```

### Customization Options

#### Adjust Line Limit

For legacy projects or different conventions:

```toml
[tool.structure-lint.line_limits]
max_lines = 200  # More lenient
```

Or more strict:

```toml
[tool.structure-lint.line_limits]
max_lines = 100  # Forces very small modules
```

#### Change Search Paths

Only check specific directories:

```toml
[tool.structure-lint]
search_paths = ["src"]  # Only src/, ignore scripts/
```

Or check additional directories:

```toml
[tool.structure-lint]
search_paths = ["src", "lib", "tests"]
```

#### Disable Temporarily

```toml
[tool.structure-lint.validators]
line_limits = false
```

### Migration Strategy

For existing projects with violations:

1. **Start High**: Set `max_lines = 500` to establish baseline
2. **Track Progress**: Gradually lower limit as you refactor
3. **Incremental**: Lower by 50 lines every sprint/release
4. **Target**: Aim for 150 lines eventually

Example progression:
```toml
# Week 1: Establish baseline
max_lines = 500

# Month 1: First reduction
max_lines = 300

# Month 2: Getting closer
max_lines = 200

# Month 3: Target reached
max_lines = 150
```

---

## One-Per-File Validator

### Purpose

Ensures each Python file contains at most one top-level function or class definition.

### Rationale

Single-definition files provide:
- **Discoverability**: Clear file naming (file name = what it contains)
- **Predictability**: Easy to find where something is defined
- **Modularity**: Natural boundaries for code organization
- **Testability**: Easier to write focused unit tests
- **Refactoring**: Simpler to move and reorganize code

### Rules

1. Count top-level functions and classes in each Python file
2. Ignore:
   - Imports
   - Module-level constants
   - Helper functions inside classes
   - Nested functions
   - `__init__.py` files (allowed to have 0 or multiple definitions)
3. Allow 0 definitions (empty files or only constants)
4. Allow 1 definition (pass)
5. Report files with 2+ definitions (fail)

### Configuration

```toml
[tool.structure-lint]
search_paths = ["src"]  # Default - applies to all validators

[tool.structure-lint.validators]
one_per_file = true  # Enable/disable
```

### Examples

#### Passing Examples

**Single class:**
```python
# src/features/auth/user.py
"""User model."""

from dataclasses import dataclass

MAX_USERNAME_LENGTH = 50  # Constants OK

@dataclass
class User:
    """User model."""
    username: str
    email: str

    def validate(self):  # Methods inside class OK
        """Validate user data."""
        return len(self.username) <= MAX_USERNAME_LENGTH
```

**Single function:**
```python
# src/utils/formatters/date_formatter.py
"""Format dates for display."""

from datetime import datetime

DEFAULT_FORMAT = "%Y-%m-%d"  # Constants OK

def format_date(date: datetime, format: str = DEFAULT_FORMAT) -> str:
    """Format a date for display."""
    return date.strftime(format)
```

**Empty file or constants only:**
```python
# src/constants/api_keys.py
"""API configuration."""

API_BASE_URL = "https://api.example.com"
API_TIMEOUT = 30
MAX_RETRIES = 3
```

#### Failing Examples

**Multiple classes:**
```python
# src/models/models.py  # BAD: Multiple models
"""User and authentication models."""

class User:
    """User model."""
    pass

class Session:  # Second class - violation!
    """Session model."""
    pass

class Token:  # Third class - violation!
    """Token model."""
    pass
```

Output:
```
Found 1 file(s) with multiple definitions:

  src/models/models.py: 3 definitions (expected 1)
    - User (class)
    - Session (class)
    - Token (class)

Consider splitting into separate files for better modularity.
```

**Better approach:**
```
src/models/
├── user.py      # Only User class
├── session.py   # Only Session class
└── token.py     # Only Token class
```

**Multiple functions:**
```python
# src/utils/helpers.py  # BAD: Grab-bag of utilities
"""Various helper functions."""

def format_date(date): ...   # First function
def parse_date(string): ...  # Second function - violation!
def validate_email(email): ... # Third function - violation!
```

**Better approach:**
```
src/utils/
├── date_formatter.py      # Only format_date
├── date_parser.py         # Only parse_date
└── email_validator.py     # Only validate_email
```

### Special Cases

#### `__init__.py` Files

`__init__.py` files are **exempt** from this rule. They commonly contain:
- Multiple imports
- Package-level constants
- Re-exports
- Initialization code

```python
# src/features/auth/__init__.py
"""Authentication package."""

from .user import User
from .session import Session
from .login import login
from .logout import logout

__all__ = ["User", "Session", "login", "logout"]
```

#### Type Aliases and Protocols

Type aliases count as definitions:

```python
# src/types/user_types.py
"""User-related types."""

from typing import Protocol

class Authenticatable(Protocol):  # This counts as 1 definition
    """Protocol for authenticatable objects."""
    def authenticate(self) -> bool: ...
```

### Customization Options

#### Change Search Paths

```toml
[tool.structure-lint]
search_paths = ["src"]  # Only check src/ (applies to all validators)
```

#### Disable Temporarily

```toml
[tool.structure-lint.validators]
one_per_file = false
```

### Migration Strategy

For projects with violations:

1. **Identify**: Run validator to find all violations
2. **Prioritize**: Start with files that have 2-3 definitions (easier wins)
3. **Refactor**: Split files and update imports
4. **Test**: Ensure tests still pass after splitting
5. **Repeat**: Tackle larger files

Example refactoring:

**Before:**
```python
# src/utils/string_utils.py (3 definitions)
def capitalize_words(s): ...
def snake_to_camel(s): ...
def truncate_string(s, length): ...
```

**After:**
```
src/utils/
├── word_capitalizer.py   # capitalize_words
├── case_converter.py     # snake_to_camel
└── string_truncator.py   # truncate_string
```

---

## Structure Validator (Opt-in)

### Purpose

Enforces an opinionated folder structure based on feature-driven development and screaming architecture principles.

### Rationale

Consistent structure provides:
- **Navigability**: Predictable location for code
- **Scalability**: Clear patterns for adding features
- **Onboarding**: New developers know where things go
- **Separation**: Clear boundaries between features/modules

**Note**: This is **opt-in by default** because it's highly opinionated. Only enable if your team agrees to this structure.

### The Three Rules

The structure validator enforces three simple rules:

#### Rule 1: Standard Folders Cannot Have Subdirectories

Standard folders (like `types/`, `utils/`, `constants/`, `tests/`) are leaf nodes in your folder tree. They contain Python files directly but cannot contain subdirectories.

**Valid:**
```
auth/
└── types/
    ├── user.py
    └── session.py
```

**Invalid:**
```
auth/
└── types/
    └── models/        # ERROR: subdirectory in standard folder
        └── user.py
```

#### Rule 2: Feature Folders Must Be Prefixed with Parent's Name

Feature folders (non-standard folders) must be named with their parent folder's name as a prefix, followed by a separator (default: `_`). This creates a clear hierarchy and prevents naming collisions.

**Exception**: Children of base folders (depth 0) are exempt from this rule.

**Valid:**
```
src/features/
├── auth/                    # depth 0, no prefix required
│   ├── auth_oauth/          # depth 1, prefixed with "auth_"
│   │   └── auth_oauth_google/  # depth 2, prefixed with "auth_oauth_"
│   └── auth_login/          # depth 1, prefixed with "auth_"
└── payments/                # depth 0, no prefix required
    └── payments_stripe/     # depth 1, prefixed with "payments_"
```

**Invalid:**
```
src/features/
└── auth/
    ├── oauth/               # ERROR: should be "auth_oauth"
    └── auth_oauth/
        └── google/          # ERROR: should be "auth_oauth_google"
```

#### Rule 3: Only Certain Files Allowed Outside Standard Folders

Python files can only appear in standard folders or in the `files_allowed_anywhere` list (default: `["__init__.py"]`). This prevents loose files from cluttering feature directories.

**Valid:**
```
auth/
├── __init__.py              # Allowed everywhere
├── types/
│   └── user.py              # In standard folder
└── utils/
    └── hash.py              # In standard folder
```

**Invalid:**
```
auth/
├── __init__.py
├── login.py                 # ERROR: not in standard folder
└── types/
    └── user.py
```

### Configuration

```toml
[tool.structure-lint]
search_paths = ["src"]  # Roots to validate (applies to all validators)

[tool.structure-lint.validators]
structure = true  # Must opt-in explicitly

[tool.structure-lint.structure]
folder_depth = 2               # Max nesting depth for feature folders
standard_folders = ["types", "utils", "constants", "tests"]
prefix_separator = "_"         # Separator for feature folder prefixes
files_allowed_anywhere = ["__init__.py"]
ignored_folders = ["__pycache__", ".mypy_cache", "*.egg-info"]
```

### Examples

#### Valid Structure

```
project/
├── src/
│   └── features/
│       ├── authentication/
│       │   ├── __init__.py
│       │   ├── types/
│       │   │   └── user.py
│       │   ├── utils/
│       │   │   └── hash_password.py
│       │   ├── constants/
│       │   │   └── config.py
│       │   ├── tests/
│       │   │   └── test_login.py
│       │   └── authentication_oauth/    # Feature folder with prefix
│       │       ├── types/
│       │       │   └── token.py
│       │       └── authentication_oauth_google/  # Nested with full prefix
│       │           └── types/
│       │               └── credentials.py
│       └── reporting/
│           ├── types/
│           └── utils/
```

#### Invalid Examples

**Files outside standard folders:**
```
src/features/auth/
├── login.py          # ERROR: Files not allowed here
└── types/
```

Error: `src/features/auth/: Disallowed files: ['login.py']`

**Feature folder without prefix:**
```
src/features/auth/
└── oauth/            # ERROR: Should be auth_oauth
```

Error: `src/features/auth/oauth: Feature folder must start with 'auth_'`

**Subdirectory in standard folder:**
```
src/features/auth/
└── types/
    └── models/       # ERROR: Standard folders cannot have subdirectories
```

Error: `src/features/auth/types: Standard folder cannot have subdirectories`

**Exceeding depth limit:**
```
src/features/auth/           # depth 0
└── auth_services/           # depth 1
    └── auth_services_oauth/ # depth 2 (at limit with default folder_depth=2)
        └── auth_services_oauth_providers/  # ERROR: depth 3, exceeds limit
```

Error: `src/features/auth/auth_services/auth_services_oauth/auth_services_oauth_providers: Exceeds max depth of 2`

### Standard and Feature Folders Can Coexist

Unlike previous versions, standard folders and feature folders can now exist at the same level. This provides flexibility in organizing code:

```
src/features/auth/
├── types/                   # Standard folder
│   └── user.py
├── utils/                   # Standard folder
│   └── helper.py
├── auth_oauth/              # Feature folder (with prefix)
│   └── types/
│       └── token.py
└── auth_password/           # Feature folder (with prefix)
    └── utils/
        └── hasher.py
```

### Customization Options

#### Different Standard Folders

```toml
[tool.structure-lint.structure]
standard_folders = ["models", "views", "controllers", "tests"]
```

Enables MVC-style organization:
```
src/features/authentication/
├── models/
├── views/
├── controllers/
└── tests/
```

#### Custom Prefix Separator

```toml
[tool.structure-lint.structure]
prefix_separator = "-"  # Use dashes instead of underscores
```

Results in:
```
src/features/auth/
└── auth-oauth/        # Dash separator
    └── auth-oauth-google/
```

Or no separator:
```toml
[tool.structure-lint.structure]
prefix_separator = ""  # Direct concatenation
```

Results in:
```
src/features/auth/
└── authoauth/
    └── authoauthgoogle/
```

#### Multiple Roots

```toml
[tool.structure-lint]
search_paths = ["src", "lib", "packages"]
```

```
project_root/
├── src/          # Validated
├── lib/          # Validated
├── packages/     # Validated
└── scripts/      # Not validated (not in search_paths)
```

#### Adjusting Depth Limits

```toml
[tool.structure-lint.structure]
folder_depth = 3  # Allow deeper nesting (default is 2)
```

#### Ignored Folders

```toml
[tool.structure-lint.structure]
ignored_folders = ["__pycache__", ".mypy_cache", ".venv", "build", "dist", "*.egg-info"]
```

Add project-specific build or cache directories that should not be validated.

### Migration Strategy

Adopting the structure validator for existing projects:

#### 1. Assess Current State

Run with structure validation enabled to see violations:

```bash
structure-lint --verbose
```

#### 2. Choose Approach

**Option A: Gradual Migration**
- Start with only new directories in `search_paths`
- Apply structure to new features only
- Gradually add more directories as you refactor

```toml
[tool.structure-lint]
search_paths = ["src/new_features"]  # Only validate new code
```

**Option B: Full Reorganization**
- Plan complete restructure
- Create new structure alongside old
- Migrate in phases
- Update imports
- Run tests continuously

#### 3. Customize to Fit

Don't fight the tool - customize it:

```toml
[tool.structure-lint.structure]
# Match your team's conventions
standard_folders = ["types", "models", "services", "utils", "tests"]
prefix_separator = "-"  # If you prefer dashes
folder_depth = 3  # Allow deeper nesting if needed
```

#### 4. Document Decisions

Add comments to your config explaining choices:

```toml
[tool.structure-lint]
# Only validate src/ - legacy/ and experiments/ are excluded
search_paths = ["src"]

[tool.structure-lint.structure]
# Added "services" as standard folder for our microservice architecture
standard_folders = ["types", "services", "utils", "tests"]

# Using dashes for better readability in folder names
prefix_separator = "-"
```

### When to Use Structure Validation

**Use when**:
- Starting a new project
- Team agrees on structure conventions
- Project is growing and needs organization
- Onboarding new developers frequently

**Don't use when**:
- Small projects (< 5 files)
- Exploratory/prototype phase
- Team hasn't agreed on structure
- Legacy project with different conventions

---

## Common Questions

### Can I disable validators temporarily?

Yes, use the `enabled` master switch:

```toml
[tool.structure-lint]
enabled = false  # Disables everything
```

Or disable individual validators:

```toml
[tool.structure-lint.validators]
line_limits = false
one_per_file = false
structure = false
```

### Can I exclude specific files or folders?

Currently, validators skip these directories automatically:
- `.venv/`, `venv/`
- `__pycache__/`
- `.git/`, `.hg/`, `.svn/`
- `node_modules/`

For structure validation, use `ignored_folders`:

```toml
[tool.structure-lint.structure]
ignored_folders = ["__pycache__", ".mypy_cache", "build", "dist"]
```

For more specific exclusions, adjust `search_paths`:

```toml
[tool.structure-lint]
search_paths = ["src"]  # Doesn't check scripts/
```

### What if I disagree with the defaults?

All rules are configurable! Adjust to fit your team:

```toml
[tool.structure-lint.line_limits]
max_lines = 300  # Your choice

[tool.structure-lint.validators]
one_per_file = false  # Disable if not relevant
```

### How do I run only one validator?

Disable the others:

```toml
[tool.structure-lint.validators]
line_limits = true    # Only this enabled
one_per_file = false
structure = false
```

---

## See Also

- [Configuration Reference](configuration.md) - All configuration options
- [Examples](examples/) - Sample configurations
- [README](../README.md) - Main documentation
