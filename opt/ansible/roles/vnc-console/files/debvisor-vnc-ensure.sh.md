# Code Issues Report: opt\ansible\roles\vnc-console\files\debvisor-vnc-ensure.sh

Generated: 2025-12-13T17:07:35.028400
Source: opt\ansible\roles\vnc-console\files\debvisor-vnc-ensure.sh

## Issues Summary

Total: 29 issues found

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
| 14 | 66 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 15 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 16 | 18 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 17 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 18 | 10 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 19 | 22 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 20 | 33 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 21 | 9 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 22 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 23 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 24 | 59 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 25 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 26 | 48 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 27 | 43 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 28 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 29 | 37 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 29 issues to fix

### Issue at Line 1

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## !/bin/bash
## Copyright (c) 2025 DebVisor contributors
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
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

### Context

```python
## !/bin/bash
## Copyright (c) 2025 DebVisor contributors
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 3

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## !/bin/bash
## Copyright (c) 2025 DebVisor contributors
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## [http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses](http://www.apache.org/licenses)/)L)I)C)E)N)S)E)-)2).)0)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 4

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## !/bin/bash
## Copyright (c) 2025 DebVisor contributors
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## [http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses](http://www.apache.org/licenses)/)L)I)C)E)N)S)E)-)2).)0)
## Unless required by applicable law or agreed to in writing, software
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 5

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## Copyright (c) 2025 DebVisor contributors
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## [http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses](http://www.apache.org/licenses)/)L)I)C)E)N)S)E)-)2).)0)
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 6

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## [http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses](http://www.apache.org/licenses)/)L)I)C)E)N)S)E)-)2).)0)
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 7

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## [http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses](http://www.apache.org/licenses)/)L)I)C)E)N)S)E)-)2).)0)
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 8

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## You may obtain a copy of the License at
## [http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses](http://www.apache.org/licenses)/)L)I)C)E)N)S)E)-)2).)0)
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 9

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## [http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.]([http://www.apache.org/licenses/LICENSE-2]([http://www.apache.org/licenses/LICENSE-]([http://www.apache.org/licenses/LICENSE]([http://www.apache.org/licenses/LICENS]([http://www.apache.org/licenses/LICEN]([http://www.apache.org/licenses/LICE]([http://www.apache.org/licenses/LIC]([http://www.apache.org/licenses/LI]([http://www.apache.org/licenses/L]([http://www.apache.org/licenses/]([http://www.apache.org/licenses](http://www.apache.org/licenses)/)L)I)C)E)N)S)E)-)2).)0)
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 10

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 11

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

## DebVisor: ensure websockify console for a VM and print full URL
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 12

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

## DebVisor: ensure websockify console for a VM and print full URL

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 13

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## See the License for the specific language governing permissions and
## limitations under the License.

## DebVisor: ensure websockify console for a VM and print full URL

set -euo pipefail
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 14

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## limitations under the License.

## DebVisor: ensure websockify console for a VM and print full URL

set -euo pipefail

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 15

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

## DebVisor: ensure websockify console for a VM and print full URL

set -euo pipefail

VM=${1:-}
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 16

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

## DebVisor: ensure websockify console for a VM and print full URL

set -euo pipefail

VM=${1:-}
if [-z "$VM"]; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 17

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## DebVisor: ensure websockify console for a VM and print full URL

set -euo pipefail

VM=${1:-}
if [-z "$VM"]; then
  echo "Usage: $0 " >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 18

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

set -euo pipefail

VM=${1:-}
if [-z "$VM"]; then
  echo "Usage: $0 " >&2
  exit 1
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 19

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
set -euo pipefail

VM=${1:-}
if [-z "$VM"]; then
  echo "Usage: $0 " >&2
  exit 1
fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 20

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

VM=${1:-}
if [-z "$VM"]; then
  echo "Usage: $0 " >&2
  exit 1
fi

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 21

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
VM=${1:-}
if [-z "$VM"]; then
  echo "Usage: $0 " >&2
  exit 1
fi

systemctl enable --now "debvisor-websockify@${VM}.service"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 22

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
if [-z "$VM"]; then
  echo "Usage: $0 " >&2
  exit 1
fi

systemctl enable --now "debvisor-websockify@${VM}.service"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 23

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
  echo "Usage: $0 " >&2
  exit 1
fi

systemctl enable --now "debvisor-websockify@${VM}.service"

HOSTNAME=$(hostname -f 2>/dev/null || hostname)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 24

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
  exit 1
fi

systemctl enable --now "debvisor-websockify@${VM}.service"

HOSTNAME=$(hostname -f 2>/dev/null || hostname)
VNC_PATH="/novnc/vnc.html?path=/vnc/${VM}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 25

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
fi

systemctl enable --now "debvisor-websockify@${VM}.service"

HOSTNAME=$(hostname -f 2>/dev/null || hostname)
VNC_PATH="/novnc/vnc.html?path=/vnc/${VM}"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 26

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

systemctl enable --now "debvisor-websockify@${VM}.service"

HOSTNAME=$(hostname -f 2>/dev/null || hostname)
VNC_PATH="/novnc/vnc.html?path=/vnc/${VM}"

echo "[http://${HOSTNAME}${VNC_PATH}"]([http://${HOSTNAME}${VNC_PATH}]([http://${HOSTNAME}${VNC_PATH]([http://${HOSTNAME}${VNC_PAT]([http://${HOSTNAME}${VNC*PA]([http://${HOSTNAME}${VNC*P]([http://${HOSTNAME}${VNC*]([http://${HOSTNAME}${VNC]([http://${HOSTNAME}${VN]([http://${HOSTNAME}${V]([http://${HOSTNAME}${]([http://${HOSTNAME}$]([http://${HOSTNAME}](http://${HOSTNAME})$){)V)N)C)*)P)A)T)H)})")
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 27

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
systemctl enable --now "debvisor-websockify@${VM}.service"

HOSTNAME=$(hostname -f 2>/dev/null || hostname)
VNC_PATH="/novnc/vnc.html?path=/vnc/${VM}"

echo "[http://${HOSTNAME}${VNC_PATH}"]([http://${HOSTNAME}${VNC_PATH}]([http://${HOSTNAME}${VNC_PATH]([http://${HOSTNAME}${VNC_PAT]([http://${HOSTNAME}${VNC*PA]([http://${HOSTNAME}${VNC*P]([http://${HOSTNAME}${VNC*]([http://${HOSTNAME}${VNC]([http://${HOSTNAME}${VN]([http://${HOSTNAME}${V]([http://${HOSTNAME}${]([http://${HOSTNAME}$]([http://${HOSTNAME}](http://${HOSTNAME})$){)V)N)C)*)P)A)T)H)})")
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 28

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

HOSTNAME=$(hostname -f 2>/dev/null || hostname)
VNC_PATH="/novnc/vnc.html?path=/vnc/${VM}"

echo "[http://${HOSTNAME}${VNC_PATH}"]([http://${HOSTNAME}${VNC_PATH}]([http://${HOSTNAME}${VNC_PATH]([http://${HOSTNAME}${VNC_PAT]([http://${HOSTNAME}${VNC*PA]([http://${HOSTNAME}${VNC*P]([http://${HOSTNAME}${VNC*]([http://${HOSTNAME}${VNC]([http://${HOSTNAME}${VN]([http://${HOSTNAME}${V]([http://${HOSTNAME}${]([http://${HOSTNAME}$]([http://${HOSTNAME}](http://${HOSTNAME})$){)V)N)C)*)P)A)T)H)})")
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 29

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
HOSTNAME=$(hostname -f 2>/dev/null || hostname)
VNC_PATH="/novnc/vnc.html?path=/vnc/${VM}"

echo "[http://${HOSTNAME}${VNC_PATH}"]([http://${HOSTNAME}${VNC_PATH}]([http://${HOSTNAME}${VNC_PATH]([http://${HOSTNAME}${VNC_PAT]([http://${HOSTNAME}${VNC*PA]([http://${HOSTNAME}${VNC*P]([http://${HOSTNAME}${VNC*]([http://${HOSTNAME}${VNC]([http://${HOSTNAME}${VN]([http://${HOSTNAME}${V]([http://${HOSTNAME}${]([http://${HOSTNAME}$]([http://${HOSTNAME}](http://${HOSTNAME})$){)V)N)C)*)P)A)T)H)})")
```python

### Proposal

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
