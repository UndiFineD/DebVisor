"""
CLI Utilities - Shared helper functions for CLI tools.

Provides common functionality for CLI tools to reduce code duplication,
including table formatting with fallback support.
"""
from typing import List, Any, Optional, Union

try:
    from tabulate import tabulate
except ImportError:
    def tabulate(data, headers=None, tablefmt="grid"):
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


def format_table(data: List[List[Any]], headers: Optional[List[str]] = None, tablefmt: str = "grid") -> str:
    """
    Format data as a table using tabulate or fallback.
    
    Args:
        data: List of rows (lists)
        headers: List of column headers
        tablefmt: Table format (default: grid)
        
    Returns:
        Formatted table string
    """
    return tabulate(data, headers=headers, tablefmt=tablefmt)
