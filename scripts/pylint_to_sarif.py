# !/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# !/usr/bin/env python3

# !/usr/bin/env python3

"""Convert pylint JSON output to SARIF format."""

import json
import sys


def convert_pylint_to_sarif(input_file: str, output_file: str) -> None:
    """Convert pylint JSON output to SARIF v2.1.0 format."""
    try:
        with open(input_file) as f:
            pylint_results = json.load(f)

        # Build SARIF structure
        sarif = {
            "version": "2.1.0",
            "$schema": (
                "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/"
                "sarif-schema-2.1.0.json"
            ),
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "pylint",
                            "version": "1.0",
                            "informationUri": "https://pylint.pycqa.org/",
                        }
                    },
                    "results": [],
                }
            ],
        }

        # Convert pylint results to SARIF results (limit to 1000)
        for item in pylint_results[:1000]:
            result = {
                "ruleId": item.get("message-id", "unknown"),
                "level": "error" if item.get("type") == "error" else "warning",
                "message": {"text": item.get("message", "")},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": item.get("path", ""),
                                "uriBaseId": "%SRCROOT%",
                            },
                            "region": {
                                "startLine": int(item.get("line", 1)),
                                "startColumn": int(item.get("column", 1)),
                            },
                        }
                    }
                ],
            }
            sarif["runs"][0]["results"].append(result)  # type: ignore[index]

        # Write SARIF output
        with open(output_file, "w") as out:
            json.dump(sarif, out, indent=2)

        print(f"? Converted {len(sarif['runs'][0]['results'])} pylint issues to SARIF")  # type: ignore[index]

    except FileNotFoundError:
        print(f"[warn] Input file not found: {input_file}", file=sys.stderr)
        # Create empty SARIF
        with open(output_file, "w") as out:
            json.dump({"version": "2.1.0", "runs": []}, out)

    except Exception as e:
        print(f"[warn] SARIF conversion failed: {e}", file=sys.stderr)
        sys.exit(0)    # Don't fail the workflow


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: pylint_to_sarif.py <input.json> <output.sarif>")
        sys.exit(1)

    convert_pylint_to_sarif(sys.argv[1], sys.argv[2])
