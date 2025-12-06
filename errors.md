

## Analysis of Recent "Failures" (2025-12-06)

Upon investigation of recent workflow runs (e.g., #19994770587, #19994770578), the reported "failures" are actually **cancellations**.

- **Cause:** The workflows are configured with `concurrency: cancel-in-progress: true`. When new commits are pushed rapidly, previous runs are automatically cancelled to save resources.
- **Impact:** These are not actual code errors and can be ignored.
- **CodeQL Status:** The CodeQL workflow has successfully passed in recent runs (e.g., #19994770584), confirming the previous fix works.
