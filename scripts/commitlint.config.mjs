/*
 * Commitlint configuration (ES Module) for DebVisor
 * Enforces Conventional Commits: https://www.conventionalcommits.org/
 */

export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Allow either lower-case or sentence-case subjects for flexibility
    'subject-case': [2, 'always', ['lower-case', 'sentence-case']],
    // Disallow trailing periods in subject
    'subject-full-stop': [2, 'never', '.'],
    // Ensure type is present and valid
    'type-enum': [2, 'always', [
      'build',
      'chore',
      'ci',
      'docs',
      'feat',
      'fix',
      'perf',
      'refactor',
      'revert',
      'style',
      'test'
    ]]
  }
};
