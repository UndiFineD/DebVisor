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


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
CLI Utilities - Shared helper functions for CLI tools.

Provides common functionality for CLI tools to reduce code duplication,
including table formatting with fallback support, common argument parsing,
and standardized error handling.
"""

import sys
import argparse
import functools
from typing import List, Any, Optional, Callable

try:
    from tabulate import tabulate    # type: ignore
except ImportError:

    def tabulate(
        data: List[List[Any]],
        headers: Optional[List[str]] = None,
        tablefmt: str = "grid",
    ) -> str:
        """Fallback implementation for when tabulate is missing."""
        if not data:
            return ""

        # Simple string representation
        result = []
        if headers:
        # Convert headers to string
            header_row = [str(h) for h in headers]
            result.append(" | ".join(header_row))
            # Add separator line
            result.append("-" * len(result[0]))

        for row in data:
        # Convert row items to string
            str_row = [str(c) for c in row]
            result.append(" | ".join(str_row))

        return "\n".join(result)


def format_table(
    data: List[List[Any]], headers: Optional[List[str]] = None, tablefmt: str = "grid"
) -> str:
    """
    Format data as a table using tabulate or fallback.

    Args:
        data: List of rows (lists)
        headers: List of column headers
        tablefmt: Table format (default: grid)

    Returns:
        Formatted table string
    """
    return str(tabulate(data, headers=headers, tablefmt=tablefmt))


def setup_common_args(parser: argparse.ArgumentParser) -> None:
    """
    Add common arguments to an ArgumentParser.

    Adds:
        --output: Output format (table, json, text)
        --verbose: Enable verbose logging
    """
    parser.add_argument(
        "--output",
        choices=["table", "json", "text"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )


def print_error(message: str, exit_code: int = 1) -> None:
    """Print error message to stderr."""
    print(f"Error: {message}", file=sys.stderr)


def print_success(message: str) -> None:
    """Print success message to stdout."""
    print(f"Success: {message}")


def print_warning(message: str) -> None:
    """Print warning message to stderr."""
    print(f"Warning: {message}", file=sys.stderr)


def handle_cli_error(func: Callable[..., int]) -> Callable[..., int]:
    """
    Decorator to handle CLI errors gracefully.

    Catches exceptions, prints them to stderr, and returns exit code 1.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> int:
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user", file=sys.stderr)
            return 130
        except Exception as e:
            print_error(str(e))
            if "--verbose" in sys.argv:
                import traceback
                traceback.print_exc()
            return 1

    return wrapper
