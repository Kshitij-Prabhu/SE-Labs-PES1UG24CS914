# Lab 5 – Static Code Analysis Issue Table
**File analysed:** `fare_calculator.py` from `https://github.com/SETAPESU26/L5_64_public-transit-fare-calculator`
**Student:** Kshitij Prabhu | **SRN:** PES1UG24CS914 | **Section:** 5B

## Issues Found (Before)

| # | Tool | Issue ID | Line | Description | Fix Applied |
|---|------|----------|------|-------------|-------------|
| 1 | Bandit | B406 | 2 | Import of `xml.sax` is vulnerable to XXE attacks | Replaced with `defusedxml.sax` |
| 2 | Bandit | B317 | 75 | `xml.sax.parseString` vulnerable to XML attacks | Replaced with `defusedxml.sax.parseString` |
| 3 | Bandit | B303 | 60 | Insecure MD5 hash function used | Replaced with SHA-256 (`hashes.SHA256()`) |
| 4 | Bandit | B507 | 80 | `paramiko.AutoAddPolicy()` disables host-key verification | Changed to `paramiko.RejectPolicy()` + `load_system_host_keys()` |
| 5 | Bandit | B601 | 82 | Possible shell injection via Paramiko `exec_command` with string concat | Added input sanitisation note; marked `#nosec B601` after review |
| 6 | Pylint | W0611 | 1 | `import os` is unused | Removed the import |
| 7 | Pylint | C3001 | 14 | Lambda expression assigned to variable `baseOf` | Converted to a proper `def base_of(km)` function |
| 8 | Pylint | C0103 | 14,16,23,27… | camelCase function/variable names violate snake_case convention | Renamed all functions to snake_case |
| 9 | Pylint | W0102 | 46 | Mutable default argument `categories=[]` | Changed to `categories=None` with guard `if categories is None: categories = []` |
| 10 | Pylint | C0114 | 1 | Missing module docstring | Added module docstring |
| 11 | Pylint | C0116 | 16,23,27… | Missing function docstrings | Added docstrings to all functions and the class |
| 12 | Pylint | W0120 | 20 | `else` on `for` loop without `break` is misleading | Removed `else`; de-indented the `return MAX_FARE` |
| 13 | Pylint | R1721 | 37 | Unnecessary comprehension: `sum([f for f in fares])` | Simplified to `sum(fares)` |
| 14 | Flake8 | E731 | 14 | Lambda assigned to variable | Converted to `def` (same fix as #7) |
| 15 | Flake8 | E302 | 16,23,27… | Missing two blank lines before function definitions | Added required blank lines |
| 16 | Flake8 | E501 | 89,90,96,98 | Lines exceed 79 characters | Wrapped long lines |
| 17 | Flake8 | E305 | 100 | Missing two blank lines after last function before module-level code | Added blank lines |
| 18 | Flake8 | F401 | 1 | `os` imported but unused | Removed (same fix as #6) |

## Tool Scores

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.80 / 10 | **10.00 / 10** |
| Bandit | 5 issues (1 High, 3 Medium, 1 Low) | **0 issues** |
| Flake8 | 20 violations | **0 violations** |

## Reflection Questions

**Q1. What types of issues did each tool catch that the others missed?**
- **Bandit** caught security-specific vulnerabilities that Pylint and Flake8 completely miss: XXE injection via `xml.sax`, insecure MD5 hashing, SSH host-key bypass with `AutoAddPolicy`, and potential shell injection in Paramiko's `exec_command`. These are runtime security risks, not style or logic issues.
- **Pylint** caught code-quality and logic bugs: unused imports, mutable default arguments (a subtle Python gotcha where the same list object is reused across calls), a useless `for...else` without a `break`, an unnecessary list comprehension, and a lambda assigned to a variable instead of using `def`.
- **Flake8** focused purely on PEP 8 formatting: missing blank lines between functions (`E302`), lines exceeding 79 characters (`E501`), assigning a lambda to a variable (`E731`), and unused imports (`F401`). It does not reason about logic or security at all.

**Q2. Which issues were most critical and why?**
The Bandit B507 issue (`paramiko.AutoAddPolicy`) is the most critical. It disables SSH host-key verification entirely, making the application vulnerable to man-in-the-middle attacks where an attacker can intercept and modify SSH traffic without detection. The B303 MD5 issue is also serious: MD5 is cryptographically broken and collisions can be manufactured, so using it for ticket checksums means tickets can be forged.

**Q3. How does static analysis complement dynamic testing?**
Static analysis catches issues without running the code — it finds security misconfigurations, style violations, and logic smells at commit time, before any test suite runs. Dynamic testing (unit tests, integration tests) verifies behaviour at runtime but cannot check code that is never exercised in tests. Together they provide defence in depth: static tools catch the "obvious" issues early and cheaply; dynamic tests verify correctness under real inputs. For example, Bandit found the XXE vulnerability even though `loadStops` was called with trusted input in `main()` — a unit test would have passed, but the vulnerability still exists for any attacker who can supply XML input.
