# Release Please Setup Guide

## Current Status

Release Please is configured and working correctly in terms of:
- ✅ Configuration files present (.release-please-manifest.json, release-please-config.json)
- ✅ Workflow file configured (.github/workflows/release-please.yml)
- ✅ Action successfully creating release branch and commit
- ❌ **Action cannot create Pull Request due to permissions**

## Required Repository Settings

To enable Release Please to create pull requests, you need to configure repository permissions:

### Step 1: Enable Workflow Permissions

1. Go to your repository on GitHub: <https://github.com/UndiFineD/DebVisor>
1. Click **Settings** (top navigation)
1. In the left sidebar, click **Actions** → **General**
1. Scroll to **Workflow permissions** section
1. Select **"Read and write permissions"**
1. ✅ **Check the box**: "Allow GitHub Actions to create and approve pull requests"
1. Click **Save**

### Step 2: Verify Permissions

After enabling, the next push should allow Release Please to:
- Create a pull request automatically
- Update CHANGELOG.md with commit history
- Bump version numbers according to conventional commits

## How Release Please Works

### Commit Convention

Release Please uses Conventional Commits to determine version bumps:

```text
feat: new feature         → Minor version bump (0.1.0 → 0.2.0)
fix: bug fix             → Patch version bump (0.1.0 → 0.1.1)
chore: maintenance       → No version bump
docs: documentation      → No version bump
ci: CI/CD changes        → No version bump

BREAKING CHANGE:         → Major version bump (0.1.0 → 1.0.0)
```

### Current Commits Being Processed

Release Please has analyzed **37 commits** and is ready to create a release PR that includes:

**Parsed Commits (30 valid):**
- All commits following conventional commit format (ci:, docs:, fix:, feat:, chore:)

**Unparsed Commits (7 skipped):**
- Merge commits from pull requests (normal - these are skipped)
- Non-conventional commits like "update", "first commit", "license and ansible fixes"

### What Will Happen After Enabling Permissions

1. **Automatic PR Creation**: On next workflow run, Release Please will create a PR titled something like:
   ```
   chore(main): release 0.2.0
   ```

1. **PR Contents**: The PR will include:
   - Updated CHANGELOG.md with all conventional commits since v0.1.0
   - Updated .release-please-manifest.json with new version
   - Any other version files you configure

1. **Merging the PR**: When you merge the release PR:
   - A new GitHub Release will be created
   - A git tag will be created (e.g., v0.2.0)
   - The release will include the changelog entries

## Manual Alternative (If You Don't Want to Enable Permissions)

If you prefer not to give GitHub Actions permission to create PRs, you can:

### Option 1: Use Personal Access Token

1. Create a Personal Access Token (PAT) with `repo` scope
1. Add it as a repository secret named `RELEASE_PLEASE_TOKEN`
1. Update `.github/workflows/release-please.yml`:

```yaml
- uses: googleapis/release-please-action@v4
  with:
    token: ${{ secrets.RELEASE_PLEASE_TOKEN }}  # Add this line
```

### Option 2: Manual Release Process

Create releases manually following this process:

1. Review commits since last release
1. Determine version bump based on conventional commits
1. Update CHANGELOG.md manually
1. Update version in .release-please-manifest.json
1. Create git tag: `git tag -a v0.2.0 -m "Release 0.2.0"`
1. Push tag: `git push origin v0.2.0`
1. Create GitHub Release from the tag

## Troubleshooting

### Issue: "Could not find releases"

This is normal for a new repository. Release Please is looking for existing releases to determine the version bump. Since this is the first automated release, it's using the version specified in `.release-please-manifest.json` (0.1.0) as the baseline.

### Issue: "Commit could not be parsed"

These warnings are expected and non-blocking:
- Merge commits from PRs are automatically skipped
- Non-conventional commits are ignored for changelog but don't break the process
- Only properly formatted conventional commits are included in the release notes

### Issue: "GitHub Actions is not permitted"

This is the current blocker. Follow **Step 1** above to resolve.

## Next Steps

1. ✅ Complete: All Release Please configuration is done
1. ⏳ **Action Required**: Enable workflow permissions (see Step 1)
1. ⏳ Wait for next workflow run or trigger manually
1. ⏳ Review and merge the auto-generated release PR
1. ✅ Enjoy automated releases!

## References

- [Release Please Documentation](https://github.com/googleapis/release-please)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Actions Permissions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
