# Improvements for `agent-context.py`

● I'll analyze the `agent-context.py` file and suggest concrete, actionable improvements.

● Now I'll create comprehensive, actionable improvements for `agent-context.py`:

● Let me view the file first to make a proper edit:

● I apologize - I cannot edit the file directly due to tool restrictions. Let me provide you with
   the improved improvements content that you can apply manually:

● ## Enhanced Improvements for `agent-context.py`

   Based on deep analysis of both `agent-context.py` (70 lines) and `base_agent.py` (548 lines),
   here are comprehensive, actionable improvements:

---

## **High-Priority Improvements**

### **1. Source Code Integration** - CRITICAL MISSING FEATURE

**Problem**: Agent describes `.description.md` files without reading the actual source code.

**Impact**: Descriptions rely solely on filenames and existing content, not code analysis.

**Implementation**:

```python
class ContextAgent(BaseAgent):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.source_path = self._derive_source_path()

    def _derive_source_path(self) -> Optional[Path]:
        """Derive source file path from .description.md filename."""
        if self.file_path.name.endswith('.description.md'):
            stem = self.file_path.stem.replace('.description', '')
            # Try common extensions
            for ext in ['.py', '.js', '.ts', '.go', '.rs', '.java']:
                source = self.file_path.parent / f"{stem}{ext}"
                if source.exists():
                    return source
        return None

    def improve_content(self, prompt: str) -> str:
        """Include source code in AI context for accurate descriptions."""
        if self.source_path and self.source_path.exists():
            source_code = self.source_path.read_text[:8000](encoding='utf-8')
            enhanced_prompt = (
                f"{prompt}\n\n"
                f"Source code to analyze:\n```\n{source_code}\n```"
            )
            return super().improve_content(enhanced_prompt)
        return super().improve_content(prompt)
```

**Tests**: `test_derives_source_path()`, `test_includes_source_in_prompt()`,
`test_handles_missing_source()`

---

### **2. Filename Validation**

**Problem**: No validation that files end with `.description.md` - could overwrite arbitrary
files.

**Risk**: User typos could corrupt source files.

**Implementation**:

```python
def __init__(self, file_path: str):
    super().__init__(file_path)
    if not self.file_path.name.endswith('.description.md'):
        raise ValueError(
            f"Context files must end with '.description.md', got: {self.file_path.name}"
        )
```

**Tests**: `test_rejects_invalid_filenames()`, `test_accepts_valid_filenames()`

---

### **3. Structured Description Template**

**Problem**: Default content is minimal: `"# Description\n\nNo description available.\n"`

**Impact**: Inconsistent, low-quality descriptions.

**Implementation**:

```python
def _get_default_content(self) -> str:
    """Return rich, structured template for new descriptions."""
    filename = self.file_path.stem.replace('.description', '')
    return f"""# Description: `{filename}`

## Purpose
[One-line purpose statement]

## Functionality
[Key features and behaviors]

## Public API
- Classes: [List classes]
- Functions: [List functions]
- Constants: [List exported constants]

## Dependencies
- [Key imports and external dependencies]

## Usage Examples

```
[CLI commands or code examples]
```

## Implementation Notes
[Design decisions, caveats, limitations]
"""
```

**Benefits**: Enforces consistency, guides AI to comprehensive descriptions

**Tests**: `test_template_has_all_sections()`, `test_template_includes_filename()`

---

## **Medium-Priority Improvements**

### **4. Enhanced Prompts with Format Enforcement**

**Current**: Generic prompts passed directly to AI

**Improvement**: Structure prompts to enforce output quality

```python
def improve_content(self, prompt: str) -> str:
    """Enhanced with structured output requirements."""
    structured_prompt = f"""
Task: Improve code description using this structured format.

Requirements:
- Analyze provided source code (if available)
- Use specific method/class names from code
- Technical but accessible language
- Each section under 500 characters
- Focus on what code actually does, not aspirations

User request: {prompt}

Output: Markdown with sections - Purpose, Functionality, Public API, Dependencies, Usage
Examples.
"""
    # Include source code if available
    if self.source_path and self.source_path.exists():
        source = self.source_path.read_text[:8000](encoding='utf-8')
        structured_prompt += f"\n\nSource code:\n```\n{source}\n```"

    return super().improve_content(structured_prompt)
```

---

### **5. Section-Based Updates** (Complex - Defer)

**Problem**: Regenerating entire file loses manual edits

**Solution**: Parse markdown, update only changed sections

**Complexity**: High - requires markdown parsing, section diffing, merge logic

**Evaluation**: Cost/benefit unclear. Manual edits should be preserved, but implementation is
non-trivial.

**Defer until proven necessary.**

---

## **Low-Priority / Already Complete**

### **✓ Backend Selection** (Implemented via BaseAgent)

- `--backend` CLI flag ✓
- `--describe-backends` diagnostics ✓
- `DV_AGENT_BACKEND` environment variable ✓
- Multi-backend: copilot, gh, github-models ✓

### **✓ Markdown Linting** (Implemented in BaseAgent.update_file)

- Calls `fix_markdown_content()` before writing ✓
- Only applied to `.md` files ✓
- Source code preserved ✓

### **✓ Fallback Handling** (Implemented in BaseAgent.run_subagent)

- Graceful when AI unavailable ✓
- Preserves original content ✓
- No placeholder corruption ✓

---

## **Implementation Roadmap**

**Phase 1** (High impact, low effort):

1. Add filename validation (10 lines, 1 test)
2. Enhance default template (20 lines, 2 tests)

**Phase 2** (High impact, medium effort):

3. Add source code integration (40 lines, 5 tests)
4. Enhance prompts with structure (15 lines, 2 tests)

**Phase 3** (Evaluate later):

5. Section-based updates (if user feedback indicates need)

**Estimated Totals**:

- New code: ~85 lines
- New tests: ~10 test cases
- Current: 70 lines → After: ~155 lines
- Complexity: Still low (extends BaseAgent cleanly)

---

## **Testing Strategy**

Create `tests/test_agent_context.py`:

```python
def test_source_path_derivation():
    # base_agent.description.md → base_agent.py

def test_rejects_non_description_files():
    # ValueError for wrong filenames

def test_template_structure():
    # Verify all sections present

def test_source_code_in_prompt():
    # Mock improve_content, verify source included

def test_multi_language_detection():
    # .py, .js, .go, etc.
```

---

## **Summary**

The current `agent-context.py` is **clean but limited**. It relies entirely on BaseAgent without
leveraging the source files it documents.

**Key transformation**: From "edit existing descriptions" to "analyze code and generate accurate
descriptions."

**Quick wins**: Filename validation + structured template = 2 hours effort, immediate quality
improvement.

**Game changer**: Source code integration = transforms agent capability fundamentally.
