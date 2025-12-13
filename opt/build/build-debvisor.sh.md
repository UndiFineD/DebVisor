# Code Issues Report: opt\build\build-debvisor.sh

Generated: 2025-12-13T17:07:39.848457
Source: opt\build\build-debvisor.sh

## Issues Summary

Total: 235 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 1 | 20 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 2 | 32 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 3 | 18 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 4 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 5 | 10 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 6 | 14 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 25 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 26 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 27 | 25 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 28 | 17 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 29 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 30 | 14 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 31 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 32 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 33 | 7 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 34 | 51 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 35 | 18 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 36 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 37 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 38 | 9 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 39 | 5 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 40 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 41 | 41 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 42 | 36 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 43 | 40 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 44 | 41 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 45 | 88 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 46 | 82 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 47 | 61 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 48 | 61 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 49 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 50 | 19 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 51 | 21 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 52 | 23 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 53 | 24 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 54 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 55 | 24 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 56 | 25 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 57 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 58 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 59 | 67 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 60 | 19 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 61 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 62 | 9 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 63 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 64 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 65 | 75 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 66 | 75 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 67 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 68 | 59 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 69 | 47 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 70 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 71 | 21 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 72 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 73 | 36 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 74 | 70 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 75 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 76 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 77 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 78 | 38 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 79 | 89 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 80 | 5 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 81 | 78 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 82 | 29 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 83 | 13 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 84 | 117 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 85 | 12 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 86 | 84 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 87 | 61 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 88 | 126 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 89 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 90 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 91 | 9 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 92 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 93 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 94 | 35 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 95 | 49 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 96 | 65 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 97 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 98 | 7 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 99 | 5 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 100 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 101 | 49 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 102 | 155 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 103 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 104 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 105 | 81 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 106 | 79 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 107 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 108 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 109 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 110 | 53 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 111 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 112 | 48 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 113 | 56 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 114 | 67 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 115 | 49 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 116 | 38 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 117 | 55 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 118 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 119 | 67 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 120 | 64 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 121 | 109 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 122 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 123 | 27 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 124 | 17 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 125 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 126 | 7 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 127 | 105 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 128 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 129 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 130 | 5 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 131 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 132 | 37 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 133 | 80 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 134 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 135 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 136 | 17 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 137 | 27 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 138 | 29 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 139 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 140 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 141 | 39 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 142 | 32 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 143 | 68 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 144 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 145 | 7 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 146 | 5 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 147 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 148 | 14 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 149 | 27 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 150 | 7 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 151 | 60 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 152 | 25 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 153 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 154 | 7 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 155 | 68 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 156 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 157 | 7 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 158 | 60 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 159 | 22 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 160 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 161 | 7 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 162 | 89 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 163 | 15 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 164 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 165 | 5 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 166 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 167 | 36 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 168 | 45 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 170 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 171 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 172 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 173 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 174 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 175 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 176 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 177 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 178 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 179 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 180 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 181 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 182 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 183 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 184 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 185 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 186 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 187 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 188 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 189 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 190 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 191 | 5 | shellcheck | `2215` | WARNING | This flag is used as a command name. Bad line break or missing [..]? |
| 191 | 23 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 192 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 193 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 194 | 62 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 195 | 46 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 196 | 34 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 197 | 5 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 198 | 90 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 199 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 200 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 201 | 45 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 202 | 79 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 203 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 204 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 205 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 206 | 43 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 207 | 81 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 208 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 209 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 210 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 211 | 55 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 212 | 9 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 213 | 13 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 214 | 42 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 215 | 86 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 216 | 9 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 217 | 63 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 218 | 7 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 219 | 2 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 220 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 221 | 18 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 222 | 25 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 223 | 49 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 224 | 72 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 225 | 9 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 226 | 26 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 227 | 7 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 228 | 50 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 229 | 5 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 230 | 59 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 231 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 232 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 233 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 234 | 45 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 235 | 57 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 236 | 41 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 237 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 238 | 44 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 239 | 48 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 240 | 92 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 241 | 82 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 242 | 13 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 243 | 79 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 244 | 47 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 245 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 246 | 9 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 247 | 77 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 248 | 7 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 249 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 250 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 251 | 40 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 252 | 81 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 253 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 235 issues to fix

### Issue at Line 1

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## !/usr/bin/env bash
## Build script for DebVisor ISO
set -euo pipefail

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
## !/usr/bin/env bash
## Build script for DebVisor ISO
set -euo pipefail

usage() {
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
## !/usr/bin/env bash
## Build script for DebVisor ISO
set -euo pipefail

usage() {
    cat &2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 32

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    -h|--help)
        usage
        exit 0
        ;;
    *)
        echo "[DebVisor] Unknown argument: $1" >&2
        usage >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 33

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        usage
        exit 0
        ;;
    *)
        echo "[DebVisor] Unknown argument: $1" >&2
        usage >&2
        exit 1
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 34

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        exit 0
        ;;
    *)
        echo "[DebVisor] Unknown argument: $1" >&2
        usage >&2
        exit 1
        ;;
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 35

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        ;;
    *)
        echo "[DebVisor] Unknown argument: $1" >&2
        usage >&2
        exit 1
        ;;
    esac
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 36

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    *)
        echo "[DebVisor] Unknown argument: $1" >&2
        usage >&2
        exit 1
        ;;
    esac
done
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 37

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        echo "[DebVisor] Unknown argument: $1" >&2
        usage >&2
        exit 1
        ;;
    esac
done

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 38

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        usage >&2
        exit 1
        ;;
    esac
done

DEBVISOR_DIST="${DEBVISOR_DIST:-trixie}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 39

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        exit 1
        ;;
    esac
done

DEBVISOR_DIST="${DEBVISOR_DIST:-trixie}"
DEBVISOR_FAST="${DEBVISOR_FAST:-0}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 40

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        ;;
    esac
done

DEBVISOR_DIST="${DEBVISOR_DIST:-trixie}"
DEBVISOR_FAST="${DEBVISOR_FAST:-0}"
DEBVISOR_ARCH="${DEBVISOR_ARCH:-amd64}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 41

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    esac
done

DEBVISOR_DIST="${DEBVISOR_DIST:-trixie}"
DEBVISOR_FAST="${DEBVISOR_FAST:-0}"
DEBVISOR_ARCH="${DEBVISOR_ARCH:-amd64}"
DEBVISOR_VERSION="${DEBVISOR_VERSION:-}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 42

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
done

DEBVISOR_DIST="${DEBVISOR_DIST:-trixie}"
DEBVISOR_FAST="${DEBVISOR_FAST:-0}"
DEBVISOR_ARCH="${DEBVISOR_ARCH:-amd64}"
DEBVISOR_VERSION="${DEBVISOR_VERSION:-}"
DEBVISOR_MIRROR_BOOTSTRAP="${DEBVISOR_MIRROR_BOOTSTRAP:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 43

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

DEBVISOR_DIST="${DEBVISOR_DIST:-trixie}"
DEBVISOR_FAST="${DEBVISOR_FAST:-0}"
DEBVISOR_ARCH="${DEBVISOR_ARCH:-amd64}"
DEBVISOR_VERSION="${DEBVISOR_VERSION:-}"
DEBVISOR_MIRROR_BOOTSTRAP="${DEBVISOR_MIRROR_BOOTSTRAP:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
DEBVISOR_MIRROR_BINARY="${DEBVISOR_MIRROR_BINARY:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 44

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
DEBVISOR_DIST="${DEBVISOR_DIST:-trixie}"
DEBVISOR_FAST="${DEBVISOR_FAST:-0}"
DEBVISOR_ARCH="${DEBVISOR_ARCH:-amd64}"
DEBVISOR_VERSION="${DEBVISOR_VERSION:-}"
DEBVISOR_MIRROR_BOOTSTRAP="${DEBVISOR_MIRROR_BOOTSTRAP:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
DEBVISOR_MIRROR_BINARY="${DEBVISOR_MIRROR_BINARY:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
DEBVISOR_FIRMWARE_CHROOT="${DEBVISOR_FIRMWARE_CHROOT:-true}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 45

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
DEBVISOR_FAST="${DEBVISOR_FAST:-0}"
DEBVISOR_ARCH="${DEBVISOR_ARCH:-amd64}"
DEBVISOR_VERSION="${DEBVISOR_VERSION:-}"
DEBVISOR_MIRROR_BOOTSTRAP="${DEBVISOR_MIRROR_BOOTSTRAP:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
DEBVISOR_MIRROR_BINARY="${DEBVISOR_MIRROR_BINARY:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
DEBVISOR_FIRMWARE_CHROOT="${DEBVISOR_FIRMWARE_CHROOT:-true}"
DEBVISOR_FIRMWARE_BINARY="${DEBVISOR_FIRMWARE_BINARY:-true}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 46

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
DEBVISOR_ARCH="${DEBVISOR_ARCH:-amd64}"
DEBVISOR_VERSION="${DEBVISOR_VERSION:-}"
DEBVISOR_MIRROR_BOOTSTRAP="${DEBVISOR_MIRROR_BOOTSTRAP:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
DEBVISOR_MIRROR_BINARY="${DEBVISOR_MIRROR_BINARY:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
DEBVISOR_FIRMWARE_CHROOT="${DEBVISOR_FIRMWARE_CHROOT:-true}"
DEBVISOR_FIRMWARE_BINARY="${DEBVISOR_FIRMWARE_BINARY:-true}"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 47

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
DEBVISOR_VERSION="${DEBVISOR_VERSION:-}"
DEBVISOR_MIRROR_BOOTSTRAP="${DEBVISOR_MIRROR_BOOTSTRAP:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
DEBVISOR_MIRROR_BINARY="${DEBVISOR_MIRROR_BINARY:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
DEBVISOR_FIRMWARE_CHROOT="${DEBVISOR_FIRMWARE_CHROOT:-true}"
DEBVISOR_FIRMWARE_BINARY="${DEBVISOR_FIRMWARE_BINARY:-true}"

normalize_bool() {
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 48

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
DEBVISOR_MIRROR_BOOTSTRAP="${DEBVISOR_MIRROR_BOOTSTRAP:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
DEBVISOR_MIRROR_BINARY="${DEBVISOR_MIRROR_BINARY:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
DEBVISOR_FIRMWARE_CHROOT="${DEBVISOR_FIRMWARE_CHROOT:-true}"
DEBVISOR_FIRMWARE_BINARY="${DEBVISOR_FIRMWARE_BINARY:-true}"

normalize_bool() {
    case "${1,,}" in
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 49

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
DEBVISOR_MIRROR_BINARY="${DEBVISOR_MIRROR_BINARY:-[http://deb.debian.org/debian/}"]([http://deb.debian.org/debian/}]([http://deb.debian.org/debian/]([http://deb.debian.org/debian]([http://deb.debian.org/debia]([http://deb.debian.org/debi]([http://deb.debian.org/deb]([http://deb.debian.org/de]([http://deb.debian.org/d](http://deb.debian.org/d)e)b)i)a)n)/)})")
DEBVISOR_FIRMWARE_CHROOT="${DEBVISOR_FIRMWARE_CHROOT:-true}"
DEBVISOR_FIRMWARE_BINARY="${DEBVISOR_FIRMWARE_BINARY:-true}"

normalize_bool() {
    case "${1,,}" in
        1|true|yes|on)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 50

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
DEBVISOR_FIRMWARE_CHROOT="${DEBVISOR_FIRMWARE_CHROOT:-true}"
DEBVISOR_FIRMWARE_BINARY="${DEBVISOR_FIRMWARE_BINARY:-true}"

normalize_bool() {
    case "${1,,}" in
        1|true|yes|on)
            echo "true"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 51

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
DEBVISOR_FIRMWARE_BINARY="${DEBVISOR_FIRMWARE_BINARY:-true}"

normalize_bool() {
    case "${1,,}" in
        1|true|yes|on)
            echo "true"
            ;;
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 52

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

normalize_bool() {
    case "${1,,}" in
        1|true|yes|on)
            echo "true"
            ;;
        0|false|no|off)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 53

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
normalize_bool() {
    case "${1,,}" in
        1|true|yes|on)
            echo "true"
            ;;
        0|false|no|off)
            echo "false"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 54

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    case "${1,,}" in
        1|true|yes|on)
            echo "true"
            ;;
        0|false|no|off)
            echo "false"
            ;;
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 55

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        1|true|yes|on)
            echo "true"
            ;;
        0|false|no|off)
            echo "false"
            ;;
        *)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 56

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
            echo "true"
            ;;
        0|false|no|off)
            echo "false"
            ;;
        *)
            echo "[DebVisor] ERROR: Invalid boolean value: $1" >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 57

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
            ;;
        0|false|no|off)
            echo "false"
            ;;
        *)
            echo "[DebVisor] ERROR: Invalid boolean value: $1" >&2
            exit 1
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 58

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        0|false|no|off)
            echo "false"
            ;;
        *)
            echo "[DebVisor] ERROR: Invalid boolean value: $1" >&2
            exit 1
            ;;
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 59

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
            echo "false"
            ;;
        *)
            echo "[DebVisor] ERROR: Invalid boolean value: $1" >&2
            exit 1
            ;;
    esac
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 60

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
            ;;
        *)
            echo "[DebVisor] ERROR: Invalid boolean value: $1" >&2
            exit 1
            ;;
    esac
}
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 61

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        *)
            echo "[DebVisor] ERROR: Invalid boolean value: $1" >&2
            exit 1
            ;;
    esac
}

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 62

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
            echo "[DebVisor] ERROR: Invalid boolean value: $1" >&2
            exit 1
            ;;
    esac
}

DEBVISOR_FIRMWARE_CHROOT="$(normalize_bool "${DEBVISOR_FIRMWARE_CHROOT}")"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 63

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
            exit 1
            ;;
    esac
}

DEBVISOR_FIRMWARE_CHROOT="$(normalize_bool "${DEBVISOR_FIRMWARE_CHROOT}")"
DEBVISOR_FIRMWARE_BINARY="$(normalize_bool "${DEBVISOR_FIRMWARE_BINARY}")"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 64

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
            ;;
    esac
}

DEBVISOR_FIRMWARE_CHROOT="$(normalize_bool "${DEBVISOR_FIRMWARE_CHROOT}")"
DEBVISOR_FIRMWARE_BINARY="$(normalize_bool "${DEBVISOR_FIRMWARE_BINARY}")"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 65

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    esac
}

DEBVISOR_FIRMWARE_CHROOT="$(normalize_bool "${DEBVISOR_FIRMWARE_CHROOT}")"
DEBVISOR_FIRMWARE_BINARY="$(normalize_bool "${DEBVISOR_FIRMWARE_BINARY}")"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 66

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
}

DEBVISOR_FIRMWARE_CHROOT="$(normalize_bool "${DEBVISOR_FIRMWARE_CHROOT}")"
DEBVISOR_FIRMWARE_BINARY="$(normalize_bool "${DEBVISOR_FIRMWARE_BINARY}")"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "${script_dir}/.." && pwd)"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 67

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

DEBVISOR_FIRMWARE_CHROOT="$(normalize_bool "${DEBVISOR_FIRMWARE_CHROOT}")"
DEBVISOR_FIRMWARE_BINARY="$(normalize_bool "${DEBVISOR_FIRMWARE_BINARY}")"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "${script_dir}/.." && pwd)"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 68

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
DEBVISOR_FIRMWARE_CHROOT="$(normalize_bool "${DEBVISOR_FIRMWARE_CHROOT}")"
DEBVISOR_FIRMWARE_BINARY="$(normalize_bool "${DEBVISOR_FIRMWARE_BINARY}")"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "${script_dir}/.." && pwd)"

cd "${project_root}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 69

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
DEBVISOR_FIRMWARE_BINARY="$(normalize_bool "${DEBVISOR_FIRMWARE_BINARY}")"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "${script_dir}/.." && pwd)"

cd "${project_root}"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 70

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "${script_dir}/.." && pwd)"

cd "${project_root}"

if ! command -v lb >/dev/null; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 71

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "${script_dir}/.." && pwd)"

cd "${project_root}"

if ! command -v lb >/dev/null; then
    echo "live-build not installed. Install prerequisites first." >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 72

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
project_root="$(cd "${script_dir}/.." && pwd)"

cd "${project_root}"

if ! command -v lb >/dev/null; then
    echo "live-build not installed. Install prerequisites first." >&2
    exit 1
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 73

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

cd "${project_root}"

if ! command -v lb >/dev/null; then
    echo "live-build not installed. Install prerequisites first." >&2
    exit 1
fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 74

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
cd "${project_root}"

if ! command -v lb >/dev/null; then
    echo "live-build not installed. Install prerequisites first." >&2
    exit 1
fi

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 75

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

if ! command -v lb >/dev/null; then
    echo "live-build not installed. Install prerequisites first." >&2
    exit 1
fi

if [! -f /etc/debian_version]; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 76

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
if ! command -v lb >/dev/null; then
    echo "live-build not installed. Install prerequisites first." >&2
    exit 1
fi

if [! -f /etc/debian_version]; then
    echo "[DebVisor] WARNING: This script is intended to run on Debian-based hosts." >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 77

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    echo "live-build not installed. Install prerequisites first." >&2
    exit 1
fi

if [! -f /etc/debian_version]; then
    echo "[DebVisor] WARNING: This script is intended to run on Debian-based hosts." >&2
else
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 78

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    exit 1
fi

if [! -f /etc/debian_version]; then
    echo "[DebVisor] WARNING: This script is intended to run on Debian-based hosts." >&2
else
    host_debian="$(cut -d. -f1 /dev/null || echo "")"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 79

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
fi

if [! -f /etc/debian_version]; then
    echo "[DebVisor] WARNING: This script is intended to run on Debian-based hosts." >&2
else
    host_debian="$(cut -d. -f1 /dev/null || echo "")"
    case "${host_debian}" in
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 80

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

if [! -f /etc/debian_version]; then
    echo "[DebVisor] WARNING: This script is intended to run on Debian-based hosts." >&2
else
    host_debian="$(cut -d. -f1 /dev/null || echo "")"
    case "${host_debian}" in
        '' )
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 81

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
if [! -f /etc/debian_version]; then
    echo "[DebVisor] WARNING: This script is intended to run on Debian-based hosts." >&2
else
    host_debian="$(cut -d. -f1 /dev/null || echo "")"
    case "${host_debian}" in
        '' )
            echo "[DebVisor] WARNING: Unable to parse /etc/debian_version; continuing without version check." >&2 ;;
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 82

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    echo "[DebVisor] WARNING: This script is intended to run on Debian-based hosts." >&2
else
    host_debian="$(cut -d. -f1 /dev/null || echo "")"
    case "${host_debian}" in
        '' )
            echo "[DebVisor] WARNING: Unable to parse /etc/debian_version; continuing without version check." >&2 ;;
        * )
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 83

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
else
    host_debian="$(cut -d. -f1 /dev/null || echo "")"
    case "${host_debian}" in
        '' )
            echo "[DebVisor] WARNING: Unable to parse /etc/debian_version; continuing without version check." >&2 ;;
        * )
            # For now we only warn if running on releases older than bookworm (12).
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 84

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    host_debian="$(cut -d. -f1 /dev/null || echo "")"
    case "${host_debian}" in
        '' )
            echo "[DebVisor] WARNING: Unable to parse /etc/debian_version; continuing without version check." >&2 ;;
        * )
            # For now we only warn if running on releases older than bookworm (12).
            if ["${host_debian}" -lt 12] 2>/dev/null; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 85

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    case "${host_debian}" in
        '' )
            echo "[DebVisor] WARNING: Unable to parse /etc/debian_version; continuing without version check." >&2 ;;
        * )
            # For now we only warn if running on releases older than bookworm (12).
            if ["${host_debian}" -lt 12] 2>/dev/null; then
                echo "[DebVisor] WARNING: Host Debian release (${host_debian}) is older than recommended (bookworm/12+)." >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 86

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        '' )
            echo "[DebVisor] WARNING: Unable to parse /etc/debian_version; continuing without version check." >&2 ;;
        * )
            # For now we only warn if running on releases older than bookworm (12).
            if ["${host_debian}" -lt 12] 2>/dev/null; then
                echo "[DebVisor] WARNING: Host Debian release (${host_debian}) is older than recommended (bookworm/12+)." >&2
            fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 87

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
            echo "[DebVisor] WARNING: Unable to parse /etc/debian_version; continuing without version check." >&2 ;;
        * )
            # For now we only warn if running on releases older than bookworm (12).
            if ["${host_debian}" -lt 12] 2>/dev/null; then
                echo "[DebVisor] WARNING: Host Debian release (${host_debian}) is older than recommended (bookworm/12+)." >&2
            fi
            ;;
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 88

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        * )
            # For now we only warn if running on releases older than bookworm (12).
            if ["${host_debian}" -lt 12] 2>/dev/null; then
                echo "[DebVisor] WARNING: Host Debian release (${host_debian}) is older than recommended (bookworm/12+)." >&2
            fi
            ;;
    esac
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 89

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
            # For now we only warn if running on releases older than bookworm (12).
            if ["${host_debian}" -lt 12] 2>/dev/null; then
                echo "[DebVisor] WARNING: Host Debian release (${host_debian}) is older than recommended (bookworm/12+)." >&2
            fi
            ;;
    esac
fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 90

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
            if ["${host_debian}" -lt 12] 2>/dev/null; then
                echo "[DebVisor] WARNING: Host Debian release (${host_debian}) is older than recommended (bookworm/12+)." >&2
            fi
            ;;
    esac
fi

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 91

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
                echo "[DebVisor] WARNING: Host Debian release (${host_debian}) is older than recommended (bookworm/12+)." >&2
            fi
            ;;
    esac
fi

for bin in debootstrap xorriso; do
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 92

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
            fi
            ;;
    esac
fi

for bin in debootstrap xorriso; do
    if ! command -v "$bin" >/dev/null 2>&1; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 93

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
            ;;
    esac
fi

for bin in debootstrap xorriso; do
    if ! command -v "$bin" >/dev/null 2>&1; then
        echo "[DebVisor] ERROR: Required tool missing: $bin" >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 94

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    esac
fi

for bin in debootstrap xorriso; do
    if ! command -v "$bin" >/dev/null 2>&1; then
        echo "[DebVisor] ERROR: Required tool missing: $bin" >&2
        exit 1
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 95

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
fi

for bin in debootstrap xorriso; do
    if ! command -v "$bin" >/dev/null 2>&1; then
        echo "[DebVisor] ERROR: Required tool missing: $bin" >&2
        exit 1
    fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 96

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

for bin in debootstrap xorriso; do
    if ! command -v "$bin" >/dev/null 2>&1; then
        echo "[DebVisor] ERROR: Required tool missing: $bin" >&2
        exit 1
    fi
done
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 97

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
for bin in debootstrap xorriso; do
    if ! command -v "$bin" >/dev/null 2>&1; then
        echo "[DebVisor] ERROR: Required tool missing: $bin" >&2
        exit 1
    fi
done

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 98

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    if ! command -v "$bin" >/dev/null 2>&1; then
        echo "[DebVisor] ERROR: Required tool missing: $bin" >&2
        exit 1
    fi
done

if ! command -v shellcheck >/dev/null 2>&1; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 99

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        echo "[DebVisor] ERROR: Required tool missing: $bin" >&2
        exit 1
    fi
done

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[DebVisor] WARNING: shellcheck not found; build scripts will not be linted. Install it with 'apt install shellcheck' on Debian-based hosts." >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 100

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        exit 1
    fi
done

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[DebVisor] WARNING: shellcheck not found; build scripts will not be linted. Install it with 'apt install shellcheck' on Debian-based hosts." >&2
fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 101

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    fi
done

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[DebVisor] WARNING: shellcheck not found; build scripts will not be linted. Install it with 'apt install shellcheck' on Debian-based hosts." >&2
fi

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 102

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
done

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[DebVisor] WARNING: shellcheck not found; build scripts will not be linted. Install it with 'apt install shellcheck' on Debian-based hosts." >&2
fi

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"] && ! command -v gpg >/dev/null 2>&1; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 103

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[DebVisor] WARNING: shellcheck not found; build scripts will not be linted. Install it with 'apt install shellcheck' on Debian-based hosts." >&2
fi

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"] && ! command -v gpg >/dev/null 2>&1; then
    echo "[DebVisor] ERROR: DEBVISOR_SIGN_ISO=1 but gpg is not installed." >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 104

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[DebVisor] WARNING: shellcheck not found; build scripts will not be linted. Install it with 'apt install shellcheck' on Debian-based hosts." >&2
fi

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"] && ! command -v gpg >/dev/null 2>&1; then
    echo "[DebVisor] ERROR: DEBVISOR_SIGN_ISO=1 but gpg is not installed." >&2
    exit 1
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 105

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    echo "[DebVisor] WARNING: shellcheck not found; build scripts will not be linted. Install it with 'apt install shellcheck' on Debian-based hosts." >&2
fi

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"] && ! command -v gpg >/dev/null 2>&1; then
    echo "[DebVisor] ERROR: DEBVISOR_SIGN_ISO=1 but gpg is not installed." >&2
    exit 1
fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 106

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
fi

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"] && ! command -v gpg >/dev/null 2>&1; then
    echo "[DebVisor] ERROR: DEBVISOR_SIGN_ISO=1 but gpg is not installed." >&2
    exit 1
fi

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 107

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"] && ! command -v gpg >/dev/null 2>&1; then
    echo "[DebVisor] ERROR: DEBVISOR_SIGN_ISO=1 but gpg is not installed." >&2
    exit 1
fi

trap 'echo "[DebVisor] ERROR: build failed" >&2' ERR
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 108

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
if ["${DEBVISOR_SIGN_ISO:-0}" = "1"] && ! command -v gpg >/dev/null 2>&1; then
    echo "[DebVisor] ERROR: DEBVISOR_SIGN_ISO=1 but gpg is not installed." >&2
    exit 1
fi

trap 'echo "[DebVisor] ERROR: build failed" >&2' ERR

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 109

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    echo "[DebVisor] ERROR: DEBVISOR_SIGN_ISO=1 but gpg is not installed." >&2
    exit 1
fi

trap 'echo "[DebVisor] ERROR: build failed" >&2' ERR

echo "[DebVisor] Project root: ${project_root}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 110

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    exit 1
fi

trap 'echo "[DebVisor] ERROR: build failed" >&2' ERR

echo "[DebVisor] Project root: ${project_root}"
echo "[DebVisor] Target distribution: ${DEBVISOR_DIST}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 111

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
fi

trap 'echo "[DebVisor] ERROR: build failed" >&2' ERR

echo "[DebVisor] Project root: ${project_root}"
echo "[DebVisor] Target distribution: ${DEBVISOR_DIST}"
echo "[DebVisor] FAST mode: ${DEBVISOR_FAST} (0=clean,1=no-clean)"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 112

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

trap 'echo "[DebVisor] ERROR: build failed" >&2' ERR

echo "[DebVisor] Project root: ${project_root}"
echo "[DebVisor] Target distribution: ${DEBVISOR_DIST}"
echo "[DebVisor] FAST mode: ${DEBVISOR_FAST} (0=clean,1=no-clean)"
echo "[DebVisor] Architecture: ${DEBVISOR_ARCH}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 113

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
trap 'echo "[DebVisor] ERROR: build failed" >&2' ERR

echo "[DebVisor] Project root: ${project_root}"
echo "[DebVisor] Target distribution: ${DEBVISOR_DIST}"
echo "[DebVisor] FAST mode: ${DEBVISOR_FAST} (0=clean,1=no-clean)"
echo "[DebVisor] Architecture: ${DEBVISOR_ARCH}"
if [-n "${DEBVISOR_VERSION}"]; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 114

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

echo "[DebVisor] Project root: ${project_root}"
echo "[DebVisor] Target distribution: ${DEBVISOR_DIST}"
echo "[DebVisor] FAST mode: ${DEBVISOR_FAST} (0=clean,1=no-clean)"
echo "[DebVisor] Architecture: ${DEBVISOR_ARCH}"
if [-n "${DEBVISOR_VERSION}"]; then
    echo "[DebVisor] Version tag: ${DEBVISOR_VERSION}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 115

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
echo "[DebVisor] Project root: ${project_root}"
echo "[DebVisor] Target distribution: ${DEBVISOR_DIST}"
echo "[DebVisor] FAST mode: ${DEBVISOR_FAST} (0=clean,1=no-clean)"
echo "[DebVisor] Architecture: ${DEBVISOR_ARCH}"
if [-n "${DEBVISOR_VERSION}"]; then
    echo "[DebVisor] Version tag: ${DEBVISOR_VERSION}"
fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 116

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
echo "[DebVisor] Target distribution: ${DEBVISOR_DIST}"
echo "[DebVisor] FAST mode: ${DEBVISOR_FAST} (0=clean,1=no-clean)"
echo "[DebVisor] Architecture: ${DEBVISOR_ARCH}"
if [-n "${DEBVISOR_VERSION}"]; then
    echo "[DebVisor] Version tag: ${DEBVISOR_VERSION}"
fi
echo "[DebVisor] Mirror (bootstrap): ${DEBVISOR_MIRROR_BOOTSTRAP}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 117

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
echo "[DebVisor] FAST mode: ${DEBVISOR_FAST} (0=clean,1=no-clean)"
echo "[DebVisor] Architecture: ${DEBVISOR_ARCH}"
if [-n "${DEBVISOR_VERSION}"]; then
    echo "[DebVisor] Version tag: ${DEBVISOR_VERSION}"
fi
echo "[DebVisor] Mirror (bootstrap): ${DEBVISOR_MIRROR_BOOTSTRAP}"
echo "[DebVisor] Mirror (binary):    ${DEBVISOR_MIRROR_BINARY}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 118

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
echo "[DebVisor] Architecture: ${DEBVISOR_ARCH}"
if [-n "${DEBVISOR_VERSION}"]; then
    echo "[DebVisor] Version tag: ${DEBVISOR_VERSION}"
fi
echo "[DebVisor] Mirror (bootstrap): ${DEBVISOR_MIRROR_BOOTSTRAP}"
echo "[DebVisor] Mirror (binary):    ${DEBVISOR_MIRROR_BINARY}"
echo "[DebVisor] Firmware flags:     chroot=${DEBVISOR_FIRMWARE_CHROOT}, binary=${DEBVISOR_FIRMWARE_BINARY}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 119

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
if [-n "${DEBVISOR_VERSION}"]; then
    echo "[DebVisor] Version tag: ${DEBVISOR_VERSION}"
fi
echo "[DebVisor] Mirror (bootstrap): ${DEBVISOR_MIRROR_BOOTSTRAP}"
echo "[DebVisor] Mirror (binary):    ${DEBVISOR_MIRROR_BINARY}"
echo "[DebVisor] Firmware flags:     chroot=${DEBVISOR_FIRMWARE_CHROOT}, binary=${DEBVISOR_FIRMWARE_BINARY}"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 120

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    echo "[DebVisor] Version tag: ${DEBVISOR_VERSION}"
fi
echo "[DebVisor] Mirror (bootstrap): ${DEBVISOR_MIRROR_BOOTSTRAP}"
echo "[DebVisor] Mirror (binary):    ${DEBVISOR_MIRROR_BINARY}"
echo "[DebVisor] Firmware flags:     chroot=${DEBVISOR_FIRMWARE_CHROOT}, binary=${DEBVISOR_FIRMWARE_BINARY}"

case "${DEBVISOR_ARCH}" in
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 121

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
fi
echo "[DebVisor] Mirror (bootstrap): ${DEBVISOR_MIRROR_BOOTSTRAP}"
echo "[DebVisor] Mirror (binary):    ${DEBVISOR_MIRROR_BINARY}"
echo "[DebVisor] Firmware flags:     chroot=${DEBVISOR_FIRMWARE_CHROOT}, binary=${DEBVISOR_FIRMWARE_BINARY}"

case "${DEBVISOR_ARCH}" in
    amd64|arm64)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 122

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
echo "[DebVisor] Mirror (bootstrap): ${DEBVISOR_MIRROR_BOOTSTRAP}"
echo "[DebVisor] Mirror (binary):    ${DEBVISOR_MIRROR_BINARY}"
echo "[DebVisor] Firmware flags:     chroot=${DEBVISOR_FIRMWARE_CHROOT}, binary=${DEBVISOR_FIRMWARE_BINARY}"

case "${DEBVISOR_ARCH}" in
    amd64|arm64)
        ;;
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 123

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
echo "[DebVisor] Mirror (binary):    ${DEBVISOR_MIRROR_BINARY}"
echo "[DebVisor] Firmware flags:     chroot=${DEBVISOR_FIRMWARE_CHROOT}, binary=${DEBVISOR_FIRMWARE_BINARY}"

case "${DEBVISOR_ARCH}" in
    amd64|arm64)
        ;;
    *)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 124

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
echo "[DebVisor] Firmware flags:     chroot=${DEBVISOR_FIRMWARE_CHROOT}, binary=${DEBVISOR_FIRMWARE_BINARY}"

case "${DEBVISOR_ARCH}" in
    amd64|arm64)
        ;;
    *)
        echo "[DebVisor] ERROR: Unsupported DEBVISOR_ARCH: ${DEBVISOR_ARCH} (allowed: amd64, arm64)" >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 125

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

case "${DEBVISOR_ARCH}" in
    amd64|arm64)
        ;;
    *)
        echo "[DebVisor] ERROR: Unsupported DEBVISOR_ARCH: ${DEBVISOR_ARCH} (allowed: amd64, arm64)" >&2
        exit 1
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 126

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
case "${DEBVISOR_ARCH}" in
    amd64|arm64)
        ;;
    *)
        echo "[DebVisor] ERROR: Unsupported DEBVISOR_ARCH: ${DEBVISOR_ARCH} (allowed: amd64, arm64)" >&2
        exit 1
        ;;
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 127

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    amd64|arm64)
        ;;
    *)
        echo "[DebVisor] ERROR: Unsupported DEBVISOR_ARCH: ${DEBVISOR_ARCH} (allowed: amd64, arm64)" >&2
        exit 1
        ;;
esac
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 128

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        ;;
    *)
        echo "[DebVisor] ERROR: Unsupported DEBVISOR_ARCH: ${DEBVISOR_ARCH} (allowed: amd64, arm64)" >&2
        exit 1
        ;;
esac

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 129

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    *)
        echo "[DebVisor] ERROR: Unsupported DEBVISOR_ARCH: ${DEBVISOR_ARCH} (allowed: amd64, arm64)" >&2
        exit 1
        ;;
esac

if [! -f config/preseed.cfg]; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 130

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        echo "[DebVisor] ERROR: Unsupported DEBVISOR_ARCH: ${DEBVISOR_ARCH} (allowed: amd64, arm64)" >&2
        exit 1
        ;;
esac

if [! -f config/preseed.cfg]; then
    echo "[DebVisor] WARNING: config/preseed.cfg not found in project root" >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 131

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        exit 1
        ;;
esac

if [! -f config/preseed.cfg]; then
    echo "[DebVisor] WARNING: config/preseed.cfg not found in project root" >&2
fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 132

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        ;;
esac

if [! -f config/preseed.cfg]; then
    echo "[DebVisor] WARNING: config/preseed.cfg not found in project root" >&2
fi

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 133

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
esac

if [! -f config/preseed.cfg]; then
    echo "[DebVisor] WARNING: config/preseed.cfg not found in project root" >&2
fi

required_paths=(
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 134

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

if [! -f config/preseed.cfg]; then
    echo "[DebVisor] WARNING: config/preseed.cfg not found in project root" >&2
fi

required_paths=(
    "config/package-lists"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 135

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
if [! -f config/preseed.cfg]; then
    echo "[DebVisor] WARNING: config/preseed.cfg not found in project root" >&2
fi

required_paths=(
    "config/package-lists"
    "config/includes.chroot"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 136

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    echo "[DebVisor] WARNING: config/preseed.cfg not found in project root" >&2
fi

required_paths=(
    "config/package-lists"
    "config/includes.chroot"
)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 137

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
fi

required_paths=(
    "config/package-lists"
    "config/includes.chroot"
)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 138

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

required_paths=(
    "config/package-lists"
    "config/includes.chroot"
)

for path in "${required_paths[@]}"; do
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 139

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
required_paths=(
    "config/package-lists"
    "config/includes.chroot"
)

for path in "${required_paths[@]}"; do
    if [! -e "${path}"]; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 140

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    "config/package-lists"
    "config/includes.chroot"
)

for path in "${required_paths[@]}"; do
    if [! -e "${path}"]; then
        echo "[DebVisor] ERROR: required path missing: ${path}" >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 141

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    "config/includes.chroot"
)

for path in "${required_paths[@]}"; do
    if [! -e "${path}"]; then
        echo "[DebVisor] ERROR: required path missing: ${path}" >&2
        exit 1
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 142

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
)

for path in "${required_paths[@]}"; do
    if [! -e "${path}"]; then
        echo "[DebVisor] ERROR: required path missing: ${path}" >&2
        exit 1
    fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 143

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

for path in "${required_paths[@]}"; do
    if [! -e "${path}"]; then
        echo "[DebVisor] ERROR: required path missing: ${path}" >&2
        exit 1
    fi
done
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 144

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
for path in "${required_paths[@]}"; do
    if [! -e "${path}"]; then
        echo "[DebVisor] ERROR: required path missing: ${path}" >&2
        exit 1
    fi
done

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 145

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    if [! -e "${path}"]; then
        echo "[DebVisor] ERROR: required path missing: ${path}" >&2
        exit 1
    fi
done

SKIP_CONFIG=0
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 146

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        echo "[DebVisor] ERROR: required path missing: ${path}" >&2
        exit 1
    fi
done

SKIP_CONFIG=0
case "${DEBVISOR_FAST}" in
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 147

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        exit 1
    fi
done

SKIP_CONFIG=0
case "${DEBVISOR_FAST}" in
    1. ```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 148

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
fi
```python

done

SKIP_CONFIG=0
case "${DEBVISOR_FAST}" in

```python
1. echo "[DebVisor] FAST=0: full clean & re-configure"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 149

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

done

SKIP_CONFIG=0
case "${DEBVISOR_FAST}" in

```python
1. echo "[DebVisor] FAST=0: full clean & re-configure"
    lb clean || true
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 150

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

SKIP_CONFIG=0
case "${DEBVISOR_FAST}" in

```python
1. echo "[DebVisor] FAST=0: full clean & re-configure"
    lb clean || true
    ;;
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 151

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

SKIP_CONFIG=0
case "${DEBVISOR_FAST}" in

```python
1. echo "[DebVisor] FAST=0: full clean & re-configure"
    lb clean || true
    ;;
1. ```python

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 152

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
case "${DEBVISOR_FAST}" in
    1. echo "[DebVisor] FAST=0: full clean & re-configure"
        lb clean || true
        ;;
    1. echo "[DebVisor] FAST=1: skipping clean, will re-configure"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 153

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    1. echo "[DebVisor] FAST=0: full clean & re-configure"
        lb clean || true
        ;;
    1. echo "[DebVisor] FAST=1: skipping clean, will re-configure"
        ;;
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 154

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
        echo "[DebVisor] FAST=0: full clean & re-configure"
        lb clean || true
        ;;
    1. echo "[DebVisor] FAST=1: skipping clean, will re-configure"
        ;;
    1. ```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 155

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    lb clean || true
    ;;
1. echo "[DebVisor] FAST=1: skipping clean, will re-configure"
    ;;
1. echo "[DebVisor] FAST=2: skipping clean and config"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 156

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    ;;
1. echo "[DebVisor] FAST=1: skipping clean, will re-configure"
    ;;
1. echo "[DebVisor] FAST=2: skipping clean and config"
    SKIP_CONFIG=1
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 157

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
1. echo "[DebVisor] FAST=1: skipping clean, will re-configure"
    ;;
1. echo "[DebVisor] FAST=2: skipping clean and config"
    SKIP_CONFIG=1
    ;;
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 158

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    echo "[DebVisor] FAST=1: skipping clean, will re-configure"
    ;;
1. echo "[DebVisor] FAST=2: skipping clean and config"
    SKIP_CONFIG=1
    ;;
*)
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 159

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    ;;
1. echo "[DebVisor] FAST=2: skipping clean and config"
    SKIP_CONFIG=1
    ;;
*)
    echo "[DebVisor] ERROR: Invalid DEBVISOR_FAST: ${DEBVISOR_FAST} (use 0,1,2)" >&2
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 160

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
1. echo "[DebVisor] FAST=2: skipping clean and config"
    SKIP_CONFIG=1
    ;;
*)
    echo "[DebVisor] ERROR: Invalid DEBVISOR_FAST: ${DEBVISOR_FAST} (use 0,1,2)" >&2
    exit 1
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 161

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    echo "[DebVisor] FAST=2: skipping clean and config"
    SKIP_CONFIG=1
    ;;
*)
    echo "[DebVisor] ERROR: Invalid DEBVISOR_FAST: ${DEBVISOR_FAST} (use 0,1,2)" >&2
    exit 1
    ;;
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 162

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    SKIP_CONFIG=1
    ;;
*)
    echo "[DebVisor] ERROR: Invalid DEBVISOR_FAST: ${DEBVISOR_FAST} (use 0,1,2)" >&2
    exit 1
    ;;
```python

esac

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 163

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    ;;
*)
    echo "[DebVisor] ERROR: Invalid DEBVISOR_FAST: ${DEBVISOR_FAST} (use 0,1,2)" >&2
    exit 1
    ;;
```python

esac

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 164

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
*)
    echo "[DebVisor] ERROR: Invalid DEBVISOR_FAST: ${DEBVISOR_FAST} (use 0,1,2)" >&2
    exit 1
    ;;
```python

esac

if ["${SKIP_CONFIG}" -ne 1]; then

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 165

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    echo "[DebVisor] ERROR: Invalid DEBVISOR_FAST: ${DEBVISOR_FAST} (use 0,1,2)" >&2
    exit 1
    ;;
```python

esac

if ["${SKIP_CONFIG}" -ne 1]; then

```python
echo "[DebVisor] Configuring live-build"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 166

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    exit 1
    ;;
```python

esac

if ["${SKIP_CONFIG}" -ne 1]; then

```python
echo "[DebVisor] Configuring live-build"
lb config \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 167

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    ;;
```python

esac

if ["${SKIP_CONFIG}" -ne 1]; then

```python
echo "[DebVisor] Configuring live-build"
lb config \
--mode debian \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 168

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

esac

if ["${SKIP_CONFIG}" -ne 1]; then

```python
echo "[DebVisor] Configuring live-build"
lb config \
--mode debian \
--distribution "${DEBVISOR_DIST}" \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 170

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

if ["${SKIP_CONFIG}" -ne 1]; then

```python
echo "[DebVisor] Configuring live-build"
lb config \
--mode debian \
--distribution "${DEBVISOR_DIST}" \
--binary-images iso-hybrid \
--architectures "${DEBVISOR_ARCH}" \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 171

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
echo "[DebVisor] Configuring live-build"
lb config \
--mode debian \
--distribution "${DEBVISOR_DIST}" \
--binary-images iso-hybrid \
--architectures "${DEBVISOR_ARCH}" \
--linux-flavours "${DEBVISOR_ARCH}" \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 172

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
lb config \
--mode debian \
--distribution "${DEBVISOR_DIST}" \
--binary-images iso-hybrid \
--architectures "${DEBVISOR_ARCH}" \
--linux-flavours "${DEBVISOR_ARCH}" \
--apt-recommends true \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 173

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--mode debian \
--distribution "${DEBVISOR_DIST}" \
--binary-images iso-hybrid \
--architectures "${DEBVISOR_ARCH}" \
--linux-flavours "${DEBVISOR_ARCH}" \
--apt-recommends true \
--archive-areas "main contrib non-free non-free-firmware" \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 174

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--distribution "${DEBVISOR_DIST}" \
--binary-images iso-hybrid \
--architectures "${DEBVISOR_ARCH}" \
--linux-flavours "${DEBVISOR_ARCH}" \
--apt-recommends true \
--archive-areas "main contrib non-free non-free-firmware" \
--debian-installer live \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 175

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--binary-images iso-hybrid \
--architectures "${DEBVISOR_ARCH}" \
--linux-flavours "${DEBVISOR_ARCH}" \
--apt-recommends true \
--archive-areas "main contrib non-free non-free-firmware" \
--debian-installer live \
--debian-installer-gui false \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 176

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--architectures "${DEBVISOR_ARCH}" \
--linux-flavours "${DEBVISOR_ARCH}" \
--apt-recommends true \
--archive-areas "main contrib non-free non-free-firmware" \
--debian-installer live \
--debian-installer-gui false \
--debian-installer-preseed config/preseed.cfg \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 177

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--linux-flavours "${DEBVISOR_ARCH}" \
--apt-recommends true \
--archive-areas "main contrib non-free non-free-firmware" \
--debian-installer live \
--debian-installer-gui false \
--debian-installer-preseed config/preseed.cfg \
--bootloaders grub-efi \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 178

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--apt-recommends true \
--archive-areas "main contrib non-free non-free-firmware" \
--debian-installer live \
--debian-installer-gui false \
--debian-installer-preseed config/preseed.cfg \
--bootloaders grub-efi \
--system live \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 179

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--archive-areas "main contrib non-free non-free-firmware" \
--debian-installer live \
--debian-installer-gui false \
--debian-installer-preseed config/preseed.cfg \
--bootloaders grub-efi \
--system live \
--firmware-chroot "${DEBVISOR_FIRMWARE_CHROOT}" \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 180

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--debian-installer live \
--debian-installer-gui false \
--debian-installer-preseed config/preseed.cfg \
--bootloaders grub-efi \
--system live \
--firmware-chroot "${DEBVISOR_FIRMWARE_CHROOT}" \
--firmware-binary "${DEBVISOR_FIRMWARE_BINARY}" \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 181

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--debian-installer-gui false \
--debian-installer-preseed config/preseed.cfg \
--bootloaders grub-efi \
--system live \
--firmware-chroot "${DEBVISOR_FIRMWARE_CHROOT}" \
--firmware-binary "${DEBVISOR_FIRMWARE_BINARY}" \
--updates true \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 182

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--debian-installer-preseed config/preseed.cfg \
--bootloaders grub-efi \
--system live \
--firmware-chroot "${DEBVISOR_FIRMWARE_CHROOT}" \
--firmware-binary "${DEBVISOR_FIRMWARE_BINARY}" \
--updates true \
--security true \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 183

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--bootloaders grub-efi \
--system live \
--firmware-chroot "${DEBVISOR_FIRMWARE_CHROOT}" \
--firmware-binary "${DEBVISOR_FIRMWARE_BINARY}" \
--updates true \
--security true \
--backports true \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 184

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--system live \
--firmware-chroot "${DEBVISOR_FIRMWARE_CHROOT}" \
--firmware-binary "${DEBVISOR_FIRMWARE_BINARY}" \
--updates true \
--security true \
--backports true \
--iso-application "DebVisor" \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 185

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--firmware-chroot "${DEBVISOR_FIRMWARE_CHROOT}" \
--firmware-binary "${DEBVISOR_FIRMWARE_BINARY}" \
--updates true \
--security true \
--backports true \
--iso-application "DebVisor" \
--iso-volume "DebVisor" \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 186

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--firmware-binary "${DEBVISOR_FIRMWARE_BINARY}" \
--updates true \
--security true \
--backports true \
--iso-application "DebVisor" \
--iso-volume "DebVisor" \
--mirror-bootstrap "${DEBVISOR_MIRROR_BOOTSTRAP}" \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 187

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--updates true \
--security true \
--backports true \
--iso-application "DebVisor" \
--iso-volume "DebVisor" \
--mirror-bootstrap "${DEBVISOR_MIRROR_BOOTSTRAP}" \
--mirror-binary "${DEBVISOR_MIRROR_BINARY}" \
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 188

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--security true \
--backports true \
--iso-application "DebVisor" \
--iso-volume "DebVisor" \
--mirror-bootstrap "${DEBVISOR_MIRROR_BOOTSTRAP}" \
--mirror-binary "${DEBVISOR_MIRROR_BINARY}" \
--grub-splash none
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 189

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--backports true \
--iso-application "DebVisor" \
--iso-volume "DebVisor" \
--mirror-bootstrap "${DEBVISOR_MIRROR_BOOTSTRAP}" \
--mirror-binary "${DEBVISOR_MIRROR_BINARY}" \
--grub-splash none
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 190

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--iso-application "DebVisor" \
--iso-volume "DebVisor" \
--mirror-bootstrap "${DEBVISOR_MIRROR_BOOTSTRAP}" \
--mirror-binary "${DEBVISOR_MIRROR_BINARY}" \
--grub-splash none
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 191

**Tool:**shellcheck |**Code:**`2215` |**Severity:** WARNING

**Message:** This flag is used as a command name. Bad line break or missing [..]?

### Context
```python

```python
--iso-volume "DebVisor" \
--mirror-bootstrap "${DEBVISOR_MIRROR_BOOTSTRAP}" \
--mirror-binary "${DEBVISOR_MIRROR_BINARY}" \
--grub-splash none
```python

fi

echo "[DebVisor] Syncing addons playbook (if script present)"

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 191

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
--iso-volume "DebVisor" \
--mirror-bootstrap "${DEBVISOR_MIRROR_BOOTSTRAP}" \
--mirror-binary "${DEBVISOR_MIRROR_BINARY}" \
--grub-splash none
```python

fi

echo "[DebVisor] Syncing addons playbook (if script present)"

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 192

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
--mirror-bootstrap "${DEBVISOR_MIRROR_BOOTSTRAP}" \
--mirror-binary "${DEBVISOR_MIRROR_BINARY}" \
--grub-splash none
```python

fi

echo "[DebVisor] Syncing addons playbook (if script present)"
if [-x build/sync-addons-playbook.sh]; then

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 193

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
--mirror-binary "${DEBVISOR_MIRROR_BINARY}" \
--grub-splash none
```python

fi

echo "[DebVisor] Syncing addons playbook (if script present)"
if [-x build/sync-addons-playbook.sh]; then

```python
build/sync-addons-playbook.sh
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 194

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
--grub-splash none
```python

fi

echo "[DebVisor] Syncing addons playbook (if script present)"
if [-x build/sync-addons-playbook.sh]; then

```python
build/sync-addons-playbook.sh
```python

else

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 195

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

fi

echo "[DebVisor] Syncing addons playbook (if script present)"
if [-x build/sync-addons-playbook.sh]; then

```python
build/sync-addons-playbook.sh
```python

else

```python
echo "[DebVisor] Skipping addons sync (build/sync-addons-playbook.sh not executable)"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 196

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

echo "[DebVisor] Syncing addons playbook (if script present)"
if [-x build/sync-addons-playbook.sh]; then

```python
build/sync-addons-playbook.sh
```python

else

```python
echo "[DebVisor] Skipping addons sync (build/sync-addons-playbook.sh not executable)"
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 197

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

echo "[DebVisor] Syncing addons playbook (if script present)"
if [-x build/sync-addons-playbook.sh]; then

```python
build/sync-addons-playbook.sh
```python

else

```python
echo "[DebVisor] Skipping addons sync (build/sync-addons-playbook.sh not executable)"
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 198

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

if [-x build/sync-addons-playbook.sh]; then

```python
build/sync-addons-playbook.sh
```python

else

```python
echo "[DebVisor] Skipping addons sync (build/sync-addons-playbook.sh not executable)"
```python

fi

if ["${DEBVISOR_SELFTEST:-0}" = "1"]; then

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 199

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
build/sync-addons-playbook.sh
```python

else

```python
echo "[DebVisor] Skipping addons sync (build/sync-addons-playbook.sh not executable)"
```python

fi

if ["${DEBVISOR_SELFTEST:-0}" = "1"]; then

```python
echo "[DebVisor] SELFTEST mode enabled: running lb config only (no build)"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 200

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

else

```python
echo "[DebVisor] Skipping addons sync (build/sync-addons-playbook.sh not executable)"
```python

fi

if ["${DEBVISOR_SELFTEST:-0}" = "1"]; then

```python
echo "[DebVisor] SELFTEST mode enabled: running lb config only (no build)"
exit 0
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 201

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
echo "[DebVisor] Skipping addons sync (build/sync-addons-playbook.sh not executable)"
```python

fi

if ["${DEBVISOR_SELFTEST:-0}" = "1"]; then

```python
echo "[DebVisor] SELFTEST mode enabled: running lb config only (no build)"
exit 0
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 202

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

fi

if ["${DEBVISOR_SELFTEST:-0}" = "1"]; then

```python
echo "[DebVisor] SELFTEST mode enabled: running lb config only (no build)"
exit 0
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 203

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

if ["${DEBVISOR_SELFTEST:-0}" = "1"]; then

```python
echo "[DebVisor] SELFTEST mode enabled: running lb config only (no build)"
exit 0
```python

fi

if ["${DEBVISOR_DRYRUN:-0}" = "1"]; then

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 204

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

if ["${DEBVISOR_SELFTEST:-0}" = "1"]; then

```python
echo "[DebVisor] SELFTEST mode enabled: running lb config only (no build)"
exit 0
```python

fi

if ["${DEBVISOR_DRYRUN:-0}" = "1"]; then

```python
echo "[DebVisor] DRYRUN enabled: configuration validated, skipping lb build"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 205

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
echo "[DebVisor] SELFTEST mode enabled: running lb config only (no build)"
exit 0
```python

fi

if ["${DEBVISOR_DRYRUN:-0}" = "1"]; then

```python
echo "[DebVisor] DRYRUN enabled: configuration validated, skipping lb build"
exit 0
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 206

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
exit 0
```python

fi

if ["${DEBVISOR_DRYRUN:-0}" = "1"]; then

```python
echo "[DebVisor] DRYRUN enabled: configuration validated, skipping lb build"
exit 0
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 207

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

fi

if ["${DEBVISOR_DRYRUN:-0}" = "1"]; then

```python
echo "[DebVisor] DRYRUN enabled: configuration validated, skipping lb build"
exit 0
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 208

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

if ["${DEBVISOR_DRYRUN:-0}" = "1"]; then

```python
echo "[DebVisor] DRYRUN enabled: configuration validated, skipping lb build"
exit 0
```python

fi

echo "[DebVisor] Building ISO (this can take a while)"

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 209

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

if ["${DEBVISOR_DRYRUN:-0}" = "1"]; then

```python
echo "[DebVisor] DRYRUN enabled: configuration validated, skipping lb build"
exit 0
```python

fi

echo "[DebVisor] Building ISO (this can take a while)"
lb build

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 210

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
echo "[DebVisor] DRYRUN enabled: configuration validated, skipping lb build"
exit 0
```python

fi

echo "[DebVisor] Building ISO (this can take a while)"
lb build
iso_name() {

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 211

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
exit 0
```python

fi

echo "[DebVisor] Building ISO (this can take a while)"
lb build
iso_name() {

```python
if [-n "${DEBVISOR_VERSION}"]; then
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 212

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

fi

echo "[DebVisor] Building ISO (this can take a while)"
lb build
iso_name() {

```python
if [-n "${DEBVISOR_VERSION}"]; then
    printf 'debvisor-%s-%s.hybrid.iso\n' "${DEBVISOR_VERSION}" "${DEBVISOR_ARCH}"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 213

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

echo "[DebVisor] Building ISO (this can take a while)"
lb build
iso_name() {

```python
if [-n "${DEBVISOR_VERSION}"]; then
    printf 'debvisor-%s-%s.hybrid.iso\n' "${DEBVISOR_VERSION}" "${DEBVISOR_ARCH}"
else
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 214

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

echo "[DebVisor] Building ISO (this can take a while)"
lb build
iso_name() {

```python
if [-n "${DEBVISOR_VERSION}"]; then
    printf 'debvisor-%s-%s.hybrid.iso\n' "${DEBVISOR_VERSION}" "${DEBVISOR_ARCH}"
else
    printf 'live-image-%s.hybrid.iso\n' "${DEBVISOR_ARCH}"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 215

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

lb build
iso_name() {

```python
if [-n "${DEBVISOR_VERSION}"]; then
    printf 'debvisor-%s-%s.hybrid.iso\n' "${DEBVISOR_VERSION}" "${DEBVISOR_ARCH}"
else
    printf 'live-image-%s.hybrid.iso\n' "${DEBVISOR_ARCH}"
fi
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 216

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

iso_name() {

```python
if [-n "${DEBVISOR_VERSION}"]; then
    printf 'debvisor-%s-%s.hybrid.iso\n' "${DEBVISOR_VERSION}" "${DEBVISOR_ARCH}"
else
    printf 'live-image-%s.hybrid.iso\n' "${DEBVISOR_ARCH}"
fi
```python

}

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 217

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
if [-n "${DEBVISOR_VERSION}"]; then
    printf 'debvisor-%s-%s.hybrid.iso\n' "${DEBVISOR_VERSION}" "${DEBVISOR_ARCH}"
else
    printf 'live-image-%s.hybrid.iso\n' "${DEBVISOR_ARCH}"
fi
```python

}

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 218

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    printf 'debvisor-%s-%s.hybrid.iso\n' "${DEBVISOR_VERSION}" "${DEBVISOR_ARCH}"
else
    printf 'live-image-%s.hybrid.iso\n' "${DEBVISOR_ARCH}"
fi
```python

}

ISO="$(iso_name)"

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 219

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
else
    printf 'live-image-%s.hybrid.iso\n' "${DEBVISOR_ARCH}"
fi
```python

}

ISO="$(iso_name)"
if [-f "${ISO}"]; then

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 220

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    printf 'live-image-%s.hybrid.iso\n' "${DEBVISOR_ARCH}"
fi
```python

}

ISO="$(iso_name)"
if [-f "${ISO}"]; then

```python
if command -v readlink >/dev/null 2>&1; then
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 221

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
fi
```python

}

ISO="$(iso_name)"
if [-f "${ISO}"]; then

```python
if command -v readlink >/dev/null 2>&1; then
    ISO_PATH="$(readlink -f "${ISO}" 2>/dev/null || echo "${ISO}")"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 222

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

}

ISO="$(iso_name)"
if [-f "${ISO}"]; then

```python
if command -v readlink >/dev/null 2>&1; then
    ISO_PATH="$(readlink -f "${ISO}" 2>/dev/null || echo "${ISO}")"
else
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 223

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

ISO="$(iso_name)"
if [-f "${ISO}"]; then

```python
if command -v readlink >/dev/null 2>&1; then
    ISO_PATH="$(readlink -f "${ISO}" 2>/dev/null || echo "${ISO}")"
else
    ISO_PATH="${ISO}"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 224

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

ISO="$(iso_name)"
if [-f "${ISO}"]; then

```python
if command -v readlink >/dev/null 2>&1; then
    ISO_PATH="$(readlink -f "${ISO}" 2>/dev/null || echo "${ISO}")"
else
    ISO_PATH="${ISO}"
fi
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 225

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

if [-f "${ISO}"]; then

```python
if command -v readlink >/dev/null 2>&1; then
    ISO_PATH="$(readlink -f "${ISO}" 2>/dev/null || echo "${ISO}")"
else
    ISO_PATH="${ISO}"
fi
echo "[DebVisor] Build complete: ${ISO_PATH}"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 226

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
if command -v readlink >/dev/null 2>&1; then
    ISO_PATH="$(readlink -f "${ISO}" 2>/dev/null || echo "${ISO}")"
else
    ISO_PATH="${ISO}"
fi
echo "[DebVisor] Build complete: ${ISO_PATH}"
```python

else

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 227

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    ISO_PATH="$(readlink -f "${ISO}" 2>/dev/null || echo "${ISO}")"
else
    ISO_PATH="${ISO}"
fi
echo "[DebVisor] Build complete: ${ISO_PATH}"
```python

else

```python
echo "[DebVisor] Build finished but ISO not found" >&2
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 228

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
else
    ISO_PATH="${ISO}"
fi
echo "[DebVisor] Build complete: ${ISO_PATH}"
```python

else

```python
echo "[DebVisor] Build finished but ISO not found" >&2
exit 1
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 229

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    ISO_PATH="${ISO}"
fi
echo "[DebVisor] Build complete: ${ISO_PATH}"
```python

else

```python
echo "[DebVisor] Build finished but ISO not found" >&2
exit 1
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 230

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
fi
echo "[DebVisor] Build complete: ${ISO_PATH}"
```python

else

```python
echo "[DebVisor] Build finished but ISO not found" >&2
exit 1
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 231

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
echo "[DebVisor] Build complete: ${ISO_PATH}"
```python

else

```python
echo "[DebVisor] Build finished but ISO not found" >&2
exit 1
```python

fi

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"]; then

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 232

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

else

```python
echo "[DebVisor] Build finished but ISO not found" >&2
exit 1
```python

fi

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"]; then

```python
echo "[DebVisor] Generating SHA256 checksum for ISO"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 233

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
echo "[DebVisor] Build finished but ISO not found" >&2
exit 1
```python

fi

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"]; then

```python
echo "[DebVisor] Generating SHA256 checksum for ISO"
sha256sum "${ISO}" > "${ISO}.sha256"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 234

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
exit 1
```python

fi

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"]; then

```python
echo "[DebVisor] Generating SHA256 checksum for ISO"
sha256sum "${ISO}" > "${ISO}.sha256"

```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 235

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

fi

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"]; then

```python
echo "[DebVisor] Generating SHA256 checksum for ISO"
sha256sum "${ISO}" > "${ISO}.sha256"

if command -v gpg >/dev/null 2>&1; then
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 236

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"]; then

```python
echo "[DebVisor] Generating SHA256 checksum for ISO"
sha256sum "${ISO}" > "${ISO}.sha256"

if command -v gpg >/dev/null 2>&1; then
    if [-n "${DEBVISOR_GPG_KEY:-}"]; then
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 237

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

if ["${DEBVISOR_SIGN_ISO:-0}" = "1"]; then

```python
echo "[DebVisor] Generating SHA256 checksum for ISO"
sha256sum "${ISO}" > "${ISO}.sha256"

if command -v gpg >/dev/null 2>&1; then
    if [-n "${DEBVISOR_GPG_KEY:-}"]; then
        echo "[DebVisor] Creating detached GPG signature with key: ${DEBVISOR_GPG_KEY}"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 238

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
echo "[DebVisor] Generating SHA256 checksum for ISO"
sha256sum "${ISO}" > "${ISO}.sha256"

if command -v gpg >/dev/null 2>&1; then
    if [-n "${DEBVISOR_GPG_KEY:-}"]; then
        echo "[DebVisor] Creating detached GPG signature with key: ${DEBVISOR_GPG_KEY}"
        gpg --local-user "${DEBVISOR_GPG_KEY}" --detach-sign --armor "${ISO}"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 239

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
sha256sum "${ISO}" > "${ISO}.sha256"

if command -v gpg >/dev/null 2>&1; then
    if [-n "${DEBVISOR_GPG_KEY:-}"]; then
        echo "[DebVisor] Creating detached GPG signature with key: ${DEBVISOR_GPG_KEY}"
        gpg --local-user "${DEBVISOR_GPG_KEY}" --detach-sign --armor "${ISO}"
    else
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 240

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
if command -v gpg >/dev/null 2>&1; then
    if [-n "${DEBVISOR_GPG_KEY:-}"]; then
        echo "[DebVisor] Creating detached GPG signature with key: ${DEBVISOR_GPG_KEY}"
        gpg --local-user "${DEBVISOR_GPG_KEY}" --detach-sign --armor "${ISO}"
    else
        echo "[DebVisor] Creating detached GPG signature with default key"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 241

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
if command -v gpg >/dev/null 2>&1; then
    if [-n "${DEBVISOR_GPG_KEY:-}"]; then
        echo "[DebVisor] Creating detached GPG signature with key: ${DEBVISOR_GPG_KEY}"
        gpg --local-user "${DEBVISOR_GPG_KEY}" --detach-sign --armor "${ISO}"
    else
        echo "[DebVisor] Creating detached GPG signature with default key"
        gpg --detach-sign --armor "${ISO}"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 242

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    if [-n "${DEBVISOR_GPG_KEY:-}"]; then
        echo "[DebVisor] Creating detached GPG signature with key: ${DEBVISOR_GPG_KEY}"
        gpg --local-user "${DEBVISOR_GPG_KEY}" --detach-sign --armor "${ISO}"
    else
        echo "[DebVisor] Creating detached GPG signature with default key"
        gpg --detach-sign --armor "${ISO}"
    fi
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 243

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
        echo "[DebVisor] Creating detached GPG signature with key: ${DEBVISOR_GPG_KEY}"
        gpg --local-user "${DEBVISOR_GPG_KEY}" --detach-sign --armor "${ISO}"
    else
        echo "[DebVisor] Creating detached GPG signature with default key"
        gpg --detach-sign --armor "${ISO}"
    fi
else
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 244

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
        gpg --local-user "${DEBVISOR_GPG_KEY}" --detach-sign --armor "${ISO}"
    else
        echo "[DebVisor] Creating detached GPG signature with default key"
        gpg --detach-sign --armor "${ISO}"
    fi
else
    echo "[DebVisor] WARNING: gpg not found; skipping ISO signature" >&2
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 245

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    else
        echo "[DebVisor] Creating detached GPG signature with default key"
        gpg --detach-sign --armor "${ISO}"
    fi
else
    echo "[DebVisor] WARNING: gpg not found; skipping ISO signature" >&2
fi
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 246

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
        echo "[DebVisor] Creating detached GPG signature with default key"
        gpg --detach-sign --armor "${ISO}"
    fi
else
    echo "[DebVisor] WARNING: gpg not found; skipping ISO signature" >&2
fi
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 247

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
        gpg --detach-sign --armor "${ISO}"
    fi
else
    echo "[DebVisor] WARNING: gpg not found; skipping ISO signature" >&2
fi
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 248

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    fi
else
    echo "[DebVisor] WARNING: gpg not found; skipping ISO signature" >&2
fi
```python

fi

if [-x build/test-firstboot.sh]; then

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 249

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
else
    echo "[DebVisor] WARNING: gpg not found; skipping ISO signature" >&2
fi
```python

fi

if [-x build/test-firstboot.sh]; then

```python
echo "[DebVisor] You can run post-build tests with: build/test-firstboot.sh"
```python

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 250

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
    echo "[DebVisor] WARNING: gpg not found; skipping ISO signature" >&2
fi
```python

fi

if [-x build/test-firstboot.sh]; then

```python
echo "[DebVisor] You can run post-build tests with: build/test-firstboot.sh"
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 251

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

```python
fi
```python

fi

if [-x build/test-firstboot.sh]; then

```python
echo "[DebVisor] You can run post-build tests with: build/test-firstboot.sh"
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 252

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

fi

if [-x build/test-firstboot.sh]; then

```python
echo "[DebVisor] You can run post-build tests with: build/test-firstboot.sh"
```python

fi

```python

### Proposal
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 253

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context
```python

if [-x build/test-firstboot.sh]; then

```python
echo "[DebVisor] You can run post-build tests with: build/test-firstboot.sh"
```python

fi

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
