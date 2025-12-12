import unittest
from pathlib import Path
import importlib.util

# Dynamically import fix_markdown_lint from repository root without modifying sys.path
ROOT = Path(__file__).resolve().parents[1]
FIXER_PATH = ROOT / "fix_markdown_lint.py"
spec = importlib.util.spec_from_file_location("fix_markdown_lint", str(FIXER_PATH))
module = importlib.util.module_from_spec(spec)  # type: ignore
assert spec and spec.loader
spec.loader.exec_module(module)  # type: ignore
fix_markdown_content = module.fix_markdown_content  # type: ignore


class TestFixMarkdownLint(unittest.TestCase):
    def test_heading_space(self):
        self.assertEqual(fix_markdown_content("##Heading\n"), "## Heading\n")

    def test_trailing_whitespace_removed(self):
        self.assertEqual(fix_markdown_content("Line with space   \n"), "Line with space\n")

    def test_list_marker_space(self):
        self.assertEqual(fix_markdown_content("-Item\n"), "- Item\n")
        self.assertEqual(fix_markdown_content("*Item\n"), "* Item\n")
        self.assertEqual(fix_markdown_content("+Item\n"), "+ Item\n")

    def test_numbered_list_space(self):
        self.assertEqual(fix_markdown_content("1.Item\n"), "1. Item\n")
        self.assertEqual(fix_markdown_content("12.Item\n"), "12. Item\n")

    def test_parenthesized_list_ok(self):
        self.assertEqual(fix_markdown_content("1.(a) Item\n"), "1. (a) Item\n")

    def test_version_strings_unchanged(self):
        self.assertEqual(fix_markdown_content("version 1.2\n"), "version 1.2\n")
        self.assertEqual(fix_markdown_content("v1.0.0 release\n"), "v1.0.0 release\n")
        self.assertEqual(fix_markdown_content("python 3.11.7\n"), "python 3.11.7\n")

    def test_decimal_numbers_unchanged(self):
        self.assertEqual(fix_markdown_content("value 0.5\n"), "value 0.5\n")

    def test_file_refs_unchanged(self):
        self.assertEqual(fix_markdown_content("see section1.2.md\n"), "see section1.2.md\n")


if __name__ == "__main__":
    unittest.main()
