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
| 100 | 12 | shellcheck | `1044` | ERROR | Couldn't find end token `'EOF'\r' in the here document. |
| 100 | 17 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 361 | 1 | shellcheck | `1072` | ERROR | Here document was not correctly terminated. Fix any mentioned problems and try again. |

## Implementation Status
Items marked below as fixed:
