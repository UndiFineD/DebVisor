● I'll analyze the current improvements file and the actual `agent-context.py` script to suggest
   better, more actionable improvements.

● Now let me check the test file to see what's actually tested:

● I can see the improvements file but cannot edit it due to tool restrictions. Let me provide you
   with the enhanced content:

   ## Enhanced Improvements for `agent-context.py`

   Based on deep analysis of the code, here are prioritized, actionable improvements:

   ### **High-Priority (Quick Wins)**

   1. **Source Code Reading** - CRITICAL MISSING FEATURE
      - Agent can't read the actual source file it's describing
      - Add methods to derive source path from `.description.md` filename
      - Include source code in AI prompts for accurate descriptions
      - Impact: Transforms from "edit descriptions" to "understand code and describe it"

   2. **Input Validation**
      - No check that file ends with `.description.md`
      - Risk of overwriting wrong files
      - Add validation in `__init__`
      - Test: `test_rejects_invalid_filenames()`

   3. **Enhanced Prompts with Source Context**
      - Current prompts lack source code context
      - Modify `improve_content()` to include truncated source code
      - Enforce structured output format in prompt
      - Test: `test_enhanced_prompt_includes_source()`

   ### **Medium-Priority (Structured Output)**

   4. **Template-Based Descriptions**
      - Current default is minimal
      - Define rich template in `_get_default_content()`
      - Sections: Purpose, Functionality, Public API, Dependencies, Usage
      - Ensures consistency across all descriptions

   5. **Selective Section Updates**
      - Currently regenerates entire file (loses manual edits)
      - Add markdown section parser
      - Update only changed sections
      - Complex - evaluate cost/benefit

   ### **Already Implemented ✓**
   - CLI `--backend` and `--describe-backends` (via BaseAgent)
   - Backend routing (DV_AGENT_BACKEND)
   - Class documentation exists

   The original suggestions were generic. These improvements are concrete, prioritized by impact,
   and include implementation hints and test strategies.
