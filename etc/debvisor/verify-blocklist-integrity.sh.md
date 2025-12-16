# Code Issues Report: etc\debvisor\verify-blocklist-integrity.sh

Generated: 2025-12-13T17:07:07.045590
Source: etc\debvisor\verify-blocklist-integrity.sh

## Issues Summary

Total: 104 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 1 | 12 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 2 | 43 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 3 | 66 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 4 | 67 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 5 | 42 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 6 | 49 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 7 | 70 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 8 | 68 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 9 | 75 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 10 | 70 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 11 | 33 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 12 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 13 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 14 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 15 | 32 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 16 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 17 | 78 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 18 | 76 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 19 | 27 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 20 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 21 | 9 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 22 | 69 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 23 | 69 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 24 | 88 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 25 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 26 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 27 | 18 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 28 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 29 | 31 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 30 | 17 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 31 | 19 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 32 | 20 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 33 | 18 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 34 | 24 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 35 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 36 | 16 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 37 | 14 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 38 | 17 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 39 | 18 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 40 | 19 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 41 | 23 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 42 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 43 | 20 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 44 | 13 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 45 | 35 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 46 | 44 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 47 | 7 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 48 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 49 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 50 | 16 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 51 | 34 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 52 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 53 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 54 | 13 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 55 | 42 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 56 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 57 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 58 | 14 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 59 | 40 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 60 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 61 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 62 | 31 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 63 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 64 | 29 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 65 | 19 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 66 | 25 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 67 | 36 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 68 | 24 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 69 | 19 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 70 | 22 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 71 | 37 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 72 | 24 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 73 | 19 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 74 | 24 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 75 | 35 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 76 | 24 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 77 | 19 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 78 | 23 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 79 | 29 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 80 | 22 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 81 | 19 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 82 | 32 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 83 | 38 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 84 | 22 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 85 | 19 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 86 | 20 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 87 | 28 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 88 | 23 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 89 | 19 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 90 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 91 | 47 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 92 | 28 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 93 | 23 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 94 | 19 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 95 | 13 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 96 | 9 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 97 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 98 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 99 | 16 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 100 | 5 | shellcheck | `1009` | INFO | The mentioned syntax error was in this simple command. |
| 100 | 9 | shellcheck | `1073` | ERROR | Couldn't parse this here document. Fix to allow more checks. |
| 100 | 12 | shellcheck | `1044`| ERROR | Couldn't find end token`'EOF'\r' in the here document. |
| 100 | 17 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 361 | 1 | shellcheck | `1072` | ERROR | Here document was not correctly terminated. Fix any mentioned problems and try again. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 104 issues to fix

### Issue at Line 1

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## !/bin/bash
## Copyright (c) 2025 DebVisor contributors
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 2

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (1)

```python
## !/bin/bash
## Copyright (c) 2025 DebVisor contributors
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License
## You may obtain a copy of the License at
```python

### Proposal (1)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 3

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (2)

```python
## !/bin/bash
## Copyright (c) 2025 DebVisor contributors
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License
## You may obtain a copy of the License at
## [[[http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/)/)w)w)w).)a)p)a)c)h)e).)o)r)g)/)l)i)c)e)n)s)e)s)/)L)I)C)E)N)S)E)-)2).)0)
```python

### Proposal (2)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 4

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (3)

```python
## !/bin/bash
## Copyright (c) 2025 DebVisor contributors
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License
## You may obtain a copy of the License at
## [[[http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/)/)w)w)w).)a)p)a)c)h)e).)o)r)g)/)l)i)c)e)n)s)e)s)/)L)I)C)E)N)S)E)-)2).)0)
## Unless required by applicable law or agreed to in writing, software
```python

### Proposal (3)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 5

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (4)

```python
## Copyright (c) 2025 DebVisor contributors
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License
## You may obtain a copy of the License at
## [[[http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/)/)w)w)w).)a)p)a)c)h)e).)o)r)g)/)l)i)c)e)n)s)e)s)/)L)I)C)E)N)S)E)-)2).)0)
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS
```python

### Proposal (4)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 6

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (5)

```python
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License
## You may obtain a copy of the License at
## [[[http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/)/)w)w)w).)a)p)a)c)h)e).)o)r)g)/)l)i)c)e)n)s)e)s)/)L)I)C)E)N)S)E)-)2).)0)
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
```python

### Proposal (5)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 7

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (6)

```python
## you may not use this file except in compliance with the License
## You may obtain a copy of the License at
## [[[http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/)/)w)w)w).)a)p)a)c)h)e).)o)r)g)/)l)i)c)e)n)s)e)s)/)L)I)C)E)N)S)E)-)2).)0)
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
## See the License for the specific language governing permissions and
```python

### Proposal (6)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 8

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (7)

```python
## You may obtain a copy of the License at
## [[[http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/)/)w)w)w).)a)p)a)c)h)e).)o)r)g)/)l)i)c)e)n)s)e)s)/)L)I)C)E)N)S)E)-)2).)0)
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
## See the License for the specific language governing permissions and
## limitations under the License
```python

### Proposal (7)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 9

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (8)

```python
## [[[http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http://](http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses]([http://www.apache.org/license]([http://www.apache.org/licens]([http://www.apache.org/licen]([http://www.apache.org/lice]([http://www.apache.org/lic]([http://www.apache.org/li]([http://www.apache.org/l]([http://www.apache.org/]([http://www.apache.org]([http://www.apache.or]([http://www.apache.o]([http://www.apache.]([http://www.apache]([http://www.apach]([http://www.apac]([http://www.apa]([http://www.ap]([http://www.a]([http://www.]([http://www]([http://ww]([http://w](http:/)/)w)w)w).)a)p)a)c)h)e).)o)r)g)/)l)i)c)e)n)s)e)s)/)L)I)C)E)N)S)E)-)2).)0)
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
## See the License for the specific language governing permissions and
## limitations under the License
```python

### Proposal (8)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 10

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (9)

```python
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
## See the License for the specific language governing permissions and
## limitations under the License
```python

### Proposal (9)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 11

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (10)

```python
## distributed under the License is distributed on an "AS IS" BASIS
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
## See the License for the specific language governing permissions and
## limitations under the License

```python

### Proposal (10)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 12

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (11)

```python
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
## See the License for the specific language governing permissions and
## limitations under the License

## verify-blocklist-integrity.sh
```python

### Proposal (11)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 13

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (12)

```python
## See the License for the specific language governing permissions and
## limitations under the License

## verify-blocklist-integrity.sh

```python

### Proposal (12)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 14

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (13)

```python
## limitations under the License

## verify-blocklist-integrity.sh

## Verify SHA256 checksums and integrity of blocklist files before deployment
```python

### Proposal (13)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 15

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (14)

```python

## verify-blocklist-integrity.sh

## Verify SHA256 checksums and integrity of blocklist files before deployment
## Supports both individual file verification and batch verification against
```python

### Proposal (14)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 16

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (15)

```python

## verify-blocklist-integrity.sh

## Verify SHA256 checksums and integrity of blocklist files before deployment
## Supports both individual file verification and batch verification against
## blocklist-metadata.json
```python

### Proposal (15)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 17

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (16)

```python

## verify-blocklist-integrity.sh

## Verify SHA256 checksums and integrity of blocklist files before deployment
## Supports both individual file verification and batch verification against
## blocklist-metadata.json

```python

### Proposal (16)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 18

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (17)

```python
## verify-blocklist-integrity.sh

## Verify SHA256 checksums and integrity of blocklist files before deployment
## Supports both individual file verification and batch verification against
## blocklist-metadata.json

## Usage
```python

### Proposal (17)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 19

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (18)

```python

## Verify SHA256 checksums and integrity of blocklist files before deployment
## Supports both individual file verification and batch verification against
## blocklist-metadata.json

## Usage
## verify-blocklist-integrity.sh --blocklist  --sha256
```python

### Proposal (18)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 20

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (19)

```python
## Verify SHA256 checksums and integrity of blocklist files before deployment
## Supports both individual file verification and batch verification against
## blocklist-metadata.json

## Usage
## verify-blocklist-integrity.sh --blocklist  --sha256
## verify-blocklist-integrity.sh --metadata blocklist-metadata.json
```python

### Proposal (19)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 21

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (20)

```python
## Supports both individual file verification and batch verification against
## blocklist-metadata.json

## Usage
## verify-blocklist-integrity.sh --blocklist  --sha256
## verify-blocklist-integrity.sh --metadata blocklist-metadata.json
## verify-blocklist-integrity.sh --blocklist  --metadata blocklist-metadata.json
```python

### Proposal (20)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 22

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (21)

```python
## blocklist-metadata.json

## Usage
## verify-blocklist-integrity.sh --blocklist  --sha256
## verify-blocklist-integrity.sh --metadata blocklist-metadata.json
## verify-blocklist-integrity.sh --blocklist  --metadata blocklist-metadata.json

```python

### Proposal (21)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 23

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (22)

```python

## Usage
## verify-blocklist-integrity.sh --blocklist  --sha256
## verify-blocklist-integrity.sh --metadata blocklist-metadata.json
## verify-blocklist-integrity.sh --blocklist  --metadata blocklist-metadata.json

```python

### Proposal (22)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 24

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (23)

```python
## Usage
## verify-blocklist-integrity.sh --blocklist  --sha256
## verify-blocklist-integrity.sh --metadata blocklist-metadata.json
## verify-blocklist-integrity.sh --blocklist  --metadata blocklist-metadata.json

set -euo pipefail
```python

### Proposal (23)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 25

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (24)

```python
## verify-blocklist-integrity.sh --blocklist  --sha256
## verify-blocklist-integrity.sh --metadata blocklist-metadata.json
## verify-blocklist-integrity.sh --blocklist  --metadata blocklist-metadata.json

set -euo pipefail

```python

### Proposal (24)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 26

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (25)

```python
## verify-blocklist-integrity.sh --metadata blocklist-metadata.json
## verify-blocklist-integrity.sh --blocklist  --metadata blocklist-metadata.json

set -euo pipefail

## Color output for readability
```python

### Proposal (25)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 27

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (26)

```python
## verify-blocklist-integrity.sh --blocklist  --metadata blocklist-metadata.json

set -euo pipefail

## Color output for readability
RED='\033[0;31m'
```python

### Proposal (26)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 28

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (27)

```python

set -euo pipefail

## Color output for readability
RED='\033[0;31m'
GREEN='\033[0;32m'
```python

### Proposal (27)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 29

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (28)

```python

set -euo pipefail

## Color output for readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
```python

### Proposal (28)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 30

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (29)

```python
set -euo pipefail

## Color output for readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
```python

### Proposal (29)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 31

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (30)

```python

## Color output for readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
```python

### Proposal (30)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 32

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (31)

```python
## Color output for readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

```python

### Proposal (31)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 33

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (32)

```python
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

## Configuration
```python

### Proposal (32)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 34

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (33)

```python
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

## Configuration
VERBOSE=false
```python

### Proposal (33)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 35

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (34)

```python
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

## Configuration
VERBOSE=false
METADATA_FILE=""
```python

### Proposal (34)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 36

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (35)

```python
BLUE='\033[0;34m'
NC='\033[0m' # No Color

## Configuration
VERBOSE=false
METADATA_FILE=""
BLOCKLIST_FILE=""
```python

### Proposal (35)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 37

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (36)

```python
NC='\033[0m' # No Color

## Configuration
VERBOSE=false
METADATA_FILE=""
BLOCKLIST_FILE=""
EXPECTED_SHA256=""
```python

### Proposal (36)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 38

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (37)

```python

## Configuration
VERBOSE=false
METADATA_FILE=""
BLOCKLIST_FILE=""
EXPECTED_SHA256=""
ABORT_ON_FAILURE=false
```python

### Proposal (37)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 39

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (38)

```python
## Configuration
VERBOSE=false
METADATA_FILE=""
BLOCKLIST_FILE=""
EXPECTED_SHA256=""
ABORT_ON_FAILURE=false

```python

### Proposal (38)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 40

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (39)

```python
VERBOSE=false
METADATA_FILE=""
BLOCKLIST_FILE=""
EXPECTED_SHA256=""
ABORT_ON_FAILURE=false

## Logging functions
```python

### Proposal (39)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 41

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (40)

```python
METADATA_FILE=""
BLOCKLIST_FILE=""
EXPECTED_SHA256=""
ABORT_ON_FAILURE=false

## Logging functions
log_info() {
```python

### Proposal (40)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 42

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (41)

```python
BLOCKLIST_FILE=""
EXPECTED_SHA256=""
ABORT_ON_FAILURE=false

## Logging functions
log_info() {
    if ["$VERBOSE" = true]; then
```python

### Proposal (41)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 43

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (42)

```python
EXPECTED_SHA256=""
ABORT_ON_FAILURE=false

## Logging functions
log_info() {
    if ["$VERBOSE" = true]; then
        echo -e "${BLUE}[INFO]${NC} $*" >&2
```python

### Proposal (42)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 44

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (43)

```python
ABORT_ON_FAILURE=false

## Logging functions
log_info() {
    if ["$VERBOSE" = true]; then
        echo -e "${BLUE}[INFO]${NC} $*" >&2
    fi
```python

### Proposal (43)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 45

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (44)

```python

## Logging functions
log_info() {
    if ["$VERBOSE" = true]; then
        echo -e "${BLUE}[INFO]${NC} $*" >&2
    fi
}
```python

### Proposal (44)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 46

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (45)

```python
## Logging functions
log_info() {
    if ["$VERBOSE" = true]; then
        echo -e "${BLUE}[INFO]${NC} $*" >&2
    fi
}

```python

### Proposal (45)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 47

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (46)

```python
log_info() {
    if ["$VERBOSE" = true]; then
        echo -e "${BLUE}[INFO]${NC} $*" >&2
    fi
}

log_success() {
```python

### Proposal (46)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 48

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (47)

```python
    if ["$VERBOSE" = true]; then
        echo -e "${BLUE}[INFO]${NC} $*" >&2
    fi
}

log_success() {
    echo -e "${GREEN}[?]${NC} $*"
```python

### Proposal (47)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 49

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (48)

```python
        echo -e "${BLUE}[INFO]${NC} $*" >&2
    fi
}

log_success() {
    echo -e "${GREEN}[?]${NC} $*"
}
```python

### Proposal (48)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 50

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (49)

```python
    fi
}

log_success() {
    echo -e "${GREEN}[?]${NC} $*"
}

```python

### Proposal (49)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 51

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (50)

```python
}

log_success() {
    echo -e "${GREEN}[?]${NC} $*"
}

log_warn() {
```python

### Proposal (50)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 52

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (51)

```python

log_success() {
    echo -e "${GREEN}[?]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*" >&2
```python

### Proposal (51)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 53

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (52)

```python
log_success() {
    echo -e "${GREEN}[?]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*" >&2
}
```python

### Proposal (52)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 54

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (53)

```python
    echo -e "${GREEN}[?]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*" >&2
}

```python

### Proposal (53)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 55

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (54)

```python
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*" >&2
}

log_error() {
```python

### Proposal (54)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 56

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (55)

```python

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
```python

### Proposal (55)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 57

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (56)

```python
log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}
```python

### Proposal (56)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 58

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (57)

```python
    echo -e "${YELLOW}[WARN]${NC} $*" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

```python

### Proposal (57)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 59

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (58)

```python
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

## Parse command line arguments
```python

### Proposal (58)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 60

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (59)

```python

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

## Parse command line arguments
parse_args() {
```python

### Proposal (59)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 61

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (60)

```python
log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

## Parse command line arguments
parse_args() {
    while [[$# -gt 0]]; do
```python

### Proposal (60)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 62

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (61)

```python
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

## Parse command line arguments
parse_args() {
    while [[$# -gt 0]]; do
        case $1 in
```python

### Proposal (61)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 63

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (62)

```python
}

## Parse command line arguments
parse_args() {
    while [[$# -gt 0]]; do
        case $1 in
            --blocklist)
```python

### Proposal (62)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 64

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (63)

```python

## Parse command line arguments
parse_args() {
    while [[$# -gt 0]]; do
        case $1 in
            --blocklist)
                BLOCKLIST_FILE="$2"
```python

### Proposal (63)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 65

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (64)

```python
## Parse command line arguments
parse_args() {
    while [[$# -gt 0]]; do
        case $1 in
            --blocklist)
                BLOCKLIST_FILE="$2"
                shift 2
```python

### Proposal (64)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 66

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (65)

```python
parse_args() {
    while [[$# -gt 0]]; do
        case $1 in
            --blocklist)
                BLOCKLIST_FILE="$2"
                shift 2
                ;;
```python

### Proposal (65)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 67

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (66)

```python
    while [[$# -gt 0]]; do
        case $1 in
            --blocklist)
                BLOCKLIST_FILE="$2"
                shift 2
                ;;
            --sha256)
```python

### Proposal (66)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 68

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (67)

```python
        case $1 in
            --blocklist)
                BLOCKLIST_FILE="$2"
                shift 2
                ;;
            --sha256)
                EXPECTED_SHA256="$2"
```python

### Proposal (67)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 69

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (68)

```python
            --blocklist)
                BLOCKLIST_FILE="$2"
                shift 2
                ;;
            --sha256)
                EXPECTED_SHA256="$2"
                shift 2
```python

### Proposal (68)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 70

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (69)

```python
                BLOCKLIST_FILE="$2"
                shift 2
                ;;
            --sha256)
                EXPECTED_SHA256="$2"
                shift 2
                ;;
```python

### Proposal (69)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 71

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (70)

```python
                shift 2
                ;;
            --sha256)
                EXPECTED_SHA256="$2"
                shift 2
                ;;
            --metadata)
```python

### Proposal (70)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 72

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (71)

```python
                ;;
            --sha256)
                EXPECTED_SHA256="$2"
                shift 2
                ;;
            --metadata)
                METADATA_FILE="$2"
```python

### Proposal (71)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 73

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (72)

```python
            --sha256)
                EXPECTED_SHA256="$2"
                shift 2
                ;;
            --metadata)
                METADATA_FILE="$2"
                shift 2
```python

### Proposal (72)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 74

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (73)

```python
                EXPECTED_SHA256="$2"
                shift 2
                ;;
            --metadata)
                METADATA_FILE="$2"
                shift 2
                ;;
```python

### Proposal (73)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 75

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (74)

```python
                shift 2
                ;;
            --metadata)
                METADATA_FILE="$2"
                shift 2
                ;;
            --verbose)
```python

### Proposal (74)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 76

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (75)

```python
                ;;
            --metadata)
                METADATA_FILE="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=true
```python

### Proposal (75)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 77

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (76)

```python
            --metadata)
                METADATA_FILE="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
```python

### Proposal (76)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 78

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (77)

```python
                METADATA_FILE="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
```python

### Proposal (77)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 79

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (78)

```python
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --abort-on-failure)
```python

### Proposal (78)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 80

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (79)

```python
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --abort-on-failure)
                ABORT_ON_FAILURE=true
```python

### Proposal (79)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 81

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (80)

```python
            --verbose)
                VERBOSE=true
                shift
                ;;
            --abort-on-failure)
                ABORT_ON_FAILURE=true
                shift
```python

### Proposal (80)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 82

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (81)

```python
                VERBOSE=true
                shift
                ;;
            --abort-on-failure)
                ABORT_ON_FAILURE=true
                shift
                ;;
```python

### Proposal (81)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 83

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (82)

```python
                shift
                ;;
            --abort-on-failure)
                ABORT_ON_FAILURE=true
                shift
                ;;
            --help)
```python

### Proposal (82)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 84

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (83)

```python
                ;;
            --abort-on-failure)
                ABORT_ON_FAILURE=true
                shift
                ;;
            --help)
                print_usage
```python

### Proposal (83)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 85

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (84)

```python
            --abort-on-failure)
                ABORT_ON_FAILURE=true
                shift
                ;;
            --help)
                print_usage
                exit 0
```python

### Proposal (84)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 86

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (85)

```python
                ABORT_ON_FAILURE=true
                shift
                ;;
            --help)
                print_usage
                exit 0
                ;;
```python

### Proposal (85)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 87

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (86)

```python
                shift
                ;;
            --help)
                print_usage
                exit 0
                ;;
            *)
```python

### Proposal (86)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 88

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (87)

```python
                ;;
            --help)
                print_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
```python

### Proposal (87)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 89

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (88)

```python
            --help)
                print_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
```python

### Proposal (88)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 90

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (89)

```python
                print_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
                exit 1
```python

### Proposal (89)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 91

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (90)

```python
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
```python

### Proposal (90)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 92

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (91)

```python
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
```python

### Proposal (91)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 93

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (92)

```python
            *)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done
```python

### Proposal (92)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 94

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (93)

```python
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done
}
```python

### Proposal (93)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 95

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (94)

```python
                print_usage
                exit 1
                ;;
        esac
    done
}

```python

### Proposal (94)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 96

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (95)

```python
                exit 1
                ;;
        esac
    done
}

print_usage() {
```python

### Proposal (95)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 97

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (96)

```python
                ;;
        esac
    done
}

print_usage() {
    cat << 'EOF'
```python

### Proposal (96)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 98

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (97)

```python
        esac
    done
}

print_usage() {
    cat << 'EOF'
Usage: verify-blocklist-integrity.sh [OPTIONS]
```python

### Proposal (97)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 99

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (98)

```python
    done
}

print_usage() {
    cat << 'EOF'
Usage: verify-blocklist-integrity.sh [OPTIONS]

```python

### Proposal (98)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 100

**Tool:**shellcheck |**Code:**`1009` |**Severity:** INFO

**Message:** The mentioned syntax error was in this simple command.

### Context (99)

```python
}

print_usage() {
    cat << 'EOF'
Usage: verify-blocklist-integrity.sh [OPTIONS]

Options:
```python

### Proposal (99)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 100 (1)

**Tool:**shellcheck |**Code:**`1073` |**Severity:** ERROR

**Message:** Couldn't parse this here document. Fix to allow more checks.

### Context (100)

```python
}

print_usage() {
    cat << 'EOF'
Usage: verify-blocklist-integrity.sh [OPTIONS]

Options:
```python

### Proposal (100)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 100 (2)

**Tool:**shellcheck |**Code:**`1044` |**Severity:** ERROR

**Message:** Couldn't find end token`'EOF'\r' in the here document.

### Context (101)

```python
}

print_usage() {
    cat << 'EOF'
Usage: verify-blocklist-integrity.sh [OPTIONS]

Options:
```python

### Proposal (101)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 100 (3)

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context (102)

```python
}

print_usage() {
    cat << 'EOF'
Usage: verify-blocklist-integrity.sh [OPTIONS]

Options:
```python

### Proposal (102)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 361

**Tool:**shellcheck |**Code:**`1072` |**Severity:** ERROR

**Message:** Here document was not correctly terminated. Fix any mentioned
problems and try again.

### Context (103)

```python
}

main "$@"
```python

### Proposal (103)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

## Implementation Progress

To mark an issue as fixed, add the issue code to the line below with a ✅ emoji:

**Fixed Issues:** (none yet)

---
*Updated: (auto-populated by coding expert)*
